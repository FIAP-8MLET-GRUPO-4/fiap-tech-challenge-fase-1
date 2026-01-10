import time
import uuid
from typing import Callable

import structlog
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

log = structlog.get_logger("api")

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable):
        request_id = request.headers.get("x-request-id") or str(uuid.uuid4())
        start = time.perf_counter()
        response: Response | None = None

        try:
            response = await call_next(request)
            return response
        finally:
            elapsed_ms = (time.perf_counter() - start) * 1000
            log.info(
                "http_request",
                request_id=request_id,
                method=request.method,
                path=request.url.path,
                query=str(request.url.query),
                status_code=getattr(response, "status_code", None),
                duration_ms=round(elapsed_ms, 2),
                client_host=getattr(request.client, "host", None),
                user_agent=request.headers.get("user-agent"),
            )
