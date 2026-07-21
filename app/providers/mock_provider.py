import numpy as np
from app.providers.base import (
    BaseProvider,
    ProviderResponse,
)


class MockProvider(BaseProvider):

    def generate(
        self,
        *,
        prompt: str,
        model: str,
    ) -> ProviderResponse:

        response = (
            f"Mock response for model '{model}': {prompt}"
        )

        input_tokens = len(prompt.split())
        output_tokens = len(response.split())

        return ProviderResponse(
            text=response,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=input_tokens + output_tokens,
            cost=0.0,
        )
            
    def embedding(
        self,
        *,
        text: str,
    ):
        return np.zeros(1536)