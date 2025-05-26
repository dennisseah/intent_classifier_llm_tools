from unittest.mock import MagicMock

from openai.types.chat.chat_completion_message_tool_call import (
    ChatCompletionMessageToolCall,
)
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


def test_generate(mocker: MockerFixture):
    mock_llm_client = MagicMock()
    tool_call_1 = MagicMock(spec=ChatCompletionMessageToolCall)
    tool_call_1.function = MagicMock()
    tool_call_1.function.name = "tool1"
    tool_call_2 = MagicMock(spec=ChatCompletionMessageToolCall)
    tool_call_2.function = MagicMock()
    tool_call_2.function.name = "tool2"

    mock_llm_client.chat.completions.create.return_value.choices = [
        MagicMock(message=MagicMock(tool_calls=[tool_call_1, tool_call_2]))
    ]
    svc = AzureOpenAIService(env=MagicMock(), llm_client=mock_llm_client)
    result = svc.generate(
        system_prompt="Test system prompt",
        user_prompt="Test user prompt",
        llm_tools=[
            {"type": "function", "function": {"name": "tool1", "description": "desc1"}},
            {"type": "function", "function": {"name": "tool2", "description": "desc2"}},
        ],
    )

    assert result == ["tool1", "tool2"]
