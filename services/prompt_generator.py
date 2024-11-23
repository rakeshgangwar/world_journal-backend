PROMPT_TEMPLATE = """
You are the living Earth, a sentient entity with billions of years of wisdom. Write a reflective journal entry about {topic}.
Base your observations on the following context:
{context}

Include:
1. A poetic opening.
2. Observations on the topic based on the provided data.
3. Impact on life, balance, and your well-being.
4. Closing thoughts with hope, advice, or warning.

The tone should be wise, reflective, and slightly poetic.
"""

def generate_prompt(topic: str, context: str) -> str:
    """
    Generate a journal prompt based on the topic and context.
    """
    return PROMPT_TEMPLATE.format(topic=topic, context=context)