import re
from dataclasses import dataclass

from app.services.similarity import cosine_similarity


@dataclass
class EvaluationResult:
    semantic_similarity: float
    correctness_score: float
    hallucination_score: float
    overall_score: float


def normalize_text(text: str) -> str:
    text = re.sub(r"[*_`#>]", "", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


class EvaluationEngine:
    def evaluate(
        self,
        *,
        provider,
        expected: str | None,
        actual: str,
    ) -> EvaluationResult:
        if not expected:
            return EvaluationResult(
                semantic_similarity=0.0,
                correctness_score=0.0,
                hallucination_score=0.0,
                overall_score=0.0,
            )

        normalized_expected = normalize_text(expected)
        normalized_actual = normalize_text(actual)

        expected_vector = provider.embedding(
            text=normalized_expected,
        )

        actual_vector = provider.embedding(
            text=normalized_actual,
        )

        similarity = cosine_similarity(
            expected_vector,
            actual_vector,
        )

        correctness = similarity

        hallucination = max(
            0.0,
            1.0 - similarity,
        )

        overall = (
            similarity * 0.40
            + correctness * 0.40
            + (1.0 - hallucination) * 0.20
        )

        return EvaluationResult(
            semantic_similarity=round(similarity, 4),
            correctness_score=round(correctness, 4),
            hallucination_score=round(hallucination, 4),
            overall_score=round(overall, 4),
        )