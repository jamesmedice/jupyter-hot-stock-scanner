from azure.ai.inference.models import SystemMessage, UserMessage
from models import MODEL_REGISTRY, Provider


def convert_to_azure_messages(messages):

    azure_messages = []

    for m in messages:

        if m["role"] == "system":
            azure_messages.append(SystemMessage(m["content"]))

        elif m["role"] == "user":
            azure_messages.append(UserMessage(m["content"]))

    return azure_messages


def get_response(model: str, client, messages):

    if model not in MODEL_REGISTRY:
        raise ValueError(f"Unknown model: {model}")

    config = MODEL_REGISTRY[model]
    provider = config["provider"]

    if provider == Provider.OPENAI_COMPAT:

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

    raise ValueError(f"Unsupported provider: {provider}")