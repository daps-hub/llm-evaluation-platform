from app.evaluations import ExactMatchEvaluator


def test_exact_match_identical_text():
    assert ExactMatchEvaluator.evaluate(
        model_output="Paris",
        expected_output="Paris",
    ) == 1.0


def test_exact_match_case_insensitive():
    assert ExactMatchEvaluator.evaluate(
        model_output="PARIS",
        expected_output="Paris",
    ) == 1.0


def test_exact_match_answer_inside_natural_language_response():
    assert ExactMatchEvaluator.evaluate(
        model_output="The capital of France is **Paris**.",
        expected_output="Paris",
    ) == 1.0


def test_exact_match_rejects_wrong_answer():
    assert ExactMatchEvaluator.evaluate(
        model_output="The capital of France is London.",
        expected_output="Paris",
    ) == 0.0
