# Departmanlar tablosunun SQLAlchemy modelini tanımlar

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class Departman(Base):
    __tablename__ = "departmanlar"

    departman_id = Column(Integer, primary_key=True, index=True)
    departman_adi = Column(
        String(50),
        nullable=False,
        unique=True,
    )

    kullanicilar = relationship(
        "Kullanici",
        back_populates="departman",
    )

    dokumanlar = relationship(
        "Dokuman",
        back_populates="departman",
        foreign_keys="Dokuman.departman_id",
    )

    dokuman_yetkileri = relationship(
        "DokumanYetkisi",
        back_populates="departman",
    )