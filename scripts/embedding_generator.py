#!/usr/bin/env python3
"""
Embedding Generator - Creates vector embeddings for semantic search
Uses OpenAI's text-embedding-3-small model (1536 dimensions)
"""

import os
from openai import OpenAI
from typing import List, Optional

# Load environment variables from .env file
try:
    from load_env import load_env
    load_env()
except ImportError:
    pass

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Model configuration
EMBEDDING_MODEL = "text-embedding-3-small"
EMBEDDING_DIMENSIONS = 1536
MAX_TOKENS = 8000  # text-embedding-3-small supports 8191 tokens


def generate_embedding(text: str) -> Optional[List[float]]:
    """
    Generate an embedding vector for the given text.

    Args:
        text: The text to embed (will be truncated if too long)

    Returns:
        List of 1536 floats representing the embedding, or None on error
    """
    if not text or not text.strip():
        print("    Warning: Empty text provided for embedding")
        return None

    # Truncate if too long (rough estimate: 1 token ≈ 4 chars)
    max_chars = MAX_TOKENS * 4
    if len(text) > max_chars:
        text = text[:max_chars]

    try:
        response = client.embeddings.create(
            model=EMBEDDING_MODEL,
            input=text,
            dimensions=EMBEDDING_DIMENSIONS
        )
        return response.data[0].embedding

    except Exception as e:
        print(f"    Error generating embedding: {e}")
        return None


def generate_article_embedding(
    title: str,
    content: str,
    summary: Optional[str] = None,
    topics: Optional[List[str]] = None,
    key_quotes: Optional[List[dict]] = None
) -> Optional[List[float]]:
    """
    Generate an embedding for an article, combining multiple fields
    for richer semantic representation.

    Args:
        title: Article title
        content: Article content
        summary: Optional GPT-4 generated summary
        topics: Optional list of topics
        key_quotes: Optional list of key quotes

    Returns:
        List of 1536 floats representing the embedding
    """
    # Build a rich text representation for embedding
    parts = [f"Title: {title}"]

    if summary:
        parts.append(f"Summary: {summary}")

    if topics:
        parts.append(f"Topics: {', '.join(topics)}")

    if key_quotes:
        quotes_text = " | ".join([q.get('text', '') for q in key_quotes[:3]])
        parts.append(f"Key quotes: {quotes_text}")

    # Add content (will be truncated if combined text is too long)
    parts.append(f"Content: {content}")

    combined_text = "\n\n".join(parts)

    return generate_embedding(combined_text)


def batch_generate_embeddings(texts: List[str]) -> List[Optional[List[float]]]:
    """
    Generate embeddings for multiple texts in a single API call.

    Args:
        texts: List of texts to embed

    Returns:
        List of embeddings (same order as input)
    """
    if not texts:
        return []

    # Filter out empty texts and track indices
    valid_indices = []
    valid_texts = []
    for i, text in enumerate(texts):
        if text and text.strip():
            valid_indices.append(i)
            # Truncate if needed
            max_chars = MAX_TOKENS * 4
            valid_texts.append(text[:max_chars] if len(text) > max_chars else text)

    if not valid_texts:
        return [None] * len(texts)

    try:
        response = client.embeddings.create(
            model=EMBEDDING_MODEL,
            input=valid_texts,
            dimensions=EMBEDDING_DIMENSIONS
        )

        # Map results back to original indices
        results = [None] * len(texts)
        for i, embedding_data in enumerate(response.data):
            original_index = valid_indices[i]
            results[original_index] = embedding_data.embedding

        return results

    except Exception as e:
        print(f"    Error in batch embedding: {e}")
        return [None] * len(texts)


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """
    Calculate cosine similarity between two vectors.

    Args:
        vec1: First vector
        vec2: Second vector

    Returns:
        Cosine similarity score (0-1, higher = more similar)
    """
    import math

    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    magnitude1 = math.sqrt(sum(a * a for a in vec1))
    magnitude2 = math.sqrt(sum(b * b for b in vec2))

    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0

    return dot_product / (magnitude1 * magnitude2)


def test_embeddings():
    """Test embedding generation and similarity"""
    print("Testing embedding generator...")
    print("-" * 50)

    # Test basic embedding
    text1 = "Claude Code is an AI coding assistant that helps developers write better code."
    embedding1 = generate_embedding(text1)
    print(f"✅ Generated embedding: {len(embedding1)} dimensions")

    # Test similar text
    text2 = "AI assistants like Claude help programmers be more productive."
    embedding2 = generate_embedding(text2)

    # Test dissimilar text
    text3 = "The weather in Paris is beautiful in spring."
    embedding3 = generate_embedding(text3)

    # Calculate similarities
    sim_1_2 = cosine_similarity(embedding1, embedding2)
    sim_1_3 = cosine_similarity(embedding1, embedding3)

    print(f"\nSimilarity tests:")
    print(f"  'AI coding' vs 'AI assistants': {sim_1_2:.3f} (should be high)")
    print(f"  'AI coding' vs 'Paris weather': {sim_1_3:.3f} (should be low)")

    # Test article embedding
    article_embedding = generate_article_embedding(
        title="Building AI Agents",
        content="This article explains how to build AI agents using the latest tools...",
        summary="A guide to AI agent development",
        topics=["AI Agents", "Development"],
        key_quotes=[{"text": "Agents are the future of AI", "context": "Introduction"}]
    )
    print(f"\n✅ Article embedding: {len(article_embedding)} dimensions")

    print("-" * 50)


if __name__ == '__main__':
    if os.getenv('OPENAI_API_KEY'):
        test_embeddings()
    else:
        print("Set OPENAI_API_KEY to test the embedding generator")
