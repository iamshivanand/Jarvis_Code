import asyncio
from dotenv import load_dotenv
from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions, ChatContext
from livekit.plugins import google, noise_cancellation

# Import your custom modules
from Jarvis_prompts import get_instructions_prompt, get_reply_prompts
from memory_loop import MemoryExtractor
from jarvis_reasoning import all_tools

load_dotenv()

class Assistant(Agent):
    def __init__(self, instructions: str, chat_ctx: ChatContext) -> None:
        super().__init__(
            chat_ctx=chat_ctx,
            instructions=instructions,
            llm=google.beta.realtime.RealtimeModel(voice="Charon"),
            tools=all_tools,
        )

async def entrypoint(ctx: agents.JobContext):
    # Get dynamic prompts
    instructions = await get_instructions_prompt()
    reply_prompt = get_reply_prompts()

    session = AgentSession(
        preemptive_generation=True
    )
    
    # Getting the current memory chat
    current_ctx = session.history.items
    
    # Instantiate the agent with the dynamic instructions
    assistant = Assistant(instructions=instructions, chat_ctx=current_ctx)

    # Start the session
    await session.start(
        room=ctx.room,
        agent=assistant,
        room_input_options=RoomInputOptions(
            noise_cancellation=noise_cancellation.BVC()
        ),
    )

    # Generate the initial reply
    await session.generate_reply(
        instructions=reply_prompt
    )

    # Start the memory saving loop
    conv_ctx = MemoryExtractor()
    # Running the memory loop as a background task
    asyncio.create_task(conv_ctx.run(current_ctx))
    


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))

    