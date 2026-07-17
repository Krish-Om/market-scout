### Introduction:
This is an API application that demonstrates two simple agents working together to research and analyze a niche topic, “Clean Beauty and Preventive Wellness”. I have used the open-source framework CrewAI [CrewAI](https://docs.crewai.com) to build this application and wrapped it with FastAPI [FastAPI](https://fastapi.tiangolo.com), using Swagger [Swagger](https://swagger.io/) Docs for interaction.

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
## For docker:
- Run the command ```docker compose up ``` to start the service.

## For local dev:
- Run the command ```uv run fastapi dev``` inside the root project directory.
