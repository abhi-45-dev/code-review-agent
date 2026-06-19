from langchain_groq import ChatGroq

from src.llm.provider import LLMProvider


class GroqProvider(LLMProvider):

    def get_llm(self):
        return ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0
        )
