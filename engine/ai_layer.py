import os
import json
from openai import OpenAI
from client_factory import get_client
from builder import build_messages
from response_router import get_response

def ask_ai(candidates, model, items=10):

    client = get_client(model)

    payload = json.dumps(candidates, indent=2)

    print(f"Payload sent to AI:\n{payload}")

    messages = build_messages(payload, items)

    result = get_response(model, client, messages)

    return result