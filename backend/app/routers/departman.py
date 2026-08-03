# Departman listeleme ve yöneticiye özel departman oluşturma endpoint'lerini tanımlar

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.database import get_db
from app.models.departman import Departman
from app.models.kullanici import Kullanici
from app.schemas.departman import (
    DepartmanCreate,
    DepartmanResponse,
)


router = APIRouter(
    prefix="/departmanlar",
    tags=["Departmanlar"],
)


# Kayıt ekranı dahil olmak üzere departmanları herkese açık listeler
@router.get(
    "",
    response_model=list[DepartmanResponse],
    summary="Departmanları listele",
)
def departmanlari_listele(
    db: Session = Depends(get_db),
):
    sorgu = select(Departman).order_by(
        Departman.departman_id
    )

    return list(db.scalars(sorgu).all())


# Yalnızca yöneticinin yeni departman oluşturmasını sağlar
@router.post(
    "",
    response_model=DepartmanResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Yeni departman oluştur",
)
def departman_olustur(
    departman_verisi: DepartmanCreate,
    db: Session = Depends(get_db),
    current_user: Kullanici = Depends(get_current_user),
):
    if current_user.rol != "Yonetici":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Yalnızca yöneticiler departman ekleyebilir.",
        )

    departman_adi = " ".join(
        departman_verisi.departman_adi.strip().split()
    )

    mevcut_departman_sorgusu = select(Departman).where(
        func.lower(Departman.departman_adi)
        == departman_adi.lower()
    )

    mevcut_departman = db.scalar(
        mevcut_departman_sorgusu
    )

    if mevcut_departman is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Bu isimde bir departman zaten bulunuyor.",
        )

    yeni_departman = Departman(
        departman_adi=departman_adi,
    )

    try:
        db.add(yeni_departman)
        db.commit()
        db.refresh(yeni_departman)

        return yeni_departman

    except IntegrityError as error:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Bu isimde bir departman zaten bulunuyor.",
        ) from error