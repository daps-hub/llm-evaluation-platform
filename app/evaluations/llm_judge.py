import json
import os
from abc import ABC, abstractmethod
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

from app.providers.openai_provider import OpenAIProvider


PROJECT_ROOT = Path(__file__).resolve().parents[2]
ENV_FILE = PROJECT_ROOT / ".env"

load_dotenv(dotenv_path=ENV_FILE)

JUDGE_MODEL = "gpt-4.1"


class BaseJudgeProvider(ABC):
    @abstractmethod
    def judge(
        self,
        prompt: str,
        expected_output: str,
        model_output: str,
    ) -> dict:
        raise NotImplementedError


class OpenAIJudgeProvider(BaseJudgeProvider):
    def __init__(self) -> None:
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise RuntimeError(
                f"OPENAI_API_KEY is not configured. "
                f"Expected .env file at: {ENV_FILE}"
            )

        self.client = OpenAI(api_key=api_key)

    def judge(
        self,
        prompt: str,
        expected_output: str,
        model_output: str,
    ) -> dict:
        response = self.client.responses.create(
            model=JUDGE_MODEL,
            input=f"""
You are an impartial expert evaluator.

Evaluate how well the model answer responds to the question
and matches the expected answer.

Question:
{prompt}

Expected Answer:
{expected_output}

Model Answer:
{model_output}

Score the answer from 0 to 10.

Return only valid JSON in this exact format:

{{
  "score": 8.5,
  "reasoning": "Short explanation."
}}
""",
        )

        output_text = response.output_text or ""

        try:
            evaluation = json.loads(output_text)
        except json.JSONDecodeError as exc:
            raise RuntimeError(
                f"Judge returned invalid JSON:\n{output_text}"
            ) from exc

        if "score" not in evaluation:
            raise RuntimeError(
                "Judge response does not contain a score."
            )

        if "reasoning" not in evaluation:
            raise RuntimeError(
                "Judge response does not contain reasoning."
            )

        score = float(evaluation["score"])

        if not 0 <= score <= 10:
            raise RuntimeError(
                f"Judge score must be between 0 and 10. "
                f"Received: {score}"
            )

        reasoning = str(evaluation["reasoning"])

        usage = response.usage

        judge_input_tokens = (
            usage.input_tokens if usage else 0
        )

        judge_output_tokens = (
            usage.output_tokens if usage else 0
        )

        judge_total_tokens = (
            usage.total_tokens
            if usage and usage.total_tokens is not None
            else judge_input_tokens + judge_output_tokens
        )

        judge_cost = OpenAIProvider.calculate_cost(
            model=JUDGE_MODEL,
            input_tokens=judge_input_tokens,
            output_tokens=judge_output_tokens,
        )

        return {
            "score": score,
            "reasoning": reasoning,
            "judge_model": JUDGE_MODEL,
            "judge_input_tokens": judge_input_tokens,
            "judge_output_tokens": judge_output_tokens,
            "judge_total_tokens": judge_total_tokens,
            "judge_cost": judge_cost,
        }


class LLMJudgeEvaluator:
    def __init__(self) -> None:
        self.provider = OpenAIJudgeProvider()

    def evaluate(
        self,
        prompt: str,
        expected_output: str,
        model_output: str,
    ) -> dict:
        return self.provider.judge(
            prompt=prompt,
            expected_output=expected_output,
            model_output=model_output,
        )