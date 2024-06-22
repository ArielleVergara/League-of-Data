from openai import OpenAI
import os

def get_chatgpt_response(data):
    try:
        client = OpenAI(
            api_key=os.environ.get(""),
        )

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": "Say this is a test",
                }
            ],
            model="gpt-3.5-turbo",
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        print(f"Error al obtener respuesta de OpenAI: {e}")
        return None