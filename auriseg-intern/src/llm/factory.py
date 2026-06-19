import os

from src.llm.groq_provider import GroqProvider
from src.llm.ollama_provider import OllamaProvider


def get_llm():
    provider = os.getenv(
        "LLM_PROVIDER",
        "groq"
    ).lower()

    if provider == "groq":
        return GroqProvider().get_llm()

    if provider == "ollama":
        return OllamaProvider().get_llm()

    raise ValueError(
        f"Unsupported provider: {provider}"
    )
