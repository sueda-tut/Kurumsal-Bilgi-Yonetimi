# Parola işlemlerini ve JWT erişim tokenlarını yönetir

import os
from datetime import datetime, timedelta, timezone
from pathlib import Path

from dotenv import load_dotenv
from jose import JWTError, jwt
from passlib.context import CryptContext


# backend/.env dosyasını yükler
BACKEND_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BACKEND_DIR / ".env")

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_HOURS = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_HOURS", "8")
)

if not JWT_SECRET_KEY:
    raise RuntimeError(
        "JWT_SECRET_KEY bulunamadı. backend/.env dosyasını kontrol edin."
    )


# Bcrypt parola özetleme ayarlarını oluşturur
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


# Parolayı bcrypt ile özetler
def sifre_ozeti_olustur(sifre: str) -> str:
    return pwd_context.hash(sifre)


# Girilen parola ile veritabanındaki özeti karşılaştırır
def sifre_dogrula(sifre: str, sifre_ozeti: str) -> bool:
    try:
        return pwd_context.verify(sifre, sifre_ozeti)
    except (ValueError, TypeError):
        return False


# Kullanıcı için JWT erişim tokenı oluşturur
def erisim_tokeni_olustur(
    kullanici_id: int,
    expires_delta: timedelta | None = None,
) -> str:
    simdi = datetime.now(timezone.utc)

    sona_erme_tarihi = simdi + (
        expires_delta
        if expires_delta is not None
        else timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    )

    payload = {
        "sub": str(kullanici_id),
        "type": "access",
        "iat": simdi,
        "exp": sona_erme_tarihi,
    }

    return jwt.encode(
        payload,
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM,
    )


# JWT tokenını doğrular ve içindeki verileri döndürür
def erisim_tokeni_coz(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            JWT_SECRET_KEY,
            algorithms=[JWT_ALGORITHM],
        )

        if payload.get("type") != "access":
            raise JWTError("Geçersiz token türü.")

        return payload

    except JWTError as error:
        raise ValueError(
            "Geçersiz veya süresi dolmuş token."
        ) from error