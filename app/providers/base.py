from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass
class ProviderResponse:
    text: str
    input_tokens: int
    output_tokens: int
    total_tokens: int
    cost: float


class BaseProvider(ABC):

    @abstractmethod
    def generate(
        self,
        *,
        prompt: str,
        model: str,
    ) -> ProviderResponse:
        ...

    @abstractmethod
    def embedding(
        self,
        *,
        text: str,
    ) -> Any:
        ...