from typing import Protocol

from openai import AzureOpenAI


class IAzureOpenAIService(Protocol):
    """
    IAzureOpenAIService is a protocol that defines the interface for
    Azure OpenAI service classes. It includes a method to get a
    generative model with specified parameters.
    """

    def get_client(self) -> AzureOpenAI:
        """
        Get a small generative model from Azure OpenAI service.

        :return: An instance of AzureOpenAI.
        """
        ...
