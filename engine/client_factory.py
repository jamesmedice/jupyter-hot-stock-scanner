# client_factory.py

import os
from openai import OpenAI
from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential

from models import MODEL_REGISTRY, Provider


def get_client(model: str):

    if model not in MODEL_REGISTRY:
        raise ValueError(f"Unknown model: {model}")

    config = MODEL_REGISTRY[model]
    provider = config["provider"]
    endpoint = config["endpoint"]
    #token = os.environ[config["env_key"]]
    token = os.environ["GITHUB_TOKEN"],

    if provider == Provider.OPENAI_COMPAT:
        return OpenAI(
            base_url=endpoint,
            api_key=token,
        )

    if provider == Provider.AZURE:
        return ChatCompletionsClient(
            endpoint=endpoint,
            credential=AzureKeyCredential(token),
        )

    raise ValueError(f"Unsupported provider: {provider}")