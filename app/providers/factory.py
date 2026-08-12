from app.providers.base import BaseProvider
from app.providers.mock_provider import MockProvider
from app.providers.openai_provider import OpenAIProvider


class ProviderFactory:
    @staticmethod
    def create(provider: str) -> BaseProvider:
        provider_name = provider.strip().lower()

        if provider_name == "mock":
            return MockProvider()

        if provider_name == "openai":
            return OpenAIProvider()

        raise ValueError(
            f"Unsupported provider: {provider}"
        )