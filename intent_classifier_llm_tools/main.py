import json
import os

from openai.types.chat.chat_completion_message_param import ChatCompletionMessageParam
from openai.types.chat.chat_completion_tool_param import ChatCompletionToolParam

from intent_classifier_llm_tools.hosting import container
from intent_classifier_llm_tools.protocols.i_azure_openai_service import (
    IAzureOpenAIService,
)

llm_client = container[IAzureOpenAIService].get_client()
llm_deployment_name = os.getenv("AZURE_OPENAI_LLM_MODEL", "")

SYS_PROMPT = "Your primary goal is to route the user query to the correct agent. "
"Default to 'none' if the input seems unclear. You should always "
"answer with one or more functions, never try to answer the query yourself."


def create_tools() -> list[ChatCompletionToolParam]:
    with open("tool_definitions.json", "r") as f:
        definitions = json.load(f)
        return [
            {
                "type": "function",
                "function": {
                    "name": k,
                    "description": v,
                    "parameters": {"type": "object", "properties": {}},
                },
            }
            for k, v in definitions.items()
        ]


def generate(text: str, llm_tools: list[ChatCompletionToolParam]) -> list[str]:
    messages: list[ChatCompletionMessageParam] = [
        {"role": "system", "content": SYS_PROMPT},
        {"role": "user", "content": text},
    ]
    response = llm_client.chat.completions.create(
        model=llm_deployment_name,
        messages=messages,
        tools=llm_tools,
        tool_choice="auto",
        # **ExperimentParameters().llm_parameters(),
    )
    message = response.choices[0].message
    tool_calls = message.tool_calls

    return [tool_call.function.name for tool_call in tool_calls] if tool_calls else []


if __name__ == "__main__":
    llm_tools = create_tools()
    text = ""

    while text != "exit":
        text = input("Enter your query (or 'exit' to quit): ")
        if text == "exit":
            break
        elif text:
            print(generate(text, llm_tools))
