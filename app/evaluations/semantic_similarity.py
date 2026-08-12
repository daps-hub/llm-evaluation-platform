from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class SemanticSimilarityEvaluator:
    _model: SentenceTransformer | None = None

    @classmethod
    def _get_model(cls) -> SentenceTransformer:
        if cls._model is None:
            cls._model = SentenceTransformer(
                "all-MiniLM-L6-v2"
            )

        return cls._model

    @classmethod
    def evaluate(
        cls,
        expected_output: str,
        model_output: str,
    ) -> float:
        if not expected_output or not model_output:
            return 0.0

        model = cls._get_model()

        embeddings = model.encode(
            [
                expected_output,
                model_output,
            ]
        )

        score = cosine_similarity(
            [embeddings[0]],
            [embeddings[1]],
        )[0][0]

        return float(score)