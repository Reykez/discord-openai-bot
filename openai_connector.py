from openai import OpenAI
from settings import openai_token

client = OpenAI(
    api_key=openai_token
)


# Map conversation list into messages list that will be used in OpenAI API request.
def map_conversation(conversation: list, userMessage: str) -> list:
    messages = []
    for dialog in conversation:
        messages.append({
            "role": "user",
            "content": dialog["message"]
        })
        messages.append({
            "role": "assistant",
            "content": dialog["response"]
        })
    messages.append({
        "role": "user",
        "content": userMessage
    })
    return messages


# Send request to OpenAI and get response message content.
def get_chat_response(messages: list) -> str:
    print('CHATGPT MESSAGE: ', messages)

    completion = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
    )

    print('Returned content: ', completion.choices)
    return completion.choices[-1].message.content
