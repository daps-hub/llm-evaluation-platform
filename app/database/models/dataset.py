from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Dataset(Base):
    __tablename__ = "datasets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    items = relationship(
        "DatasetItem",
        back_populates="dataset",
        cascade="all, delete-orphan",
    )


class DatasetItem(Base):
    __tablename__ = "dataset_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    dataset_id: Mapped[int] = mapped_column(
        ForeignKey("datasets.id", ondelete="CASCADE")
    )

    prompt: Mapped[str] = mapped_column(Text)
    expected_output: Mapped[str] = mapped_column(Text)

    item_metadata: Mapped[dict | None] = mapped_column(
        "metadata",
        JSONB,
        nullable=True,
    )

    dataset = relationship(
        "Dataset",
        back_populates="items",
    )