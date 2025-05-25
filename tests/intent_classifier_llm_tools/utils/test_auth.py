from typing import Callable

from pytest_mock import MockerFixture

from intent_classifier_llm_tools.utils.auth import get_openai_auth_key


def test_get_openai_auth_key():
    # Test with a valid API key
    api_key = "test_api_key"
    auth_key = get_openai_auth_key(api_key)
    assert auth_key == {"api_key": api_key}


def test_get_openai_auth_key_none(mocker: MockerFixture):
    patch_token = mocker.patch(
        "intent_classifier_llm_tools.utils.auth.DefaultAzureCredential"
    )
    patch_func = mocker.patch(
        "intent_classifier_llm_tools.utils.auth.get_bearer_token_provider"
    )
    auth_key = get_openai_auth_key(None)
    assert "azure_ad_token_provider" in auth_key
    assert isinstance(auth_key["azure_ad_token_provider"], Callable)
    patch_token.assert_called_once()
    patch_func.assert_called_once()
