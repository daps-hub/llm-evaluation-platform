import uuid
from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.models.evaluation import Evaluation


def create_evaluation(
    db: Session,
    *,
    provider: str,
    model: str,
    prompt: str,
    expected_response: str | None,
    actual_response: str,
    latency_ms: int,
    input_tokens: int,
    output_tokens: int,
    total_tokens: int,
    cost: float,
    status: str,
    semantic_similarity: float | None = None,
    correctness_score: float | None = None,
    hallucination_score: float | None = None,
    overall_score: float | None = None,
    relevance_score: float | None = None,
    judge_reasoning: str | None = None,
) -> Evaluation:
    evaluation = Evaluation(
        provider=provider,
        model=model,
        prompt=prompt,
        expected_response=expected_response,
        actual_response=actual_response,
        latency_ms=latency_ms,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        total_tokens=total_tokens,
        cost=cost,
        status=status,
        semantic_similarity=semantic_similarity,
        correctness_score=correctness_score,
        hallucination_score=hallucination_score,
        overall_score=overall_score,
        relevance_score=relevance_score,
        judge_reasoning=judge_reasoning,
    )

    db.add(evaluation)
    db.commit()
    db.refresh(evaluation)

    return evaluation


def get_evaluation_by_id(
    db: Session,
    evaluation_id: uuid.UUID,
) -> Evaluation | None:
    statement = select(Evaluation).where(
        Evaluation.id == evaluation_id,
    )

    return db.scalar(statement)


def list_evaluations(
    db: Session,
    *,
    offset: int = 0,
    limit: int = 50,
) -> Sequence[Evaluation]:
    statement = (
        select(Evaluation)
        .order_by(Evaluation.created_at.desc())
        .offset(offset)
        .limit(limit)
    )

    return db.scalars(statement).all()