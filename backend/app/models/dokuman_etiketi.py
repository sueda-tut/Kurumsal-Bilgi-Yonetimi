# Doküman etiketleri tablosunun SQLAlchemy modelini tanımlar

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from app.db.base import Base


class DokumanEtiketi(Base):
    __tablename__ = "dokuman_etiketleri"

    __table_args__ = (
        UniqueConstraint(
            "dokuman_id",
            "etiket_adi",
            name="uq_dokuman_etiketleri_dokuman_etiket",
        ),
    )

    dokuman_etiket_id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    dokuman_id = Column(
        Integer,
        ForeignKey(
            "dokumanlar.dokuman_id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    etiket_adi = Column(
        String(50),
        nullable=False,
        index=True,
    )

    dokuman = relationship(
        "Dokuman",
        back_populates="etiketler",
    )