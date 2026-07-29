from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class SemanticSimilarityEvaluator:
    _model = SentenceTransformer("all-MiniLM-L6-v2")

    @classmethod
    def evaluate(
        cls,
        expected_output: str,
        model_output: str,
    ) -> float:
        embeddings = cls._model.encode(
            [
                expected_output,
                model_output,
            ]
        )

        similarity = cosine_similarity(
            [embeddings[0]],
            [embeddings[1]],
        )[0][0]

        return float(similarity)