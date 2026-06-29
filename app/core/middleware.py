import time

from fastapi import Request
from starlette.responses import Response


async def process_time_middleware(
    request: Request,
    call_next,
) -> Response:

    start = time.perf_counter()

    response = await call_next(request)

    elapsed = time.perf_counter() - start

    response.headers["X-Process-Time"] = f"{elapsed:.6f}"

    return response
