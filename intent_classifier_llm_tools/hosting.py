"""Defines our top level DI container.
Utilizes the Lagom library for dependency injection, see more at:

- https://lagom-di.readthedocs.io/en/latest/
- https://github.com/meadsteve/lagom
"""

import logging

from dotenv import load_dotenv
from lagom import Container, dependency_definition

from intent_classifier_llm_tools.protocols.i_azure_openai_service import (
    IAzureOpenAIService,
)

load_dotenv()


container = Container()
"""The top level DI container for our application."""


# Register our dependencies ------------------------------------------------------------


@dependency_definition(container, singleton=True)
def _() -> logging.Logger:
    return logging.getLogger("intent_classifier_llm_tools")


@dependency_definition(container)
def _(c: Container) -> IAzureOpenAIService:
    from intent_classifier_llm_tools.services.azure_openai_service import (
        AzureOpenAIService,
    )

    return c[AzureOpenAIService]
