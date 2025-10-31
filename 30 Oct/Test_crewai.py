import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, LLM

# ---------------------------------------------------
# Load environment variables
# ---------------------------------------------------
load_dotenv()

# Required environment variables
OPENROUTER_API_KEY = os.getenv("OPENROUTER_CREWAI_KEY")
OPENROUTER_API_BASE = os.getenv("OPENROUTER_API_BASE", "https://openrouter.ai/api/v1")

if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY or OPENROUTER_CREWAI_KEY is missing in .env file")

# # Set them globally for LiteLLM
# os.environ["OPENROUTER_API_KEY"] = OPENROUTER_API_KEY
# os.environ["OPENROUTER_API_BASE"] = OPENROUTER_API_BASE
# os.environ["OR_APP_NAME"] = "CrewAI Climate Research Bot"
# os.environ["OR_SITE_URL"] = "https://example.com"  # optional, helps OpenRouter track usage

# ---------------------------------------------------
# Configure LLM with OpenRouter through LiteLLM
# ---------------------------------------------------
llm = LLM(
    model="openrouter/meta-llama/llama-3.3-8b-instruct:free",  # correct OpenRouter syntax
    temperature=0.7,
    api_key=OPENROUTER_API_KEY,
    base_url=OPENROUTER_API_BASE,
    litellm_provider="openrouter",  # required for LiteLLM routing
)

# ---------------------------------------------------
# Define agents
# ---------------------------------------------------
researcher = Agent(
    role="Researcher",
    goal="Find key facts about climate change from trusted sources.",
    backstory="An expert environmental scientist who specializes in climate data collection.",
    llm=llm,
    verbose=True,
)

writer = Agent(
    role="Writer",
    goal="Summarize the research into a short, engaging article.",
    backstory="A skilled communicator who writes accessible, informative science content.",
    llm=llm,
    verbose=True,
)

# ---------------------------------------------------
#  Define tasks
# ---------------------------------------------------
research_task = Task(
    description="Gather recent (2023–2025) data and key facts about climate change from scientific reports or credible sources.",
    expected_output="A list of 5 key, verifiable climate change facts with their sources.",
    agent=researcher,
)

writing_task = Task(
    description="Write a 200-word informative article based on the research findings.",
    expected_output="A concise, engaging summary article suitable for the general public.",
    agent=writer,
    context=[research_task],  # use previous task output as input
)

# ---------------------------------------------------
# Run the crew
# ---------------------------------------------------
crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, writing_task],
    verbose=True,
)

print("🚀 Running CrewAI with OpenRouter Llama 3.3 8B model...\n")
result = crew.kickoff()

print("\n=== 🧾 FINAL OUTPUT ===\n")
print(result)
