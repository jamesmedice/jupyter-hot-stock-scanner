# models.py

from enum import Enum

class Provider(str, Enum):
    OPENAI = "openai_compat"
    AZURE = "azure"


MODEL_REGISTRY = {
    "xai/grok-3-mini": {
        "provider": Provider.AZURE,
        "endpoint": "https://models.github.ai/inference",
        "env_key": "GITHUB_TOKEN"
    },
    "openai/gpt-4o-mini": {
        "provider": Provider.OPENAI,
        "endpoint": "https://models.github.ai/inference",
        "env_key": "GITHUB_TOKEN"
    },
    "microsoft/Phi-4-mini-reasoning": {
        "provider": Provider.AZURE,
        "endpoint": "https://models.github.ai/inference",
        "env_key": "GITHUB_TOKEN"
    },
    "meta/Meta-Llama-3.1-405B-Instruct": {
        "provider": Provider.AZURE,
        "endpoint": "https://models.github.ai/inference",
        "env_key": "GITHUB_TOKEN"
    },
}