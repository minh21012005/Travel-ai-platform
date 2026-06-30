from dataclasses import dataclass


@dataclass(slots=True)
class LLMRequest:
    system_prompt: str
    user_prompt: str


@dataclass(slots=True)
class LLMResponse:
    text: str
