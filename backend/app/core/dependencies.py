# JWT tokenından mevcut kullanıcıyı bulan FastAPI dependency'sini tanımlar

from fastapi import Depends, HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.security import erisim_tokeni_coz
from app.crud.kullanici import kullanici_getir
from app.db.database import get_db
from app.models.kullanici import Kullanici


bearer_scheme = HTTPBearer(auto_error=False)


# Bearer tokenını doğrular ve giriş yapan kullanıcıyı döndürür
def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Security(
        bearer_scheme
    ),
    db: Session = Depends(get_db),
) -> Kullanici:
    kimlik_dogrulama_hatasi = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Geçersiz veya süresi dolmuş token.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if credentials is None:
        raise kimlik_dogrulama_hatasi

    try:
        payload = erisim_tokeni_coz(credentials.credentials)
        kullanici_id = int(payload.get("sub"))
    except (ValueError, TypeError):
        raise kimlik_dogrulama_hatasi

    kullanici = kullanici_getir(
        db=db,
        kullanici_id=kullanici_id,
    )

    if kullanici is None or not kullanici.aktif_mi:
        raise kimlik_dogrulama_hatasi

    return kullanici