# Define two agents "Market Researcher" and "Business Analyst"

import os

from crewai import LLM, Agent

api_key = os.getenv("GROQ_API_KEY")
local_llm = None
if api_key:
    local_llm = LLM(
        llm_type="litellm",
        model="groq/llama-3.1-8b-instant",
        api_key=api_key,
        stream=False,
    )
# else: For local development
#     local_llm = LLM(model="ollama/llama3.1:8b", base_url="http://ollama:11434")

shared_llm = local_llm
market_researcher = Agent(
    role="Clean Beauty & Wellness Researcher",
    goal="Identify emerging consumer shifts, clinical ingredient trends, and formulation dynamics within {topic}",
    backstory=(
        "You are an elite research analyst specializing in the intersection of green science, "
        "dermatology, and preventive health. You filter out marketing buzzwords to find real "
        "formulation innovations, ingredient safety consumer demands, and regulatory shifts."
    ),
    llm=shared_llm,  # Claude, DeepSeek or OpenAI
    verbose=True,
    allow_delegation=False,
    max_execution_time=60,
)

# Agent 2: The Strategist
business_analyst = Agent(
    role="Preventive Wellness Business Strategist",
    goal="Synthesize raw trend data into a competitive market analysis and product positioning brief",
    backstory=(
        "You are a seasoned strategist in the premium wellness sector. You take complex "
        "ingredient and consumer trends and translate them into actionable business opportunities, "
        "mapping out immediate entry points and warning against market oversaturation."
    ),
    llm=shared_llm,
    verbose=True,
    allow_delegation=False,
    max_execution_time=120,
)
