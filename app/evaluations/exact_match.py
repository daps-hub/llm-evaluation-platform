class ExactMatchEvaluator:
    @staticmethod
    def evaluate(
        model_output: str,
        expected_output: str,
    ) -> float:
        normalized_model_output = model_output.strip().lower()
        normalized_expected_output = expected_output.strip().lower()

        return float(
            normalized_model_output
            == normalized_expected_output
        )