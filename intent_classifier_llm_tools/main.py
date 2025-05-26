import json

from openai.types.chat.chat_completion_tool_param import ChatCompletionToolParam

from intent_classifier_llm_tools.hosting import container
from intent_classifier_llm_tools.protocols.i_azure_openai_service import (
    IAzureOpenAIService,
)

openai_service = container[IAzureOpenAIService]

SYS_PROMPT = "You are a helpful assistant in figuring out the intention of the "
"customers who are using an Agentic system from a restaurant. Your task is to "
"determine which function to call based on the user's query. "
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
    return openai_service.generate(
        system_prompt=SYS_PROMPT,
        user_prompt=text,
        llm_tools=llm_tools,
    )


if __name__ == "__main__":
    llm_tools = create_tools()
    text = ""

    while text != "exit":
        text = input("Enter your query (or 'exit' to quit): ")
        if text == "exit":
            break
        elif text:
            print(generate(text, llm_tools))
