import re
import string


class ExactMatchEvaluator:
    @staticmethod
    def _normalize(text: str) -> str:
        text = text.strip().lower()

        # Remove common Markdown formatting
        text = text.replace("**", "")
        text = text.replace("__", "")
        text = text.replace("*", "")
        text = text.replace("_", "")

        # Remove punctuation
        text = text.translate(
            str.maketrans("", "", string.punctuation)
        )

        # Collapse repeated whitespace
        text = re.sub(r"\s+", " ", text)

        return text.strip()

    @staticmethod
    def evaluate(
        model_output: str,
        expected_output: str,
    ) -> float:
        normalized_model_output = (
            ExactMatchEvaluator._normalize(model_output)
        )

        normalized_expected_output = (
            ExactMatchEvaluator._normalize(expected_output)
        )

        # Traditional normalized exact match
        if normalized_model_output == normalized_expected_output:
            return 1.0

        # Short-answer match:
        # expected answer appears as a complete phrase in model output
        pattern = (
            r"\b"
            + re.escape(normalized_expected_output)
            + r"\b"
        )

        if re.search(pattern, normalized_model_output):
            return 1.0

        return 0.0