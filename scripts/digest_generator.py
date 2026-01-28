#!/usr/bin/env python3
"""
Weekly Digest Generator
Creates synthesized weekly digests from new content using GPT-4
"""

import os
import glob
from datetime import datetime, timedelta
from pathlib import Path
import yaml
import frontmatter
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def get_week_number():
    """Get current ISO week number"""
    return datetime.now().strftime('%Y-W%U')

def get_date_range(days=7):
    """Get date range for filtering posts"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    return start_date, end_date

def find_recent_posts(days=7):
    """Find all posts from the last N days"""
    start_date, end_date = get_date_range(days)
    posts = []

    # Search all author directories
    for md_file in Path('content/authors').glob('**/*.md'):
        try:
            post = frontmatter.load(md_file)

            # Get published date
            pub_date = post.get('published')
            if isinstance(pub_date, str):
                pub_date = datetime.fromisoformat(pub_date)

            # Check if within date range
            if pub_date and start_date <= pub_date <= end_date:
                posts.append({
                    'title': post.get('title', 'Untitled'),
                    'author': post.get('author', 'Unknown'),
                    'url': post.get('url', ''),
                    'published': pub_date,
                    'topics': post.get('topics', []),
                    'key_quotes': post.get('key_quotes', []),
                    'stance': post.get('stance', {}),
                    'evolution_note': post.get('evolution_note', ''),
                    'filepath': str(md_file)
                })

        except Exception as e:
            print(f"Error parsing {md_file}: {e}")

    # Sort by date (newest first)
    posts.sort(key=lambda x: x['published'], reverse=True)

    return posts

def generate_digest_content(posts):
    """Use GPT-4 to create synthesized digest"""

    if not posts:
        return None

    # Create summary of posts for GPT-4
    post_summaries = []
    for post in posts:
        summary = f"""
**{post['title']}** by {post['author']}
Published: {post['published'].strftime('%Y-%m-%d')}
URL: {post['url']}
Topics: {', '.join(post['topics'])}
Evolution note: {post['evolution_note']}
"""
        if post['key_quotes']:
            summary += f"\nKey quotes:\n"
            for quote in post['key_quotes'][:2]:
                summary += f"  - \"{quote['text']}\"\n"

        post_summaries.append(summary.strip())

    all_summaries = "\n\n---\n\n".join(post_summaries)

    prompt = f"""Create a compelling weekly digest for AI thought leadership content.

**This week's posts ({len(posts)} total):**

{all_summaries}

**Generate a digest with these sections:**

1. **Executive Summary** (2-3 sentences)
   - What's the big picture this week?
   - Any emerging themes or surprising insights?

2. **Highlights by Theme**
   - Group related posts by common themes
   - For each theme: brief synthesis + which authors contributed

3. **Notable Quotes** (3-5 most impactful)
   - Include quote + author + why it matters

4. **Evolution Watch**
   - Track how ideas are evolving
   - Note any shifts in perspective or new paradigms

5. **Recommended Reads** (Top 3)
   - Which posts are must-reads and why?
   - Brief value proposition for each

**Format:**
- Use markdown
- Keep it concise but insightful
- Link to original posts: [Title](url)
- Highlight cross-author connections
- Note areas of agreement/disagreement if any

**Tone:**
- Professional but engaging
- Focus on insights, not summaries
- Synthesize, don't just list
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert at synthesizing technical content into insightful digests. You understand AI, coding tools, software development, and thought leadership. You identify patterns, connections, and emerging trends across multiple sources."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=2000
        )

        digest_content = response.choices[0].message.content.strip()
        return digest_content

    except Exception as e:
        print(f"Error generating digest with GPT-4: {e}")
        return None

