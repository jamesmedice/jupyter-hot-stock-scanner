# models.py

from enum import Enum

class Provider(str, Enum):
    OPENAI = "openai_compat"
    AZURE = "azure"


MODEL_REGISTRY = {
    "grok-3-mini": {
        "provider": Provider.OPENAI,
        "endpoint": "https://models.github.ai/inference"
    },
    "openai/gpt-4o-mini": {
        "provider": Provider.OPENAI,
        "endpoint": "https://models.github.ai/inference"
    },
    "microsoft/Phi-4": {
        "provider": Provider.AZURE,
        "endpoint": "https://models.github.ai/inference"
    },
    "meta/Meta-Llama-3.1-405B-Instruct": {
        "provider": Provider.AZURE,
        "endpoint": "https://models.github.ai/inference"
    },
    "cohere/cohere-command-a": {
        "provider": Provider.AZURE,
        "endpoint": "https://models.github.ai/inference"
    },
    "mistral-ai/mistral-small-2503": {
        "provider": Provider.AZURE,
        "endpoint": "https://models.github.ai/inference"
    },
    "microsoft/MAI-DS-R1": {
        "provider": Provider.AZURE,
        "endpoint": "https://models.github.ai/inference"
    },
}