from openai import OpenAI
import numpy as np

from app.config import get_settings

settings = get_settings()


class EmbeddingService:
    def __init__(self):
        self.client = OpenAI(
            api_key=settings.OPENAI_API_KEY
        )

    def embedding(self, text: str):
        response = self.client.embeddings.create(
            model="text-embedding-3-small",
            input=text,
        )

        return np.array(response.data[0].embedding)


def cosine_similarity(a, b):
    return float(
        np.dot(a, b)
        / (np.linalg.norm(a) * np.linalg.norm(b))
    )