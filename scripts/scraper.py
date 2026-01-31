#!/usr/bin/env python3
"""
Content Scraper for AI Thought Leadership Knowledge Base
Fetches blog posts via RSS or web scraping and saves to Obsidian vault
"""

# Load environment variables from .env file
try:
    from load_env import load_env
    load_env()
except ImportError:
    pass

import feedparser
import requests
from bs4 import BeautifulSoup
import yaml
from datetime import datetime
from pathlib import Path
import hashlib
import re
import sys
import os
from content_processor import process_article

# Get project root directory (parent of scripts/)
PROJECT_ROOT = Path(__file__).parent.parent

def load_config(config_file='config/sources.yaml'):
    """Load source configuration"""
    config_path = PROJECT_ROOT / config_file
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    return [s for s in config['sources'] if s.get('active', True)]

def fetch_rss_posts(source):
    """Fetch posts from RSS feed"""
    print(f"  Fetching RSS: {source['rss']}")

    try:
        feed = feedparser.parse(source['rss'])
        posts = []

        for entry in feed.entries[:10]:  # Limit to 10 most recent
            # Parse published date
            pub_date = None
            if hasattr(entry, 'published_parsed'):
                pub_date = datetime(*entry.published_parsed[:6])
            elif hasattr(entry, 'updated_parsed'):
                pub_date = datetime(*entry.updated_parsed[:6])
            else:
                pub_date = datetime.now()

            # Extract content
            content = ''
            if hasattr(entry, 'content'):
                content = entry.content[0].value
            elif hasattr(entry, 'summary'):
                content = entry.summary
            elif hasattr(entry, 'description'):
                content = entry.description

            posts.append({
                'title': entry.title,
                'url': entry.link,
                'published': pub_date,
                'content': content,
                'author': source['name'],
                'author_id': source['id']
            })

        print(f"  Found {len(posts)} posts")
        return posts

    except Exception as e:
        print(f"  Error fetching RSS: {e}")
        return []

