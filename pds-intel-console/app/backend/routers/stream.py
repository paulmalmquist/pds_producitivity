from fastapi import APIRouter
from fastapi.responses import EventSourceResponse

from utils.sse import stream_tokens

router = APIRouter()


@router.get('/chat')
async def stream_chat(prompt: str):
    async def event_publisher():
        async for token in stream_tokens(
            f"Streaming response for '{prompt}' with incremental analysis."
        ):
            yield {'data': token}

    return EventSourceResponse(event_publisher())
