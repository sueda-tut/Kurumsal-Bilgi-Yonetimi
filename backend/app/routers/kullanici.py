# Kullanıcı listeleme ve ID ile getirme endpoint'lerini tanımlar

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    status,
)
from sqlalchemy.orm import Session

from app.crud.kullanici import (
    kullanici_getir,
    kullanicilari_listele,
)
from app.db.database import get_db
from app.schemas.kullanici import KullaniciResponse


router = APIRouter(
    prefix="/kullanicilar",
    tags=["Kullanicilar"],
)


@router.get(
    "",
    response_model=list[KullaniciResponse],
)
def kullanici_listesi(
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return kullanicilari_listele(
        db=db,
        offset=offset,
        limit=limit,
    )


@router.get(
    "/{kullanici_id}",
    response_model=KullaniciResponse,
)
def kullanici_detayi(
    kullanici_id: int,
    db: Session = Depends(get_db),
):
    kullanici = kullanici_getir(
        db=db,
        kullanici_id=kullanici_id,
    )

    if kullanici is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Kullanıcı bulunamadı.",
        )

    return kullanici