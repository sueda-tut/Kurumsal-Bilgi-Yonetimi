from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base


class DokumanEtiketi(Base):
    __tablename__ = "dokuman_etiketleri"

    dokuman_etiket_id = Column(Integer, primary_key=True, index=True)
    dokuman_id = Column(
        Integer,
        ForeignKey("dokumanlar.dokuman_id"),
        nullable=False
    )
    etiket_adi = Column(String(50), nullable=False)

    dokuman = relationship(
        "Dokuman",
        back_populates="etiketler"
    )