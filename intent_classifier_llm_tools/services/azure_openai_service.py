from dataclasses import dataclass

from lagom.environment import Env
from openai import AzureOpenAI

from intent_classifier_llm_tools.protocols.i_azure_openai_service import (
    IAzureOpenAIService,
)
from intent_classifier_llm_tools.utils.auth import get_openai_auth_key


class AzureOpenAIServiceEnv(Env):
    """
    Environment variables for Azure OpenAI Service.
    """

    azure_openai_endpoint: str
    azure_openai_api_version: str
    azure_openai_api_key: str | None = None


@dataclass
class AzureOpenAIService(IAzureOpenAIService):
    env: AzureOpenAIServiceEnv

    def get_client(self) -> AzureOpenAI:
        return AzureOpenAI(
            azure_endpoint=self.env.azure_openai_endpoint,
            api_version=self.env.azure_openai_api_version,
            **get_openai_auth_key(self.env.azure_openai_api_key),  # type: ignore
        )
