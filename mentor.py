from llm import llm

def explain_topic(topic):
    prompt = f"""
You are a DSA mentor for a beginner.

Explain the topic: {topic}

Rules:
- Simple language
- Step by step
- Small example
- When to use it
"""
    return llm.invoke(prompt).content


def generate_problem(topic):
    prompt = f"""
Give ONE {topic} LeetCode-style problem.

Return in this format:
Problem:
Example:
Constraints:
Follow-up:
"""
    return llm.invoke(prompt).content


def give_hint(problem):
    prompt = f"""
Give a small hint for this DSA problem without giving full solution:

{problem}
"""
    return llm.invoke(prompt).content


def evaluate_code(problem, code):
    prompt = f"""
You are a strict DSA interviewer.

Problem:
{problem}

User code:
{code}

Check:
- Is logic correct
- Time complexity
- Space complexity
- Edge cases missing
- Better optimal approach

Give verdict: Correct / Incorrect
"""
    return llm.invoke(prompt).content
