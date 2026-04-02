from azure.ai.inference.models import SystemMessage, UserMessage
from models import MODEL_REGISTRY, Provider

from azure_message import convert_to_azure_messages
from mistral_message import convert_to_mistral_messages

def get_response(model: str, client, messages):

    if model not in MODEL_REGISTRY:
        raise ValueError(f"Unknown model: {model}")

    config = MODEL_REGISTRY[model]
    provider = config["provider"]

    if provider == Provider.OPENAI:

        response = client.chat.completions.create(
            model=model,
            temperature=0.2,
            messages=messages
        )

        return response.choices[0].message.content

    if provider == Provider.AZURE:

        azure_messages = convert_to_azure_messages(messages)

        response = client.complete(
            model=model,
            messages=azure_messages,
            temperature=0.2,
            max_tokens=1000
        )

        return response.choices[0].message.content

    if provider == Provider.MISTRAL:

        mistral_messages = convert_to_mistral_messages(messages)

        response = client.chat.complete(
            model=model,
            messages=mistral_messages,
            temperature=0.2,
            max_tokens=1000,
            top_p=1.0
        )

        return response.choices[0].message.content

    raise ValueError(f"Unsupported provider: {provider}")