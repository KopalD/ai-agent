from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from google.adk.agents import Agent

def get_current_time() -> dict:
    """
    A simple tool to get the current time in ISO format.
    """
    from datetime import datetime
    return {"current_time" : datetime.now().isoformat()}

# Define your root agent
root_agent = Agent(
    name="basic_agent",
    model="gemini-2.0-flash",
    description="Basic agent",
    instruction="You are a helpful agent! who provides information about various topics in detail.",
    tools=[get_current_time]
)
