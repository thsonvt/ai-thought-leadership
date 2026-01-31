#!/usr/bin/env python3
"""
Diátaxis Classifier - Classifies articles by documentation type
Types: tutorial, how-to, reference, explanation
"""

import os
from openai import OpenAI
from pathlib import Path

# Load environment variables from .env file
try:
    from load_env import load_env
    load_env()
except ImportError:
    pass

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Diátaxis type definitions for the prompt
DIATAXIS_DEFINITIONS = """
The Diátaxis framework defines four types of documentation:

1. TUTORIAL (learning-oriented)
   - Teaches beginners through hands-on lessons
   - "Follow along to learn X"
   - Step-by-step, building toward a goal
   - Focus: learning by doing

2. HOW-TO (task-oriented)
   - Solves a specific problem
   - "How to achieve X"
   - Assumes some knowledge
   - Focus: accomplishing a goal

3. REFERENCE (information-oriented)
   - Describes the machinery
   - Technical specifications, API docs
   - Dry, accurate, complete
   - Focus: providing facts

4. EXPLANATION (understanding-oriented)
   - Explains concepts and context
   - "Why X works this way"
   - Discusses background, alternatives, trade-offs
   - Focus: providing understanding
"""


def classify_article(title: str, content: str, author: str = None) -> str:
    """
    Classify an article by Diátaxis type.

    Args:
        title: Article title
        content: Article content (will be truncated if too long)
        author: Optional author name for context

    Returns:
        One of: 'tutorial', 'how-to', 'reference', 'explanation'
    """
    # Truncate content if too long
    max_content_length = 3000
    if len(content) > max_content_length:
        content = content[:max_content_length] + "\n\n[Content truncated...]"

    prompt = f"""{DIATAXIS_DEFINITIONS}

Analyze this article and classify it into ONE Diátaxis type.

**Article Title:** {title}
{f"**Author:** {author}" if author else ""}

**Content Preview:**
{content}

**Instructions:**
1. Consider the article's primary PURPOSE (teaching, solving, describing, explaining)
2. Look at the structure and tone
3. Choose the BEST fit - most articles lean toward one type

**Respond with ONLY one word:** tutorial, how-to, reference, or explanation
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert at classifying technical content using the Diátaxis framework. Respond with exactly one word."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.1,
            max_tokens=10
        )

        result = response.choices[0].message.content.strip().lower()

        # Validate the result
        valid_types = ['tutorial', 'how-to', 'reference', 'explanation']
        if result in valid_types:
            return result

        # Handle edge cases (e.g., "how to" vs "how-to")
        if result in ['howto', 'how to', 'how-to guide']:
            return 'how-to'

        # Default to explanation if unclear
        print(f"    Warning: Unexpected classification '{result}', defaulting to 'explanation'")
        return 'explanation'

    except Exception as e:
        print(f"    Error classifying article: {e}")
        return 'explanation'  # Default fallback


def test_classifier():
    """Test the classifier with sample content"""
    test_cases = [
        {
            "title": "Building Your First Claude Code Agent",
            "content": "In this tutorial, we'll walk through creating your first AI agent step by step. First, install the SDK. Then, create a new file...",
            "expected": "tutorial"
        },
        {
            "title": "How to Fix Memory Leaks in Python",
            "content": "If you're experiencing memory issues, here's how to diagnose and fix them. Step 1: Use memory_profiler...",
            "expected": "how-to"
        },
        {
            "title": "Claude API Reference",
            "content": "POST /v1/messages. Parameters: model (string, required), messages (array, required), max_tokens (integer)...",
            "expected": "reference"
        },
        {
            "title": "Why AI Agents Need Better Context Management",
            "content": "The challenge with AI agents isn't the models themselves, but how we manage context. Let me explain why this matters...",
            "expected": "explanation"
        }
    ]

    print("Testing Diátaxis classifier...")
    print("-" * 50)

    for test in test_cases:
        result = classify_article(test["title"], test["content"])
        status = "✅" if result == test["expected"] else "❌"
        print(f"{status} '{test['title'][:40]}...'")
        print(f"   Expected: {test['expected']}, Got: {result}")

    print("-" * 50)


if __name__ == '__main__':
    if os.getenv('OPENAI_API_KEY'):
        test_classifier()
    else:
        print("Set OPENAI_API_KEY to test the classifier")
