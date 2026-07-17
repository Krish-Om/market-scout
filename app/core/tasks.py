from crewai import Task

from app.core.agents import business_analyst, market_researcher

research_task = Task(
    description=(
        "Conduct an in-depth investigation into the current market landscape of {topic}. "
        "Pinpoint the top 3 high-growth micro-trends (e.g., specific raw ingredients, "
        "functional bio-actives, or eco-packaging standards) and detail the exact consumer "
        "pain points driving them."
    ),
    expected_output="A deep-dive data brief covering clinical/consumer trend indicators and market gaps.",
    agent=market_researcher,
)

analysis_task = Task(
    description=(
        "Analyze the findings from the research task regarding {topic}. "
        "Synthesize these insights into a structured Market Scout Report. The report must contain: "
        "1. Executive Summary, 2. Top Growth Fields, 3. Strategic Barriers to Entry, and 4. A Go-to-Market Recommendation."
    ),
    expected_output="A polished, executive-ready Markdown report utilizing bold text, headers, and bullet structures.",
    agent=business_analyst,
)
