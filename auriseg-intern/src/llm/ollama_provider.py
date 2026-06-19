from src.llm.provider import LLMProvider


class OllamaProvider(LLMProvider):

    def get_llm(self):
        raise NotImplementedError(
            "Ollama provider not implemented yet."
        )
