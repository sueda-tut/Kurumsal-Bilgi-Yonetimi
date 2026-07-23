# API hatalarını standart JSON yanıt biçimine dönüştürür

import logging
from typing import Any

from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.requests import Request
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR


logger = logging.getLogger("app.error")


HATA_KODLARI = {
    400: "BAD_REQUEST",
    401: "UNAUTHORIZED",
    403: "FORBIDDEN",
    404: "NOT_FOUND",
    409: "CONFLICT",
    413: "FILE_TOO_LARGE",
    415: "UNSUPPORTED_MEDIA_TYPE",
    422: "VALIDATION_ERROR",
    500: "INTERNAL_SERVER_ERROR",
}


def hata_yaniti_olustur(
    request: Request,
    status_code: int,
    message: str,
    details: Any = None,
    headers: dict[str, str] | None = None,
) -> JSONResponse:
    hata = {
        "code": HATA_KODLARI.get(
            status_code,
            "HTTP_ERROR",
        ),
        "message": message,
    }

    if details is not None:
        hata["details"] = details

    return JSONResponse(
        status_code=status_code,
        headers=headers,
        content={
            "success": False,
            "error": hata,
            "path": request.url.path,
        },
    )


async def http_exception_handler(
    request: Request,
    exception: HTTPException,
) -> JSONResponse:
    if isinstance(exception.detail, str):
        message = exception.detail
        details = None
    else:
        message = "İstek gerçekleştirilemedi."
        details = exception.detail

    logger.warning(
        "%s %s | %s | %s",
        request.method,
        request.url.path,
        exception.status_code,
        message,
    )

    return hata_yaniti_olustur(
        request=request,
        status_code=exception.status_code,
        message=message,
        details=details,
        headers=exception.headers,
    )


async def validation_exception_handler(
    request: Request,
    exception: RequestValidationError,
) -> JSONResponse:
    hatalar = []

    for hata in exception.errors():
        konum = [
            str(parca)
            for parca in hata.get("loc", [])
            if parca != "body"
        ]

        hatalar.append(
            {
                "field": ".".join(konum),
                "message": hata.get(
                    "msg",
                    "Geçersiz değer.",
                ),
                "type": hata.get(
                    "type",
                    "validation_error",
                ),
            }
        )

    logger.warning(
        "%s %s | 422 | doğrulama hatası",
        request.method,
        request.url.path,
    )

    return hata_yaniti_olustur(
        request=request,
        status_code=422,
        message="Gönderilen veriler geçersiz.",
        details=hatalar,
    )


async def genel_exception_handler(
    request: Request,
    exception: Exception,
) -> JSONResponse:
    logger.exception(
        "%s %s | beklenmeyen hata",
        request.method,
        request.url.path,
        exc_info=exception,
    )

    return hata_yaniti_olustur(
        request=request,
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        message="Beklenmeyen bir sunucu hatası oluştu.",
    )