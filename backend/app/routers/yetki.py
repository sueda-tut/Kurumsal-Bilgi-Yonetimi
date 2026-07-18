# Doküman yetkilerini listeleyen GET endpoint'ini tanımlar

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session

from app.crud.dokuman import dokuman_getir
from app.crud.yetki import (
    dokumanin_yetkilerini_listele,
)
from app.db.database import get_db
from app.schemas.dokuman_yetkisi import (
    DokumanYetkisiResponse,
)


router = APIRouter(
    tags=["Yetkiler"],
)


@router.get(
    "/dokumanlar/{dokuman_id}/yetkiler",
    response_model=list[DokumanYetkisiResponse],
)
def dokumanin_yetkileri(
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

    return dokumanin_yetkilerini_listele(
        db=db,
        dokuman_id=dokuman_id,
    )