def create_simple_digest(posts):
    """Fallback: Create simple digest without GPT-4"""

    digest = f"# Weekly AI Thought Leadership Digest\n\n"
    digest += f"**Week**: {get_week_number()}  \n"
    digest += f"**Posts**: {len(posts)}  \n"
    digest += f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"

    digest += "---\n\n"
    digest += "## This Week's Posts\n\n"

    for post in posts:
        digest += f"### [{post['title']}]({post['url']})\n\n"
        digest += f"**Author**: {post['author']}  \n"
        digest += f"**Published**: {post['published'].strftime('%Y-%m-%d')}  \n"
        digest += f"**Topics**: {', '.join(post['topics'])}  \n\n"

        if post['key_quotes']:
            digest += "**Key Quote**:\n"
            digest += f"> {post['key_quotes'][0]['text']}\n\n"

        digest += "---\n\n"

    return digest

def save_digest(digest_content, week_number):
    """Save digest to markdown file"""

    # Create synthesis directory if needed
    digest_dir = Path('content/synthesis/weekly-digests')
    digest_dir.mkdir(parents=True, exist_ok=True)

    filename = digest_dir / f"{week_number}.md"

    # Create frontmatter
    frontmatter_content = f"""---
week: {week_number}
generated: {datetime.now().isoformat()}
type: weekly-digest
---

"""

    full_content = frontmatter_content + digest_content

    filename.write_text(full_content)

    return str(filename)

def save_digest_html(digest_content, week_number):
    """Convert digest to HTML for email"""

    try:
        import markdown

        # Convert markdown to HTML
        html = markdown.markdown(digest_content, extensions=['extra', 'codehilite'])

        # Wrap in email template
        html_template = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 700px;
            margin: 0 auto;
            padding: 20px;
        }}
        h1, h2, h3 {{ color: #2c3e50; }}
        blockquote {{
            border-left: 4px solid #3498db;
            padding-left: 20px;
            margin-left: 0;
            font-style: italic;
            color: #555;
        }}
        a {{ color: #3498db; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
        hr {{ border: none; border-top: 1px solid #eee; margin: 30px 0; }}
    </style>
</head>
<body>
    {html}
    <hr>
    <p style="font-size: 12px; color: #999; text-align: center;">
        AI Thought Leadership Knowledge Base · Week {week_number}
    </p>
</body>
</html>
"""

        # Save HTML version
        digest_dir = Path('content/synthesis/weekly-digests')
        html_file = digest_dir / f"{week_number}.html"
        html_file.write_text(html_template)

        return str(html_file)

    except ImportError:
        print("markdown library not installed, skipping HTML generation")
        return None

def main(days=7, use_gpt4=True):
    """Main digest generation function"""

    print(f"📊 Generating Weekly Digest")
    print("=" * 50)

    week_number = get_week_number()
    print(f"Week: {week_number}")

    # Find recent posts
    posts = find_recent_posts(days=days)
    print(f"Found {len(posts)} posts from the last {days} days")

    if not posts:
        print("No new posts to digest")
        return None

    # Generate digest
    if use_gpt4 and os.getenv('OPENAI_API_KEY'):
        print("Generating digest with GPT-4...")
        digest_content = generate_digest_content(posts)
        if not digest_content:
            print("GPT-4 failed, using simple digest")
            digest_content = create_simple_digest(posts)
    else:
        print("Generating simple digest...")
        digest_content = create_simple_digest(posts)

    # Save digest
    md_file = save_digest(digest_content, week_number)
    print(f"✅ Saved markdown: {md_file}")

    html_file = save_digest_html(digest_content, week_number)
    if html_file:
        print(f"✅ Saved HTML: {html_file}")

    print("\n" + "=" * 50)
    print("Digest generation complete!")

    return {
        'week': week_number,
        'posts_count': len(posts),
        'markdown_file': md_file,
        'html_file': html_file,
        'content': digest_content
    }

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Generate weekly digest')
    parser.add_argument('--days', type=int, default=7, help='Days to look back')
    parser.add_argument('--no-gpt4', action='store_true', help='Skip GPT-4, use simple digest')

    args = parser.parse_args()

    if not os.getenv('OPENAI_API_KEY') and not args.no_gpt4:
        print("⚠️  Warning: OPENAI_API_KEY not set. Will use simple digest.")

    result = main(days=args.days, use_gpt4=not args.no_gpt4)

    if result:
        print(f"\nDigest preview (first 500 chars):")
        print("-" * 50)
        print(result['content'][:500])
        print("...")
