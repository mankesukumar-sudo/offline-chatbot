import asyncio
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from agent.agent import root_agent

load_dotenv()

APP_NAME = "offline_chatbot"
USER_ID = "local_user"
SESSION_ID = "session_001"


async def run_chat() -> None:
    session_service = InMemorySessionService()
    await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
    )

    runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

    print("Offline Chatbot ready. Type 'exit' to quit.\n")
    while True:
        user_input = input("You: ").strip()
        if not user_input or user_input.lower() in {"exit", "quit"}:
            break

        message = types.Content(
            role="user",
            parts=[types.Part(text=user_input)],
        )

        reply = ""
        async for event in runner.run_async(
            user_id=USER_ID,
            session_id=SESSION_ID,
            new_message=message,
        ):
            if event.is_final_response() and event.content and event.content.parts:
                reply = "".join(
                    part.text for part in event.content.parts if getattr(part, "text", None)
                )

        print(f"Bot: {reply}\n")


if __name__ == "__main__":
    asyncio.run(run_chat())