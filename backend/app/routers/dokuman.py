# Doküman listeleme ve detay endpoint'lerini yetki kontrollü sunar

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.crud.dokuman import (
    dokuman_getir,
    dokumanlari_listele,
)
from app.db.database import get_db
from app.models.kullanici import Kullanici
from app.schemas.dokuman import DokumanResponse
from app.services.dokuman_yetki import (
    dokumani_gorebilir_mi,
    gorebildigi_dokuman_idleri,
)


router = APIRouter(
    prefix="/dokumanlar",
    tags=["Dokümanlar"],
)


@router.get(
    "",
    response_model=list[DokumanResponse],
    summary="Yetkiye göre doküman listesi",
)
def dokuman_listesi(
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: Kullanici = Depends(get_current_user),
):
    gorulebilir_idler = gorebildigi_dokuman_idleri(
        db=db,
        kullanici=current_user,
    )

    return dokumanlari_listele(
        db=db,
        gorulebilir_dokuman_idleri=gorulebilir_idler,
        offset=offset,
        limit=limit,
    )


@router.get(
    "/{dokuman_id}",
    response_model=DokumanResponse,
    summary="Yetki kontrollü doküman detayı",
)
def dokuman_detayi(
    dokuman_id: int,
    db: Session = Depends(get_db),
    current_user: Kullanici = Depends(get_current_user),
):
    dokuman = dokuman_getir(
        db=db,
        dokuman_id=dokuman_id,
    )

    if dokuman is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doküman bulunamadı.",
        )

    if not dokumani_gorebilir_mi(
        db=db,
        kullanici=current_user,
        dokuman_id=dokuman_id,
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bu dokümanı görüntüleme yetkiniz yok.",
        )

    return dokuman