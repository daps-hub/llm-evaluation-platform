import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
import numpy as np
from app.providers.base import BaseProvider, ProviderResponse


PROJECT_ROOT = Path(__file__).resolve().parents[2]
ENV_FILE = PROJECT_ROOT / ".env"

load_dotenv(dotenv_path=ENV_FILE)


class OpenAIProvider(BaseProvider):
    def __init__(self) -> None:
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise RuntimeError(
                f"OPENAI_API_KEY is not configured. "
                f"Expected .env file at: {ENV_FILE}"
            )

        self.client = OpenAI(api_key=api_key)

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

        return ProviderResponse(
            text=text,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=total_tokens,
            cost=0.0,
        )
    def embedding(
        self,
        *,
        text: str,
    ):
        response = self.client.embeddings.create(
            model="text-embedding-3-small",
            input=text,
        )

        return np.array(response.data[0].embedding)