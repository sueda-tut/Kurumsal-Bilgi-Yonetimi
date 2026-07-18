# Doküman etiketlerini listeleyen GET endpoint'ini tanımlar

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session

from app.crud.dokuman import dokuman_getir
from app.crud.etiket import (
    dokumanin_etiketlerini_listele,
)
from app.db.database import get_db
from app.schemas.dokuman_etiketi import (
    DokumanEtiketiResponse,
)


router = APIRouter(
    tags=["Etiketler"],
)


@router.get(
    "/dokumanlar/{dokuman_id}/etiketler",
    response_model=list[DokumanEtiketiResponse],
)
def dokumanin_etiketleri(
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

    return dokumanin_etiketlerini_listele(
        db=db,
        dokuman_id=dokuman_id,
    )