from typing import Callable

from azure.identity import DefaultAzureCredential, get_bearer_token_provider


def get_openai_auth_key(api_key: str | None) -> dict[str, str | Callable[[], str]]:
    """
    Get the OpenAI API key from the environment variables.

    :param api_key: The OpenAI API key. If None, it will use Azure AD token provider.
    :return: Dictionary containing the OpenAI API key.
    """
    if api_key:
        return {"api_key": api_key}

    token_provider = get_bearer_token_provider(
        DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
    )
    return {"azure_ad_token_provider": token_provider}
