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
    "microsoft/Phi-4-mini-reasoning": {
        "provider": Provider.AZURE,
        "endpoint": "https://models.github.ai/inference"
    },
    "meta/Meta-Llama-3.1-405B-Instruct": {
        "provider": Provider.AZURE,
        "endpoint": "https://models.github.ai/inference"
    },
}