from azure.ai.inference.models import SystemMessage, UserMessage 

def convert_to_azure_messages(messages):

    azure_messages = []

    for m in messages:

        if m["role"] == "system":
            azure_messages.append(SystemMessage(m["content"]))

        elif m["role"] == "user":
            azure_messages.append(UserMessage(m["content"]))

    return azure_messages