# SQLAlchemy veritabanı bağlantısını ve oturum yönetimini yapılandırır

import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# backend/.env dosyasının konumunu belirler
BACKEND_DIR = Path(__file__).resolve().parents[2]
ENV_PATH = BACKEND_DIR / ".env"

# Ortam değişkenlerini backend/.env dosyasından yükler
load_dotenv(dotenv_path=ENV_PATH)

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL bulunamadı. backend/.env dosyasını kontrol edin."
    )


# SQLAlchemy veritabanı motorunu oluşturur
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)


# Her istek için kullanılacak veritabanı oturumunu oluşturur
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


# FastAPI endpoint'lerine veritabanı oturumu sağlar
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()