"""Server-Sent Events (SSE) streaming utilities"""

import json
from typing import AsyncGenerator


async def create_sse_response(
    generator: AsyncGenerator[str, None]
) -> AsyncGenerator[str, None]:
    """
    Convert content generator to SSE format

    Args:
        generator: Async generator yielding content chunks

    Yields:
        SSE-formatted messages
    """
    try:
        async for chunk in generator:
            # Format as SSE message
            sse_message = f"data: {json.dumps({'content': chunk})}\n\n"
            yield sse_message

        # Send completion signal
        yield f"data: {json.dumps({'done': True})}\n\n"

    except Exception as e:
        # Send error message
        error_message = f"data: {json.dumps({'error': str(e)})}\n\n"
        yield error_message
