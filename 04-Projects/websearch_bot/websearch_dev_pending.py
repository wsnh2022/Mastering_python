import os

import httpx
from openrouter import OpenRouter

with OpenRouter(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    client=httpx.Client(timeout=90.0, follow_redirects=True),
    timeout_ms=90000,
) as client:
    response = client.chat.send(
        model="deepseek/deepseek-v4-flash",
        messages=[
            {
                "role": "user",
                "content": "provide the 26-07-2026 date temperature for india and for china. For each location, list the temperature along with the corresponding date and time in a separate lines in 10 words. ?",
            }
        ],
        tools=[
            {
                "type": "openrouter:web_search",
                "parameters": {
                    "engine": "exa",
                    "max_characters": 1500,
                    "max_total_results": 4,
                },
            }
        ],
    )
    print(response.choices[0].message.content)
