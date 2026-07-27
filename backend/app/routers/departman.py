# Aktif kullanıcılara departman listesini sunan endpoint'i tanımlar

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.database import get_db
from app.models.departman import Departman
from app.models.kullanici import Kullanici
from app.schemas.departman import DepartmanResponse


router = APIRouter(
    prefix="/departmanlar",
    tags=["Departmanlar"],
)


# Doküman listesinde kullanılmak üzere departmanları listeler
@router.get(
    "",
    response_model=list[DepartmanResponse],
    summary="Departmanları listele",
)
def departmanlari_listele(
    db: Session = Depends(get_db),
    current_user: Kullanici = Depends(get_current_user),
):
    sorgu = select(Departman).order_by(
        Departman.departman_id
    )

    return list(db.scalars(sorgu).all())