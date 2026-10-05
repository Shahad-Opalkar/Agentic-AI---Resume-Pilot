from ollama import chat
import json


def generate_response(prompt):

    response = chat(
        model="qwen2.5:3b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        format="json"
    )

    content = response["message"]["content"]

    return json.loads(content)