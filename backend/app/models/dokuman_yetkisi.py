# Departman bazlı doküman yetkilerinin SQLAlchemy modelini tanımlar

from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    UniqueConstraint,
    text,
)
from sqlalchemy.orm import relationship

from app.db.base import Base


class DokumanYetkisi(Base):
    __tablename__ = "dokuman_yetkileri"

    __table_args__ = (
        UniqueConstraint(
            "dokuman_id",
            "departman_id",
            name="uq_dokuman_yetkileri_dokuman_departman",
        ),
    )

    yetki_id = Column(Integer, primary_key=True, index=True)

    dokuman_id = Column(
        Integer,
        ForeignKey(
            "dokumanlar.dokuman_id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    departman_id = Column(
        Integer,
        ForeignKey("departmanlar.departman_id"),
        nullable=False,
        index=True,
    )

    goruntuleyebilir_mi = Column(
        Boolean,
        nullable=False,
        server_default=text("TRUE"),
    )

    dokuman = relationship(
        "Dokuman",
        back_populates="yetkiler",
    )

    departman = relationship(
        "Departman",
        back_populates="dokuman_yetkileri",
    )