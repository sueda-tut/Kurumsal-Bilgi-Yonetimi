from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base


class DokumanYetkisi(Base):
    __tablename__ = "dokuman_yetkileri"

    yetki_id = Column(Integer, primary_key=True, index=True)
    dokuman_id = Column(
        Integer,
        ForeignKey("dokumanlar.dokuman_id"),
        nullable=False
    )
    rol_adi = Column(String(30), nullable=False)
    goruntuleyebilir_mi = Column(Boolean, nullable=False, default=True)

    dokuman = relationship(
        "Dokuman",
        back_populates="yetkiler"
    )