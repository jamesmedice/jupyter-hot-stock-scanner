from mistralai import Mistral, UserMessage, SystemMessage

def convert_to_mistral_messages(messages):

    mistral_messages = []

    for m in messages:

        if m["role"] == "system":
            mistral_messages.append(SystemMessage(m["content"]))

        elif m["role"] == "user":
            mistral_messages.append(UserMessage(m["content"]))

    return mistral_messages