import asyncio
import os
from typing import Optional

from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from utils import call_agent_async
from agent import root_agent


load_dotenv()

# Read DB URL from environment variable
db_url = os.environ.get("DATABASE_URL", "postgresql+asyncpg://kopal@localhost:5432/aidb")

# Database-backed session service
session_service = DatabaseSessionService(db_url=db_url)

# Runner
runner = Runner(
    agent=root_agent,
    app_name="advance_agent",
    session_service=session_service
)


def create_initial_state(user_id: str) -> dict:
    """
    Create an initial session state for a user.

    Args:
        user_id: Display id for the user.

    Returns:
        A dict representing the initial session state.
    """
    jobs = []

    return {"user_id": user_id, "jobs": jobs}


async def do_query(user_id: str, session_id: str, query: str):
    print("Starting query process...")
    # Setup constants
    APP_NAME = os.environ.get("APP_NAME")
    USER_ID = user_id
    SESSION_ID = session_id
    QUERY = query

    # Check for existing sessions for this user
    existing_sessions = await session_service.list_sessions(
        app_name=APP_NAME,
        user_id=USER_ID,
    )

    # If there's an existing session, use it, otherwise create a new one
    if existing_sessions and len(existing_sessions.sessions) > 0:
        # Use the most recent session
        SESSION_ID = existing_sessions.sessions[0].id
        print(f"Continuing existing session: {SESSION_ID}")
    else:
        # Create a new session with initial state
        new_session = await session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            state=create_initial_state(user_id=USER_ID),
        )
        SESSION_ID = new_session.id
        print(f"Created new session: {SESSION_ID}")


    # ===== PART 5: Interactive Conversation Loop =====

    await call_agent_async(runner, USER_ID, SESSION_ID, QUERY)


if __name__ == "__main__":
    import asyncio
    asyncio.run(do_query("test_user", "test_session", "what do you know about thailand ?"))
