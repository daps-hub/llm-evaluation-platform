import traceback
import uuid
from collections.abc import Sequence
from time import perf_counter

from sqlalchemy.orm import Session

from app.database.models.evaluation import Evaluation
from app.evaluations.repository import (
    create_evaluation,
    get_evaluation_by_id,
    list_evaluations,
)
from app.evaluations.schemas import EvaluationCreate
from app.providers import ProviderFactory
from app.services.evaluator import EvaluationEngine
from app.services.judge import LLMJudge


def run_evaluation(
    db: Session,
    evaluation_data: EvaluationCreate,
) -> Evaluation:
    start_time = perf_counter()

    try:
        print(
            "STEP 1: Creating provider",
            flush=True,
        )

        provider = ProviderFactory.create(
            evaluation_data.provider,
        )

        print(
            "STEP 2: Generating actual response",
            flush=True,
        )

        provider_response = provider.generate(
            prompt=evaluation_data.prompt,
            model=evaluation_data.model,
        )

        print(
            "ACTUAL RESPONSE:",
            repr(provider_response.text),
            flush=True,
        )

        print(
            "STEP 3: Calculating semantic similarity",
            flush=True,
        )

        evaluation_result = EvaluationEngine().evaluate(
            provider=provider,
            expected=evaluation_data.expected_response or "",
            actual=provider_response.text,
        )

        print(
            "SEMANTIC SIMILARITY:",
            evaluation_result.semantic_similarity,
            flush=True,
        )

        print(
            "STEP 4: Running LLM judge",
            flush=True,
        )

        judge = LLMJudge().evaluate(
            provider=provider,
            model=evaluation_data.model,
            prompt=evaluation_data.prompt,
            expected=evaluation_data.expected_response or "",
            actual=provider_response.text,
        )

        print(
            "JUDGE RESULT:",
            judge,
            flush=True,
        )

        latency_ms = int(
            (perf_counter() - start_time) * 1000
        )

        print(
            "STEP 5: Saving evaluation",
            flush=True,
        )

        evaluation = create_evaluation(
            db,
            provider=evaluation_data.provider,
            model=evaluation_data.model,
            prompt=evaluation_data.prompt,
            expected_response=evaluation_data.expected_response,
            actual_response=provider_response.text,
            latency_ms=latency_ms,
            input_tokens=provider_response.input_tokens,
            output_tokens=provider_response.output_tokens,
            total_tokens=provider_response.total_tokens,
            cost=provider_response.cost,
            status="success",
            semantic_similarity=evaluation_result.semantic_similarity,
            correctness_score=judge.correctness,
            hallucination_score=judge.hallucination,
            overall_score=judge.overall,
            relevance_score=judge.relevance,
            judge_reasoning=judge.reasoning,
        )

        print(
            "STEP 6: Evaluation saved successfully",
            flush=True,
        )

        return evaluation

    except Exception as exc:
        db.rollback()

        print(
            "EVALUATION FAILED:",
            type(exc).__name__,
            str(exc),
            flush=True,
        )

        traceback.print_exc()

        raise


def get_evaluation(
    db: Session,
    evaluation_id: uuid.UUID,
) -> Evaluation | None:
    return get_evaluation_by_id(
        db,
        evaluation_id,
    )


def get_evaluations(
    db: Session,
    *,
    offset: int = 0,
    limit: int = 50,
) -> Sequence[Evaluation]:
    return list_evaluations(
        db,
        offset=offset,
        limit=limit,
    )