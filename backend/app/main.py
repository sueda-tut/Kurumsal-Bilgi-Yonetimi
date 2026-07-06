from fastapi import FastAPI
from sqlalchemy import text

from app.db.database import engine

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Kurumsal Bilgi Yönetimi API çalışıyor!"}


@app.get("/db-test")
def db_test():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        return {
            "database_connection": "Başarılı",
            "result": result.scalar()
        }