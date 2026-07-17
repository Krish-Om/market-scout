from crewai import Crew, Process

from app.core.agents import business_analyst, market_researcher
from app.core.tasks import analysis_task, research_task


def run_market_scout(target_topic: str):
    market_scout_crew = Crew(
        agents=[market_researcher, business_analyst],
        tasks=[research_task, analysis_task],
        process=Process.sequential,
        verbose=False,
    )

    crew_output = market_scout_crew.kickoff(inputs={"topic": target_topic})
    return crew_output
