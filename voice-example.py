import asyncio

from openai import AsyncOpenAI
from openai.helpers import LocalAudioPlayer

openai = AsyncOpenAI()

input = """Alright, team, let's bring the energy—time to move, sweat, and feel amazing!\n\nWe're starting with a dynamic warm-up, so roll those shoulders, stretch it out, and get that body ready! Now, into our first round—squats, lunges, and high knees—keep that core tight, push through, you got this!\n\nHalfway there, stay strong—breathe, focus, and keep that momentum going! Last ten seconds, give me everything you've got!\n\nAnd… done! Take a deep breath, shake it out—you crushed it! Stay hydrated, stay moving, and I'll see you next time!"""

instructions = """Voice: High-energy, upbeat, and encouraging, projecting enthusiasm and motivation.\n\nPunctuation: Short, punchy sentences with strategic pauses to maintain excitement and clarity.\n\nDelivery: Fast-paced and dynamic, with rising intonation to build momentum and keep engagement high.\n\nPhrasing: Action-oriented and direct, using motivational cues to push participants forward.\n\nTone: Positive, energetic, and empowering, creating an atmosphere of encouragement and achievement."""

async def main() -> None:

    async with openai.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="coral",
        input=input,
        instructions=instructions,
        response_format="pcm",
    ) as response:
        await LocalAudioPlayer().play(response)

if __name__ == "__main__":
    asyncio.run(main())