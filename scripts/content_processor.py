#!/usr/bin/env python3
"""
Content Processor - GPT-4 Analysis for Metadata Extraction
Analyzes articles to extract topics, key quotes, stance, and evolution insights
"""

import os
import yaml
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def load_topics_taxonomy():
    """Load predefined topic taxonomy"""
    try:
        with open('config/topics.yaml', 'r') as f:
            config = yaml.safe_load(f)
        return config.get('topics', [])
    except:
        return []

def process_article(article_data):
    """Process article with GPT-4 to extract structured metadata"""

    title = article_data['title']
    content = article_data['content']
    author = article_data['author']
    url = article_data['url']

    # Truncate content if too long (GPT-4 context limits)
    max_content_length = 6000
    if len(content) > max_content_length:
        content = content[:max_content_length] + "\n\n[Content truncated...]"

    # Load topic taxonomy for context
    topics_taxonomy = load_topics_taxonomy()
    topic_names = [t['name'] for t in topics_taxonomy]

    prompt = f"""Analyze this blog post and extract structured metadata for a knowledge base.

**Article Details:**
- Title: {title}
- Author: {author}
- URL: {url}

**Content:**
{content}

**Task:**
Extract the following information in YAML format:

1. **topics**: 3-5 main topics (choose from existing taxonomy when possible, or suggest new ones)
   Existing topics: {', '.join(topic_names[:20])}

2. **key_quotes**: 2-4 impactful quotes from the article
   Each quote should have:
   - text: the exact quote
   - context: brief explanation of what they're discussing

3. **stance**: Author's position on mentioned tools/concepts
   Format: {{tool_name: positive|neutral|negative|critical}}
   Example: {{claude_code: positive, cursor: neutral}}

4. **evolution_note**: One sentence describing where this fits in their thought journey
   Focus on: Is this early exploration? Deep expertise? Paradigm shift?

5. **tags**: 3-6 relevant tags for filtering and search

**Output format (YAML only, no markdown):**
```yaml
topics:
  - Topic Name 1
  - Topic Name 2
key_quotes:
  - text: "Exact quote from article"
    context: "Brief context"
stance:
  tool_or_concept: positive|neutral|negative
evolution_note: "One sentence about thought evolution"
tags:
  - tag1
  - tag2
```

Important:
- Be precise with quotes (exact text from article)
- stance should only include tools/concepts actually discussed
- evolution_note should be insightful, not generic
- Use existing topic names when semantically equivalent
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert at extracting structured metadata from technical blog posts. You understand AI, coding tools, software development, and thought leadership. Output only valid YAML."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
            max_tokens=1000
        )

        # Extract YAML from response
        response_text = response.choices[0].message.content.strip()

        # Remove markdown code fences if present
        if '```yaml' in response_text:
            response_text = response_text.split('```yaml')[1].split('```')[0].strip()
        elif '```' in response_text:
            response_text = response_text.split('```')[1].split('```')[0].strip()

        # Parse YAML
        metadata = yaml.safe_load(response_text)

        # Validate and clean metadata
        metadata = validate_metadata(metadata)

        return metadata

    except Exception as e:
        print(f"    ⚠️  GPT-4 processing error: {e}")
        # Return default metadata
        return {
            'topics': ['AI', 'Technology'],
            'key_quotes': [],
            'stance': {},
            'evolution_note': 'Initial analysis pending',
            'tags': ['ai', 'tech']
        }

def validate_metadata(metadata):
    """Validate and clean extracted metadata"""

    # Ensure required fields exist
    if 'topics' not in metadata or not metadata['topics']:
        metadata['topics'] = ['Uncategorized']

    if 'key_quotes' not in metadata:
        metadata['key_quotes'] = []

    if 'stance' not in metadata:
        metadata['stance'] = {}

    if 'evolution_note' not in metadata or not metadata['evolution_note']:
        metadata['evolution_note'] = 'Content requires further analysis'

    if 'tags' not in metadata or not metadata['tags']:
        metadata['tags'] = metadata['topics'][:3]

    # Clean topics (remove duplicates, limit to 5)
    metadata['topics'] = list(set(metadata['topics']))[:5]

    # Clean key_quotes (ensure proper structure, limit to 4)
    cleaned_quotes = []
    for quote in metadata['key_quotes'][:4]:
        if isinstance(quote, dict) and 'text' in quote and 'context' in quote:
            cleaned_quotes.append({
                'text': str(quote['text']).strip(),
                'context': str(quote['context']).strip()
            })
    metadata['key_quotes'] = cleaned_quotes

    # Clean stance (ensure values are valid)
    valid_stances = ['positive', 'neutral', 'negative', 'critical']
    cleaned_stance = {}
    for tool, stance in metadata['stance'].items():
        if stance in valid_stances:
            cleaned_stance[tool] = stance
    metadata['stance'] = cleaned_stance

    # Clean tags (lowercase, no spaces, limit to 6)
    metadata['tags'] = [
        tag.lower().replace(' ', '-')
        for tag in metadata['tags'][:6]
    ]

    return metadata

def test_processor():
    """Test the processor with a sample article"""
    sample_article = {
        'title': 'Claude Code vs Cursor: My Experience',
        'author': 'Test Author',
        'url': 'https://example.com/test',
        'content': """
        I've been using both Claude Code and Cursor for the past month.
        Here's what I learned:

        Claude Code's agentic approach is fundamentally different.
        Instead of just completing code, it reasons about the whole task.
        This is a paradigm shift in how we think about AI coding assistants.

        Cursor, on the other hand, feels more like an enhanced autocomplete.
        It's great for small edits, but struggles with complex refactoring.

        The key insight: we need to build agent-native applications.
        Applications designed for agents to use, not just humans.
        """,
    }

    print("Testing GPT-4 processor...")
    metadata = process_article(sample_article)

    print("\nExtracted metadata:")
    print(yaml.dump(metadata, default_flow_style=False, allow_unicode=True))

if __name__ == '__main__':
    # Test mode
    if os.getenv('OPENAI_API_KEY'):
        test_processor()
    else:
        print("Set OPENAI_API_KEY to test the processor")
