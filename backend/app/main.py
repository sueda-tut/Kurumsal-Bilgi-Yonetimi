# FastAPI uygulamasını, router'ları ve veritabanı test endpoint'ini yapılandırır

from fastapi import FastAPI, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.db.database import engine
from app.routers import (
    dokuman,
    etiket,
    kullanici,
    sohbet,
    yetki,
)


app = FastAPI(
    title="Kurumsal Bilgi Yönetimi API",
    description="RAG tabanlı kurumsal bilgi yönetimi sistemi",
    version="1.0.0",
)


app.include_router(kullanici.router)
app.include_router(dokuman.router)
app.include_router(sohbet.router)
app.include_router(etiket.router)
app.include_router(yetki.router)


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