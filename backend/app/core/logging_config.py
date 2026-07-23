# Uygulamanın temel log yapılandırmasını ve istek loglarını yönetir

import logging
import os
from time import perf_counter

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()


def logging_yapilandir() -> None:
    logging.basicConfig(
        level=LOG_LEVEL,
        format=(
            "%(asctime)s | %(levelname)s | "
            "%(name)s | %(message)s"
        ),
        datefmt="%Y-%m-%d %H:%M:%S",
    )


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        logger = logging.getLogger("app.request")
        baslangic = perf_counter()

        try:
            response = await call_next(request)

        except Exception:
            sure_ms = (perf_counter() - baslangic) * 1000

            logger.exception(
                "%s %s | hata | %.2f ms",
                request.method,
                request.url.path,
                sure_ms,
            )

            raise

        sure_ms = (perf_counter() - baslangic) * 1000

        logger.info(
            "%s %s | %s | %.2f ms",
            request.method,
            request.url.path,
            response.status_code,
            sure_ms,
        )

        return response