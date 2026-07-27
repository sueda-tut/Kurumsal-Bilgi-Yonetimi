# Doküman etiketlerini yetki kontrolüyle listeleyen endpoint'i tanımlar

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.crud.dokuman import dokuman_getir
from app.crud.etiket import (
    dokumanin_etiketlerini_listele,
)
from app.db.database import get_db
from app.models.kullanici import Kullanici
from app.schemas.dokuman_etiketi import (
    DokumanEtiketiResponse,
)
from app.services.dokuman_yetki import (
    dokumani_gorebilir_mi,
)


router = APIRouter(
    tags=["Etiketler"],
)


# Yalnızca dokümanı görebilen kullanıcılara etiketleri döndürür
@router.get(
    "/dokumanlar/{dokuman_id}/etiketler",
    response_model=list[DokumanEtiketiResponse],
    summary="Yetki kontrollü doküman etiketleri",
)
def dokumanin_etiketleri(
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
            detail=(
                "Bu dokümanın etiketlerini "
                "görüntüleme yetkiniz yok."
            ),
        )

    return dokumanin_etiketlerini_listele(
        db=db,
        dokuman_id=dokuman_id,
    )