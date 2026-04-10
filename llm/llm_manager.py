from agno.models.azure.openai_chat import AzureOpenAI
from agno.models.google.gemini import Gemini
from agno.models.huggingface.huggingface import HuggingFace
from agno.models.openai import OpenAIChat
from agno.models.openrouter.openrouter import OpenRouter

from config.setting import LLMProvider


class LLM_Manager:
    def __init__(self, setting):
        self.setting = setting
        self.model = self._init_model()

    def _init_model(self):
        provider = self.setting.LLM_PROVIDER

        if provider == LLMProvider.OPENAI:
            return OpenAIChat(
                id=self.setting.OPENAI_MODEL,
                api_key=self.setting.OPENAI_API_KEY,
                temperature=self.setting.LLM_TEMPERATURE,
            )

        if provider == LLMProvider.OPENROUTER:
            return OpenRouter(
                id=self.setting.OPENROUTER_MODEL,
                api_key=self.setting.OPENROUTER_API_KEY,
                temperature=self.setting.LLM_TEMPERATURE,
            )

        if provider == LLMProvider.GEMINI:
            return Gemini(
                id=self.setting.GEMINI_MODEL,
                api_key=self.setting.GOOGLE_API_KEY,
                temperature=self.setting.LLM_TEMPERATURE,
            )

        if provider == LLMProvider.HUGGINGFACE:
            return HuggingFace(
                id=self.setting.HUGGINGFACE_MODEL,
                api_key=self.setting.HUGGINGFACE_API_KEY,
                temperature=self.setting.LLM_TEMPERATURE,
            )

        if provider == LLMProvider.AZURE:
            return AzureOpenAI(
                id=self.setting.AZURE_MODEL,
                api_key=self.setting.AZURE_API_KEY,
                azure_endpoint=self.setting.AZURE_ENDPOINT,
                azure_deployment=self.setting.AZURE_DEPLOYMENT,
                api_version=self.setting.AZURE_API_VERSION,
                temperature=self.setting.LLM_TEMPERATURE,
            )

        raise ValueError(f"Unsupported LLM provider: {provider}")
    
    def get_model(self):
        return self.model
