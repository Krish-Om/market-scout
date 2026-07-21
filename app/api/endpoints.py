import asyncio
import json
import os
import uuid
from logging import DEBUG, INFO, Logger
from typing import Dict

import redis
from fastapi import APIRouter, BackgroundTasks, HTTPException, status

from app.api.schemas import ScoutRequest, ScoutResponse

logger = Logger(__name__, level=INFO)
router = APIRouter()


jobs_db: Dict[str, dict] = {}

redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
r = redis.from_url(redis_url, decode_responses=True)


async def worker(job_id: str, topic: str):
    """
    Worker function executed in background to handle the local GPU inference loop
    without blocking the main server thread.
    """
    from app.core.crew import run_market_scout

    try:
        r.set(f"job:{job_id}", json.dumps({"status": "processing", "result": None}))
        # kick off the crew
        crew_output = await asyncio.wait_for(
            asyncio.to_thread(run_market_scout, target_topic=topic), timeout=300.0
        )
        # 2. Parse result safely
        if crew_output.json_dict:
            result_data = crew_output.json_dict
        elif crew_output.pydantic:
            result_data = crew_output.pydantic.model_dump()
        else:
            result_data = str(crew_output)

        # 3. Save successful state to Redis (Expiring in 2 days to keep it clean)
        r.setex(
            f"job:{job_id}",
            172800,
            json.dumps(
                {
                    "status": "completed",
                    "result": result_data,
                    "token_usage": dict(crew_output.token_usage),
                }
            ),
        )
        logger.info(f"Job {job_id} completed successfully.")
    except asyncio.TimeoutError:
        r.set(
            f"job:{job_id}",
            json.dumps(
                {
                    "status": "failed",
                    "error": (
                        "Execution halted: Hard timeout of 300s breached (Agent Loop Cascade suspected)."
                    ),
                }
            ),
        )
        logger.error(
            f"Job {job_id} failed due to exceeding maximum allowed runtime context."
        )
    except Exception as e:
        jobs_db[job_id]["status"] = "failed"
        jobs_db[job_id]["error"] = f"Runtime Exception encountered: {str(e)}"
        logger.error(f"System Crash on Job {job_id} : {str(e)}")


@router.post(
    "/scout", response_model=ScoutResponse, status_code=status.HTTP_201_CREATED
)
async def start_market_scout(payload: ScoutRequest, background_tasks: BackgroundTasks):
    """
    Runs a crew to scout the market topic of "Clean beauty and Preventive Cleaness"
    Returns a job tracking id
    """

    try:
        # Call the service
        topic = payload.topic
        job_id = str(uuid.uuid4())

        jobs_db[job_id] = {
            "status": "pending",
            "topic": topic,
            "result": None,
            "error": None,
        }

        background_tasks.add_task(worker, job_id, topic)
        # await worker(job_id,topic)
        logger.info(msg=f"CrewAI job started with {job_id}")
        return ScoutResponse(
            job_id=job_id,
            status="pending",
            message="CrewAI successfully kicked off on local GPU, please wait a moment",
            token_usage={},
        )
    except Exception as e:
        logger.info(msg=e)
        raise Exception(f"Error: {e}")


@router.get(
    "/scout/",
    response_model=ScoutResponse,
    status_code=status.HTTP_200_OK,
)
async def get_scout_results(job_id: str):
    """
    Poll endpoint to check the inference status or retrieve the final results(Executive Summary).
    """
    try:
        job_data = r.get(f"job:{job_id.strip()}")

        if not job_data:
            raise HTTPException(
                status_code=404, detail="Job registration target not found in Redis."
            )
        logger.debug(
            msg=f"Job id : {job_id} status: {json.loads(job_data).get('status')} result: {json.loads(job_data).get('result')}"
        )
        job_dict = json.loads(job_data)
        return ScoutResponse(
            job_id=job_id,
            status=job_dict.get("status"),
            message=job_dict.get("result"),
            token_usage=job_dict.get("token_usage", {}),
        )
    except HTTPException as http_except:
        logger.info(msg=http_except)
        raise HTTPException(
            status_code=http_except.status_code, detail=http_except.detail
        )
    except Exception as e:
        logger.info(msg=e)
        raise Exception(f"Error: {e}")
