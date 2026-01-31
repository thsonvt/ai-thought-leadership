#!/usr/bin/env python3
"""
Supabase Sync - Syncs articles from markdown files to Supabase database
Handles embedding generation and Diátaxis classification
"""

import os
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any

import frontmatter
from supabase import create_client, Client

# Load environment variables from .env file
try:
    from load_env import load_env
    load_env()
except ImportError:
    pass

from diataxis_classifier import classify_article
from embedding_generator import generate_article_embedding

# Get project root directory
PROJECT_ROOT = Path(__file__).parent.parent

# Initialize Supabase client
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_ANON_KEY')

supabase: Optional[Client] = None
if SUPABASE_URL and SUPABASE_KEY:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def get_url_hash(url: str) -> str:
    """Generate MD5 hash of URL (first 8 chars)"""
    return hashlib.md5(url.encode()).hexdigest()[:8]


def parse_markdown_file(filepath: Path) -> Optional[Dict[str, Any]]:
    """
    Parse a markdown file and extract article data.

    Args:
        filepath: Path to the markdown file

    Returns:
        Dictionary with article data, or None on error
    """
    try:
        post = frontmatter.load(filepath)

        # Extract frontmatter
        fm = post.metadata

        # Get content (everything after frontmatter)
        content = post.content

        return {
            'title': fm.get('title', 'Untitled'),
            'author': fm.get('author', 'Unknown'),
            'author_id': fm.get('author_id', 'unknown'),
            'url': fm.get('url', ''),
            'published': fm.get('published'),
            'fetched': fm.get('fetched'),
            'topics': fm.get('topics', []),
            'key_quotes': fm.get('key_quotes', []),
            'stance': fm.get('stance', {}),
            'evolution_note': fm.get('evolution_note', ''),
            'tags': fm.get('tags', []),
            'content': content,
            'filepath': str(filepath)
        }

    except Exception as e:
        print(f"  Error parsing {filepath}: {e}")
        return None


def generate_summary(title: str, content: str, key_quotes: List[dict]) -> str:
    """Generate a brief summary from article data"""
    # For now, use a simple extraction approach
    # Could be enhanced with GPT-4 later
    summary_parts = []

    # Use first key quote if available
    if key_quotes and key_quotes[0].get('text'):
        summary_parts.append(key_quotes[0]['text'][:200])

    # Use first paragraph of content
    paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
    for p in paragraphs:
        # Skip headers and metadata lines
        if not p.startswith('#') and not p.startswith('**') and len(p) > 50:
            summary_parts.append(p[:300])
            break

    return ' '.join(summary_parts)[:500] if summary_parts else title


def sync_article_to_supabase(article: Dict[str, Any], force_update: bool = False) -> bool:
    """
    Sync a single article to Supabase.

    Args:
        article: Article data dictionary
        force_update: If True, update even if article exists

    Returns:
        True if synced successfully, False otherwise
    """
    if not supabase:
        print("  Error: Supabase client not initialized")
        return False

    url = article.get('url', '')
    if not url:
        print("  Error: Article has no URL")
        return False

    url_hash = get_url_hash(url)
    title = article.get('title', 'Untitled')

    # Check if article exists
    existing = supabase.table('articles').select('id, embedding').eq('url', url).execute()

    if existing.data and not force_update:
        # Check if embedding exists
        if existing.data[0].get('embedding'):
            print(f"  ⏭️  Skipping (exists): {title[:40]}...")
            return True
        print(f"  🔄 Updating embedding: {title[:40]}...")

    # Generate summary
    summary = generate_summary(
        title,
        article.get('content', ''),
        article.get('key_quotes', [])
    )

    # Classify with Diátaxis
    print(f"  📊 Classifying: {title[:40]}...")
    diataxis_type = classify_article(
        title,
        article.get('content', ''),
        article.get('author')
    )
    print(f"     → {diataxis_type}")

    # Generate embedding
    print(f"  🧮 Generating embedding...")
    embedding = generate_article_embedding(
        title=title,
        content=article.get('content', ''),
        summary=summary,
        topics=article.get('topics', []),
        key_quotes=article.get('key_quotes', [])
    )

    if not embedding:
        print(f"  ❌ Failed to generate embedding")
        return False

    # Prepare data for upsert
    data = {
        'url': url,
        'url_hash': url_hash,
        'title': title,
        'author': article.get('author', 'Unknown'),
        'author_id': article.get('author_id', 'unknown'),
        'published': str(article.get('published')) if article.get('published') else None,
        'fetched': str(article.get('fetched')) if article.get('fetched') else str(datetime.now().date()),
        'content': article.get('content', '')[:50000],  # Limit content size
        'summary': summary,
        'topics': article.get('topics', []),
        'key_quotes': article.get('key_quotes', []),
        'stance': article.get('stance', {}),
        'evolution_note': article.get('evolution_note', ''),
        'tags': article.get('tags', []),
        'diataxis_type': diataxis_type,
        'embedding': embedding
    }

    try:
        # Upsert (insert or update based on URL)
        result = supabase.table('articles').upsert(
            data,
            on_conflict='url'
        ).execute()

        if result.data:
            print(f"  ✅ Synced: {title[:40]}...")
            return True
        else:
            print(f"  ❌ Failed to sync: {title[:40]}...")
            return False

    except Exception as e:
        print(f"  ❌ Error syncing: {e}")
        return False


def sync_all_articles(force_update: bool = False) -> Dict[str, int]:
    """
    Sync all markdown articles to Supabase.

    Args:
        force_update: If True, update all articles even if they exist

    Returns:
        Dictionary with counts: synced, skipped, failed
    """
    print("🔄 Supabase Sync")
    print("=" * 50)

    if not supabase:
        print("❌ Error: Supabase not configured")
        print("   Set SUPABASE_URL and SUPABASE_ANON_KEY environment variables")
        return {'synced': 0, 'skipped': 0, 'failed': 0}

    # Find all markdown files in content/authors/
    authors_dir = PROJECT_ROOT / 'content' / 'authors'
    if not authors_dir.exists():
        print(f"❌ Authors directory not found: {authors_dir}")
        return {'synced': 0, 'skipped': 0, 'failed': 0}

    md_files = list(authors_dir.glob('**/*.md'))
    print(f"\nFound {len(md_files)} markdown files")

    stats = {'synced': 0, 'skipped': 0, 'failed': 0}

    for filepath in md_files:
        print(f"\n📄 Processing: {filepath.name}")

        # Parse markdown file
        article = parse_markdown_file(filepath)
        if not article:
            stats['failed'] += 1
            continue

        # Sync to Supabase
        if sync_article_to_supabase(article, force_update=force_update):
            stats['synced'] += 1
        else:
            stats['failed'] += 1

    # Summary
    print("\n" + "=" * 50)
    print("✅ Sync Complete!")
    print(f"   Synced: {stats['synced']}")
    print(f"   Skipped: {stats['skipped']}")
    print(f"   Failed: {stats['failed']}")

    return stats


def test_connection():
    """Test Supabase connection"""
    if not supabase:
        print("❌ Supabase not configured")
        return False

    try:
        result = supabase.table('articles').select('id').limit(1).execute()
        print("✅ Supabase connection successful")
        return True
    except Exception as e:
        print(f"❌ Supabase connection failed: {e}")
        return False


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Sync articles to Supabase')
    parser.add_argument('--force', action='store_true', help='Force update all articles')
    parser.add_argument('--test', action='store_true', help='Test connection only')

    args = parser.parse_args()

    if args.test:
        test_connection()
    else:
        sync_all_articles(force_update=args.force)