def scrape_web_posts(source):
    """Scrape blog posts from website (for sites without RSS)"""
    print(f"  Web scraping: {source['url']}")

    try:
        response = requests.get(source['url'], timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')

        # This is a generic scraper - may need customization per site
        # Look for common blog post patterns
        posts = []

        # Try to find article links
        article_links = soup.find_all('a', href=True)

        # Filter for likely blog post URLs
        blog_urls = set()
        for link in article_links[:20]:  # Limit to first 20 links
            href = link.get('href', '')

            # Make absolute URL
            if href.startswith('/'):
                from urllib.parse import urljoin
                href = urljoin(source['url'], href)

            # Filter for blog post patterns (customize as needed)
            if any(pattern in href for pattern in ['/blog/', '/post/', '/writing/', '/engineering/']):
                blog_urls.add(href)

        # Fetch each article
        for url in list(blog_urls)[:5]:  # Limit to 5 most recent
            try:
                article = scrape_single_article(url, source)
                if article:
                    posts.append(article)
            except Exception as e:
                print(f"    Error scraping {url}: {e}")

        print(f"  Found {len(posts)} posts")
        return posts

    except Exception as e:
        print(f"  Error web scraping: {e}")
        return []

def scrape_single_article(url, source):
    """Scrape a single article page"""
    print(f"    Scraping: {url}")

    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract title
    title = None
    if soup.find('h1'):
        title = soup.find('h1').get_text().strip()
    elif soup.find('title'):
        title = soup.find('title').get_text().strip()
    else:
        title = "Untitled"

    # Extract article content
    content = ''
    selector = source.get('scrape_selector', 'article')
    article_elem = soup.find(selector) or soup.find('article') or soup.find('main')

    if article_elem:
        # Remove script and style tags
        for script in article_elem(['script', 'style']):
            script.decompose()
        content = article_elem.get_text(separator='\n', strip=True)

    # Try to extract date (common patterns)
    pub_date = datetime.now()
    date_elem = soup.find('time')
    if date_elem and date_elem.get('datetime'):
        try:
            from dateutil import parser
            pub_date = parser.parse(date_elem['datetime'])
        except:
            pass

    return {
        'title': title,
        'url': url,
        'published': pub_date,
        'content': content,
        'author': source['name'],
        'author_id': source['id']
    }

def generate_slug(title):
    """Generate URL-safe slug from title"""
    slug = re.sub(r'[^\w\s-]', '', title.lower())
    slug = re.sub(r'[-\s]+', '-', slug)
    return slug[:60]  # Limit length

def article_exists(author_id, url):
    """Check if article already exists in vault"""
    # Create a hash of the URL to use as unique identifier
    url_hash = hashlib.md5(url.encode()).hexdigest()[:8]

    author_dir = PROJECT_ROOT / "content" / "authors" / author_id
    if not author_dir.exists():
        return False

    # Check if any file contains this URL in frontmatter
    for md_file in author_dir.glob('*.md'):
        try:
            content = md_file.read_text()
            if url in content or url_hash in md_file.name:
                return True
        except:
            pass

    return False

def save_article(article_data, dry_run=False):
    """Save article to Obsidian vault"""
    author_id = article_data['author_id']
    pub_date = article_data['published']

    # Generate filename
    date_str = pub_date.strftime('%Y-%m-%d')
    slug = generate_slug(article_data['title'])
    url_hash = hashlib.md5(article_data['url'].encode()).hexdigest()[:8]
    filename = f"{date_str}-{slug}-{url_hash}.md"

    # Create author directory if needed
    author_dir = PROJECT_ROOT / "content" / "authors" / author_id
    author_dir.mkdir(parents=True, exist_ok=True)

    filepath = author_dir / filename

    # Process article with GPT-4 to extract metadata
    print(f"    Processing with GPT-4...")
    metadata = process_article(article_data)

    # Generate markdown content
    markdown = generate_markdown(article_data, metadata)

    if dry_run:
        print(f"    [DRY RUN] Would save to: {filepath}")
        return str(filepath)

    # Save file
    filepath.write_text(markdown)
    print(f"    Saved: {filepath}")

    return str(filepath)

def generate_markdown(article_data, metadata):
    """Generate markdown file with frontmatter"""

    # Build frontmatter as a proper dictionary, then dump as YAML
    frontmatter_data = {
        'title': article_data['title'],
        'author': article_data['author'],
        'author_id': article_data['author_id'],
        'url': article_data['url'],
        'published': article_data['published'].strftime('%Y-%m-%d'),
        'fetched': datetime.now().strftime('%Y-%m-%d'),
        'topics': metadata.get('topics', []),
        'key_quotes': metadata.get('key_quotes', []),
        'stance': metadata.get('stance', {}),
        'evolution_note': metadata.get('evolution_note', ''),
        'tags': metadata.get('tags', [])
    }

    frontmatter = "---\n"
    frontmatter += yaml.dump(frontmatter_data, default_flow_style=False, allow_unicode=True, sort_keys=False)
    frontmatter += "---\n\n"

    # Convert HTML content to markdown (basic conversion)
    content = clean_content(article_data['content'])

    markdown = frontmatter + f"# {article_data['title']}\n\n"
    markdown += f"**Author**: {article_data['author']}  \n"
    markdown += f"**Published**: {article_data['published'].strftime('%Y-%m-%d')}  \n"
    markdown += f"**Source**: [{article_data['url']}]({article_data['url']})\n\n"
    markdown += "---\n\n"
    markdown += content
    markdown += "\n\n---\n\n"
    markdown += "## Key Takeaways\n\n"

    # Add key quotes
    if metadata.get('key_quotes'):
        markdown += "### Notable Quotes\n\n"
        for quote in metadata['key_quotes']:
            markdown += f"> {quote['text']}\n\n"
            markdown += f"*Context: {quote['context']}*\n\n"

    # Add topic links
    if metadata.get('topics'):
        markdown += "## Related Topics\n\n"
        for topic in metadata['topics']:
            topic_slug = generate_slug(topic)
            markdown += f"- [[topics/{topic_slug}]]\n"

    return markdown

def clean_content(html_content):
    """Clean and format content"""
    # Remove excessive whitespace
    content = re.sub(r'\n\s*\n\s*\n', '\n\n', html_content)
    content = content.strip()
    return content

def main(dry_run=False, limit=None, days_back=7):
    """Main scraper function"""
    from datetime import timedelta

    print("🔍 AI Thought Leadership Scraper")
    print("=" * 50)

    # Calculate cutoff date
    cutoff_date = datetime.now() - timedelta(days=days_back)
    print(f"\n📅 Looking for articles from the last {days_back} days")
    print(f"   (published after {cutoff_date.strftime('%Y-%m-%d')})")

    # Load sources
    sources = load_config()
    print(f"\nConfigured sources: {len(sources)}")

    new_articles = []
    skipped_articles = 0

    for source in sources:
        print(f"\n📰 Processing: {source['name']}")

        # Fetch posts
        if source.get('rss'):
            posts = fetch_rss_posts(source)
        else:
            posts = scrape_web_posts(source)

        # Process each post
        for post in posts:
            # Check if article is too old
            if post['published'] < cutoff_date:
                print(f"  ⏭️  Skipping (too old: {post['published'].strftime('%Y-%m-%d')}): {post['title'][:40]}...")
                skipped_articles += 1
                continue

            # Check if already exists
            if article_exists(source['id'], post['url']):
                print(f"  ⏭️  Skipping (exists): {post['title'][:50]}...")
                skipped_articles += 1
                continue

            print(f"  ✨ New article: {post['title'][:50]}...")

            try:
                filepath = save_article(post, dry_run=dry_run)
                new_articles.append(filepath)

                if limit and len(new_articles) >= limit:
                    print(f"\n⚠️  Reached limit of {limit} articles")
                    break

            except Exception as e:
                print(f"  ❌ Error saving: {e}")

        if limit and len(new_articles) >= limit:
            break

    # Summary
    print("\n" + "=" * 50)
    print(f"✅ Complete!")
    print(f"  New articles: {len(new_articles)}")
    print(f"  Skipped (existing): {skipped_articles}")

    if new_articles:
        print("\n📝 New articles saved:")
        for filepath in new_articles:
            print(f"  - {filepath}")

    return new_articles

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Scrape AI thought leadership content')
    parser.add_argument('--dry-run', action='store_true', help='Test run without saving')
    parser.add_argument('--limit', type=int, help='Limit number of new articles to fetch')
    parser.add_argument('--days-back', type=int, default=7, help='How many days back to look for articles (default: 7)')

    args = parser.parse_args()

    # Check for OpenAI API key
    if not os.getenv('OPENAI_API_KEY'):
        print("⚠️  Warning: OPENAI_API_KEY not set. Metadata extraction will fail.")
        print("   Set it with: export OPENAI_API_KEY='sk-...'")

    main(dry_run=args.dry_run, limit=args.limit, days_back=args.days_back)
