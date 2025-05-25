from unittest.mock import MagicMock

from pytest_mock import MockerFixture

from intent_classifier_llm_tools.services.azure_openai_service import (
    AzureOpenAIService,
)


def test_get_client(mocker: MockerFixture):
    patched_azure_openai = mocker.patch(
        "intent_classifier_llm_tools.services.azure_openai_service.AzureOpenAI",
        autospec=True,
    )
    svc = AzureOpenAIService(env=MagicMock())
    assert svc.get_client() is not None
    patched_azure_openai.assert_called_once()
