import json
import re
from dataclasses import dataclass


@dataclass
class JudgeResult:
    correctness: float
    hallucination: float
    relevance: float
    overall: float
    reasoning: str


class LLMJudge:
    def evaluate(
        self,
        *,
        provider,
        model: str,
        prompt: str,
        expected: str,
        actual: str,
    ) -> JudgeResult:
        judge_prompt = f"""
You are an expert AI evaluator.

Evaluate the actual answer against the prompt and expected answer.

Prompt:
{prompt}

Expected Answer:
{expected}

Actual Answer:
{actual}

Return only one valid JSON object with this exact structure:

{{
    "correctness": 0.0,
    "hallucination": 0.0,
    "relevance": 0.0,
    "overall": 0.0,
    "reasoning": ""
}}

Requirements:
- All scores must be numbers between 0.0 and 1.0.
- Return JSON only.
- Do not use Markdown.
- Do not use code fences.
"""

        response = provider.generate(
            prompt=judge_prompt,
            model=model,
        )

        print(
            "RAW JUDGE RESPONSE:",
            repr(response.text),
            flush=True,
        )

        cleaned_text = self._clean_json(
            response.text,
        )
        
        print(
            "CLEANED JUDGE RESPONSE:",
            repr(cleaned_text),
            flush=True,
        )

        try:
            result = json.loads(cleaned_text)
        except json.JSONDecodeError as exc:
            raise ValueError(
                f"Judge returned invalid JSON: {response.text}"
            ) from exc

        print(
            "PARSED JUDGE RESULT:",
            result,
            flush=True,
        )

        return JudgeResult(
            correctness=self._validate_score(
                result.get("correctness"),
                "correctness",
            ),
            hallucination=self._validate_score(
                result.get("hallucination"),
                "hallucination",
            ),
            relevance=self._validate_score(
                result.get("relevance"),
                "relevance",
            ),
            overall=self._validate_score(
                result.get("overall"),
                "overall",
            ),
            reasoning=str(
                result.get("reasoning", "")
            ),
        )

    @staticmethod
    def _clean_json(
        text: str,
    ) -> str:
        cleaned = text.strip()

        cleaned = re.sub(
            r"^```(?:json)?\s*",
            "",
            cleaned,
            flags=re.IGNORECASE,
        )

        cleaned = re.sub(
            r"\s*```$",
            "",
            cleaned,
        )

        start = cleaned.find("{")
        end = cleaned.rfind("}")

        if start == -1 or end == -1:
            raise ValueError(
                f"Judge response did not contain JSON: {text}"
            )

        return cleaned[start : end + 1]

    @staticmethod
    def _validate_score(
        value,
        field_name: str,
    ) -> float:
        try:
            score = float(value)
        except (TypeError, ValueError) as exc:
            raise ValueError(
                f"Invalid score for {field_name}: {value}"
            ) from exc

        score = max(
            0.0,
            min(1.0, score),
        )

        return round(score, 4)