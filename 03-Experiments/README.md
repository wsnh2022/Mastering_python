# Experiments

Temporary code and notebooks used for learning.
Safe place to test ideas before creating a real project.

## Reusable Dynamic Ai Prompt To generate beginner guide for any python library
```text
Teach me the [LIBRARY_NAME] library in Python using first principles and the
"outline before details" approach. I am a beginner in this specific library
(adjust my depth level as needed based on context).

Structure the response as follows:

PART 0 - First Principles
Explain the core problem this library solves and the mental model behind it,
before showing any code.

PART 1 - The Outline
Give me a table mapping out every major concept/feature in this library,
in the order I should learn them. This is the map - no code yet.

PART 2+ - One Section Per Concept
For each concept in the outline:
- Explain what it does and why it exists
- Give a minimal, runnable code example
- Add clear notes below the code explaining each non-obvious line/argument
- Point out common beginner mistakes for that specific feature
- Keep code and explanation balanced - don't over-explain trivial lines,
  don't under-explain tricky ones

PART N - Putting It Together
One realistic, slightly larger example that combines multiple concepts from
above into something practically useful (tailored to [USE_CASE] if I specify one).

PART N+1 - Free Resources
List free resources to practice with:
- Official docs link
- Free sandbox/testing tools or APIs/datasets relevant to this library
- 1-2 well-regarded free tutorials or articles
- Any free interactive practice platforms if relevant

PART N+2 - Practical Next Steps
Give me 4-5 concrete hands-on exercises, ordered from easiest to hardest,
that would build real skill with this library - not just reading comprehension.

Rules:
- Use markdown formatting with headings and tables
- Every code sample must be runnable, not pseudocode
- Explain technical terms briefly the first time they appear
- Don't pad simple concepts with unnecessary depth
- Flag anything that's version-specific or has changed recently, if relevant
```
