# FastAPI uygulamasını, router'ları, hata yönetimini ve loglamayı yapılandırır

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.core.exception_handlers import (
    genel_exception_handler,
    http_exception_handler,
    validation_exception_handler,
)
from app.core.logging_config import (
    RequestLoggingMiddleware,
    logging_yapilandir,
)
from app.db.database import engine
from app.routers import (
    dokuman,
    etiket,
    kullanici,
    sohbet,
    yetki,
)
from app.routers.auth import router as auth_router


# Uygulama başlatılırken temel log yapılandırmasını etkinleştirir
logging_yapilandir()


app = FastAPI(
    title="Kurumsal Bilgi Yönetimi API",
    description="RAG tabanlı kurumsal bilgi yönetimi sistemi",
    version="1.0.0",
)


# Bütün HTTP isteklerinin temel bilgilerini loglar
app.add_middleware(RequestLoggingMiddleware)

# Uygulama genelindeki hataları standart biçime dönüştürür
app.add_exception_handler(
    HTTPException,
    http_exception_handler,
)
app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler,
)
app.add_exception_handler(
    Exception,
    genel_exception_handler,
)


# Uygulamanın API router'larını bağlar
app.include_router(kullanici.router)
app.include_router(dokuman.router)
app.include_router(sohbet.router)
app.include_router(etiket.router)
app.include_router(yetki.router)
app.include_router(auth_router)


@app.get("/", tags=["Genel"])
def root():
    return {
        "message": "Kurumsal Bilgi Yönetimi API çalışıyor!"
    }


@app.get("/db-test", tags=["Veritabanı"])
def db_test():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))

        return {
            "database_connection": "Başarılı",
            "result": result.scalar(),
        }

    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=500,
            detail="Veritabanı bağlantısı başarısız.",
        ) from error