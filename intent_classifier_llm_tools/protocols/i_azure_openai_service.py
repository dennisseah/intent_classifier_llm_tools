from typing import Protocol

from openai.types.chat.chat_completion_tool_param import ChatCompletionToolParam


class IAzureOpenAIService(Protocol):
    """
    IAzureOpenAIService is a protocol that defines the interface for
    Azure OpenAI service classes. It includes a method to get a
    generative model with specified parameters.
    """

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        llm_tools: list[ChatCompletionToolParam],
    ) -> list[str]:
        """
        Generates a response from the Azure OpenAI service based on the
        provided system prompt, user prompt, and tools.

        :param system_prompt: The system prompt to guide the model's behavior.
        :param user_prompt: The user's input to the model.
        :param llm_tools: A list of tools that the model can use to assist
            in generating the response.
        :return: A list of strings representing the model's tool call function names.
        """
        ...
