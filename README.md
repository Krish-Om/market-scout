### Introduction:
This is an API application that demonstrates two simple agents working together to research and analyze a niche topic, “Clean Beauty and Preventive Wellness”. I have used the open-source framework CrewAI [CrewAI](https://docs.crewai.com) to build this application and wrapped it with FastAPI [FastAPI](https://fastapi.tiangolo.com), using Swagger [Swagger](https://swagger.io/) Docs for interaction.
It is live at this link: [link](https://homeserver.saury-company.ts.net/docs)

### Prerequisites:
- Python 3.11+
- Docker[docker](https://docs.docker.com/get-started/get-docker) (for deployment) or Podman [podman](https://podman.io/docs/installation)
- Ollama/llama3.1:8b model (for local development)
- uv [uv](https://docs.astral.sh/uv/getting-started/installation/) # For Project and Package management.
- Groq API Key [GROQ](https://console.groq.com).

### Models Used:
I have used a local ollama/llama3.1:8b [ollama](https://docs.ollama.com/) model running locally in Podman for local development and groq/llama-3.1-8b-instant provided by groq. In testing, the Groq model is much faster than the latter.

### Project Structure:

```
market-scout/
│__ compose-dev.yaml # Development compose file.
|__ compose-deployment # Depolyment compose file.
├── .gitignore # Ignores .env, **pycache**, .venv
|__ .dockerignore # Ignores files for Docker build context.
├── README.md # Execution manual, setup guide, and documentation
├── requirements.txt # Package dependencies (fastapi, uvicorn, crewai, pydantic)
├── .env.example # Template for local secrets (copy to .env)
│
├── app/ # Main application package
│ ├── **__init__**.py
│ ├── main.py # FastAPI app initialization & routing injection
│ │
│ ├── api/ # HTTP layer
│ │ ├── **__init__**.py
│ │ ├── endpoints.py # Contains POST /scout
│ │ └── schemas.py # Pydantic v2 request/response models
│ │
│ └── core/ # AI & Business Logic layer
│ ├── **init**.py
│ ├── agents.py # CrewAI Agent definitions
│ ├── tasks.py # CrewAI Task definitions
│ └── crew.py # Crew assembly and execution orchestration.
| |__ Dockerfile # Docker image

```
### How to run:
- Clone this repo.
- Setup the environment file with valid credentials.
  - ``` cp .env.exmaple .env ```
- Edit the .env with valid credentials.
## For docker:
- Run the command ```docker compose -f compose-development up ``` to start the service locally.
- Run the command ```docker compose -f compose-deployment up ``` to start the service in deployment.

## For local dev:
- Run the command ```uv run fastapi dev``` inside the root project directory.

## Architecture:
User Request -> FastAPI -> Agent 1 (Research) -> Agent 2 (Scout/Writer) -> Redis -> Response

## AI modes of failure:
1. Hallucination 🌀: The LLM generates false facts about "clean beauty" ingredients or health regulations.

2. Context Drift & Attention Decay 📉: As the context window fills up, the agent forgets initial constraints or instructions.

3. Structural Breakage 💔: The second agent fails to output valid JSON/Pydantic format, causing your FastAPI backend or Redis parser to crash.

4. Cascading Error Amplification 🌊: Agent 1 makes a minor factual error or assumption, and Agent 2 accepts it as absolute truth, multiplying the error in the final REST API response.

5. API Latency & Timeout Exhaustion ⏳: Because two agents run linearly, the total execution time creeps past your HTTP timeout limits (e.g., 300 seconds), causing the REST API to drop the connection before Redis gets the data.
