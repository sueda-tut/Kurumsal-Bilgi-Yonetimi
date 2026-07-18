# Doküman listeleme ve ID ile getirme endpoint'lerini tanımlar

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    status,
)
from sqlalchemy.orm import Session

from app.crud.dokuman import (
    dokuman_getir,
    dokumanlari_listele,
)
from app.db.database import get_db
from app.schemas.dokuman import DokumanResponse


router = APIRouter(
    prefix="/dokumanlar",
    tags=["Dokumanlar"],
)


@router.get(
    "",
    response_model=list[DokumanResponse],
)
def dokuman_listesi(
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return dokumanlari_listele(
        db=db,
        offset=offset,
        limit=limit,
    )


@router.get(
    "/{dokuman_id}",
    response_model=DokumanResponse,
)
def dokuman_detayi(
    dokuman_id: int,
    db: Session = Depends(get_db),
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

    return dokuman