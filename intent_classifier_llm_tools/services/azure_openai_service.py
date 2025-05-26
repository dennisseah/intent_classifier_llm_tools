from dataclasses import dataclass

from lagom.environment import Env
from openai import AzureOpenAI
from openai.types.chat.chat_completion_message_param import ChatCompletionMessageParam
from openai.types.chat.chat_completion_tool_param import ChatCompletionToolParam

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
    azure_openai_llm_model: str
    azure_openai_api_key: str | None = None


@dataclass
class AzureOpenAIService(IAzureOpenAIService):
    env: AzureOpenAIServiceEnv
    llm_client: AzureOpenAI | None = None

    def get_client(self) -> AzureOpenAI:
        if self.llm_client is not None:
            return self.llm_client
        self.llm_client = AzureOpenAI(
            azure_endpoint=self.env.azure_openai_endpoint,
            api_version=self.env.azure_openai_api_version,
            **get_openai_auth_key(self.env.azure_openai_api_key),  # type: ignore
        )
        return self.llm_client

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        llm_tools: list[ChatCompletionToolParam],
    ) -> list[str]:
        messages: list[ChatCompletionMessageParam] = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        llm_client = self.get_client()
        response = llm_client.chat.completions.create(
            model=self.env.azure_openai_llm_model,
            messages=messages,
            tools=llm_tools,
            tool_choice="auto",
        )
        message = response.choices[0].message
        tool_calls = message.tool_calls

        return (
            [tool_call.function.name for tool_call in tool_calls] if tool_calls else []
        )
