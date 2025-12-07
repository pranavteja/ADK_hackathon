from google.adk.agents.llm_agent import Agent
from .tools import search_jobs, analyze_historical_rates, check_worker_availability, list_all_jobs

# --- Sub-Agents ---

job_finder_agent = Agent(
    model='gemini-2.5-flash',
    name='job_finder',
    description='Finds incoming jobs.',
    instruction=(
        "You find jobs in `gig_jobs.csv`. Use `search_jobs(category, location_query)`. "
        "Support 'anywhere' search. Report Urgency Level."
    ),
    tools=[search_jobs, list_all_jobs]
)

pricing_analyst_agent = Agent(
    model='gemini-2.5-flash',
    name='pricing_analyst',
    description='Analyzes historical data to estimate costs.',
    instruction=(
        "You determine fair prices using HISTORICAL data. "
        "Use `analyze_historical_rates(trade, description_keywords)` to find what similar jobs actually cost in the past. "
        "Do not just guess. Cite the 'Similar Job' found."
    ),
    tools=[analyze_historical_rates]
)

worker_manager_agent = Agent(
    model='gemini-2.5-flash',
    name='worker_manager',
    description='Manages worker availability.',
    instruction=(
        "Find available workers using `check_worker_availability(trade, pincode)`. "
        "Recommend workers based on Rating and Expertise (Elite/Expert)."
    ),
    tools=[check_worker_availability]
)

# --- Root Agent ---

root_agent = Agent(
    model='gemini-2.5-flash',
    name='gig_platform_brain',
    description='Coordinator for the Gig Platform.',
    instruction=(
        "You are the Brain of the Gig Agent Platform.\n"
        "Capabilities:\n"
        "1. Jobs: Ask `job_finder` what's new.\n"
        "2. Pricing: Ask `pricing_analyst` for estimates based on History.\n"
        "3. Workers: Ask `worker_manager` who is free.\n\n"
        "Flow: If a user wants a job, find it, then check history to tell them what it might pay, then find a worker if they are a customer."
    ),
    tools=[], 
    sub_agents=[job_finder_agent, pricing_analyst_agent, worker_manager_agent]
)
