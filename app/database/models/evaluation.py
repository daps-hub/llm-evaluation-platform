import uuid
from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Evaluation(Base):
    __tablename__ = "evaluations"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    provider: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="mock",
    )

    model: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    prompt: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    expected_response: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    actual_response: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    latency_ms: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    input_tokens: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    output_tokens: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    total_tokens: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    cost: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    semantic_similarity: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    correctness_score: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    hallucination_score: Mapped[float | None] = mapped_column(
          Float,
          nullable=True,
    )

    overall_score: Mapped[float | None] = mapped_column(
         Float,
         nullable=True,
    )
    
    relevance_score: Mapped[float | None] = mapped_column(
    Float,
    nullable=True,
    )
    judge_reasoning: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )