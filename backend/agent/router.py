from llm import generate_response

def classify_task(user_query):
    prompt = f"""
You are a routing agent.

You MUST return exactly one of these words:

ats
skills
rewrite
interview

User request:
{user_query}

Return ONLY one word.
No explanation.
No punctuation.
No extra text.
"""

    return generate_response(prompt).strip().lower()