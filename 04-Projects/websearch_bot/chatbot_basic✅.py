import os

from dotenv import load_dotenv
from openrouter import OpenRouter

load_dotenv()

client = OpenRouter(api_key=os.getenv("OPENROUTER_API_KEY"))


def ask(question: str) -> str:
    response = client.chat.send(
        model="deepseek/deepseek-v4-flash",
        messages=[{"role": "user", "content": question}],
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    question = input("Ask: ")
    print(ask(question))
