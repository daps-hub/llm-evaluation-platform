import os
from pathlib import Path
from typing import Final

import numpy as np
from dotenv import load_dotenv
from openai import OpenAI

from app.providers.base import BaseProvider, ProviderResponse


PROJECT_ROOT = Path(__file__).resolve().parents[2]
ENV_FILE = PROJECT_ROOT / ".env"

load_dotenv(dotenv_path=ENV_FILE)


MODEL_PRICING: Final[dict[str, dict[str, float]]] = {
    "gpt-4.1": {
        "input_per_million": 2.00,
        "output_per_million": 8.00,
    },
    "gpt-4.1-mini": {
        "input_per_million": 0.40,
        "output_per_million": 1.60,
    },
    "gpt-4.1-nano": {
        "input_per_million": 0.10,
        "output_per_million": 0.40,
    },
}


class OpenAIProvider(BaseProvider):
    def __init__(self) -> None:
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise RuntimeError(
                f"OPENAI_API_KEY is not configured. "
                f"Expected .env file at: {ENV_FILE}"
            )

        self.client = OpenAI(api_key=api_key)

    @staticmethod
    def calculate_cost(
        *,
        model: str,
        input_tokens: int,
        output_tokens: int,
    ) -> float:
        pricing = MODEL_PRICING.get(model)

        if pricing is None:
            raise ValueError(
                f"Pricing is not configured for model: {model}"
            )

        input_cost = (
            input_tokens
            / 1_000_000
            * pricing["input_per_million"]
        )

        output_cost = (
            output_tokens
            / 1_000_000
            * pricing["output_per_million"]
        )

        return round(input_cost + output_cost, 10)

    def generate(
        self,
        *,
        prompt: str,
        model: str,
    ) -> ProviderResponse:
        response = self.client.responses.create(
            model=model,
            input=prompt,
        )

        text = response.output_text or ""
        usage = response.usage

        input_tokens = usage.input_tokens if usage else 0
        output_tokens = usage.output_tokens if usage else 0

        total_tokens = (
            usage.total_tokens
            if usage and usage.total_tokens is not None
            else input_tokens + output_tokens
        )

        cost = self.calculate_cost(
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
        )

        return ProviderResponse(
            text=text,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=total_tokens,
            cost=cost,
        )

    def embedding(
        self,
        *,
        text: str,
    ) -> np.ndarray:
        response = self.client.embeddings.create(
            model="text-embedding-3-small",
            input=text,
        )

        return np.array(
            response.data[0].embedding,
            dtype=np.float32,
        )