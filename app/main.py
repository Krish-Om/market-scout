from logging import INFO, Logger

import crewai.llms.cache as _crewai_cache
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.endpoints import router

_crewai_cache.mark_cache_breakpoint = lambda msg: msg
logger = Logger("uvicorn.error")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
logger.log(level=INFO, msg="Initialized fastapi app")

app.include_router(router=router, prefix="/api/v1")
