from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class ExperimentStatus(str, Enum):
    CREATED = "created"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class Experiment(Base):
    __tablename__ = "experiments"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    dataset_id: Mapped[int] = mapped_column(
        ForeignKey("datasets.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    provider: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    model_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    status: Mapped[ExperimentStatus] = mapped_column(
        SqlEnum(
            ExperimentStatus,
            name="experiment_status",
            values_callable=lambda enum_class: [
                item.value for item in enum_class
            ],
        ),
        default=ExperimentStatus.CREATED,
        nullable=False,
    )

    error_message: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    started_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    dataset = relationship(
        "Dataset",
        back_populates="experiments",
    )

    results = relationship(
        "ExperimentResult",
        back_populates="experiment",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class ExperimentResult(Base):
    __tablename__ = "experiment_results"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    experiment_id: Mapped[int] = mapped_column(
        ForeignKey("experiments.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    dataset_item_id: Mapped[int] = mapped_column(
        ForeignKey("dataset_items.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    model_output: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    input_tokens: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    output_tokens: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    total_tokens: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    cost: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    exact_match_score: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    semantic_similarity_score: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    judge_score: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )
    
    judge_reasoning: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    latency_ms: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    error_message: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    experiment = relationship(
        "Experiment",
        back_populates="results",
    )

    dataset_item = relationship(
        "DatasetItem",
        back_populates="results",
    )

    generation_cost: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    judge_cost: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    total_cost: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )