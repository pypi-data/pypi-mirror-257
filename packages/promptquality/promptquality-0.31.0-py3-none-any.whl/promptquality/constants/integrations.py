from enum import Enum


class IntegrationName(str, Enum):
    azure = "azure"
    openai = "openai"
