import os
import sys

from dotenv import load_dotenv
from pydantic_ai import Agent

# Load .env
load_dotenv()


# Check API key
if not os.getenv("OPENROUTER_API_KEY"):
    print("Error: OPENROUTER_API_KEY is missing.")
    sys.exit(1)


# Create AI agent
agent = Agent(
    "openrouter:deepseek/deepseek-v4-flash-0731", model_settings={"max_tokens": 3000}
)


def ask_ai(prompt):
    """Send prompt to AI and return the answer."""

    if not prompt.strip():
        raise ValueError("Prompt cannot be empty.")

    try:
        result = agent.run_sync(prompt)

        if not result.output:
            raise ValueError("AI returned an empty response.")

        return result.output.strip()

    except Exception as error:
        raise RuntimeError(f"AI request failed: {error}") from error


# Get query from terminal
if len(sys.argv) < 2:
    print('Usage: python aci.py "your question"')
    sys.exit(1)

user_query = " ".join(sys.argv[1:])


# 1. GENERATE
answer = ask_ai(
    f"""
Answer this question for a beginner:

{user_query}
"""
)

print("\nGENERATED:")
print(answer)


# 2. CRITIQUE
critique = ask_ai(
    f"""
Review this answer for a beginner.

ANSWER:
{answer}

Give a short critique.
Identify what should be improved.
"""
)

print("\nCRITIQUE:")
print(critique)


# 3. IMPROVE
improved = ask_ai(
    f"""
Improve the original answer using the critique.

ORIGINAL:
{answer}

CRITIQUE:
{critique}

Return only the improved answer.
"""
)

print("\nIMPROVED:")
print(improved)

# 4. SAVE TO MARKDOWN
filename = user_query.lower().replace(" ", "_") + ".md"

with open(filename, "w", encoding="utf-8") as file:
    file.write(f"# {user_query}\n\n")
    file.write(improved)

print(f"\nSaved to: {filename}")
