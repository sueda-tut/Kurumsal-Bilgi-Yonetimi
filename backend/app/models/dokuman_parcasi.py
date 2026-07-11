from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.base import Base


class DokumanParcasi(Base):
    __tablename__ = "dokuman_parcalari"

    parca_id = Column(Integer, primary_key=True, index=True)
    dokuman_id = Column(
        Integer,
        ForeignKey("dokumanlar.dokuman_id"),
        nullable=False
    )
    parca_sirasi = Column(Integer, nullable=False)
    parca_metni = Column(Text, nullable=False)
    sayfa_no = Column(Integer, nullable=True)
    token_sayisi = Column(Integer, nullable=False)
    embedding_id = Column(String(100), unique=True)
    olusturulma_tarihi = Column(DateTime, nullable=False, server_default=func.now())

    dokuman = relationship(
        "Dokuman",
        back_populates="parcalar"
    )