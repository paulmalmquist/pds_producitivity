from collections.abc import AsyncIterator


async def stream_tokens(text: str) -> AsyncIterator[str]:
    for chunk in text.split():
        yield chunk + ' '
