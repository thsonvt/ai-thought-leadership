# Thought Leadership Knowledge Base - Implementation Plan

**Created**: 2026-01-29
**Status**: Ready for Implementation
**Estimated Timeline**: Phase 1 (2 weeks), Phase 2 (1 week), Phase 3 (ongoing)

---

## Overview

A simple, AI-powered knowledge base to track thought leaders in AI-assisted coding, built with Obsidian + automation scripts. Enables semantic search, cross-referencing, and thought evolution tracking.

### Key Requirements
- **Sources**: 5-10 blogs initially, scaling to dozens
- **Content**: Long-form posts (blogs), future: tweets, YouTube, GitHub
- **Update Frequency**: Weekly automated ingestion
- **Search**: Semantic search + filtered browsing
- **Interaction**: All of: Q&A, browsing, periodic summaries, quick reference
- **Location**: Separate from Mintlify docs (private system)
- **Simplicity**: Obsidian-based (no custom app development)
- **Cost**: ~$5-10/month (OpenAI embeddings)

### Unique Features
- **Cross-referencing**: Connect ideas across authors
- **Thought evolution**: Track how perspectives change over time
- **Weekly digest**: Email + Slack notifications
- **Configurable notifications**: Turn on/off, adjust frequency

---

## System Architecture

```
┌────────────────────────────────────────────────────┐
│          GitHub Actions (Weekly Cron)              │
│  ┌──────────────────────────────────────────────┐ │
│  │ 1. Fetch RSS/Web Content                    │ │
│  │ 2. Extract & Convert to Markdown            │ │
│  │ 3. GPT-4 Analysis (topics, quotes, stance)  │ │
│  │ 4. Commit to Obsidian Vault Repo            │ │
│  │ 5. Generate Weekly Digest                   │ │
│  │ 6. Send Notifications (Email/Slack)         │ │
│  └──────────────────────────────────────────────┘ │
└────────────────┬───────────────────────────────────┘
                 │
                 ▼
┌────────────────────────────────────────────────────┐
│        Obsidian Vault (GitHub Repo + Local)        │
│  ┌──────────────────────────────────────────────┐ │
│  │ content/authors/[name]/[date]-[slug].md     │ │
│  │ content/topics/[topic].md (MOCs)            │ │
│  │ content/synthesis/weekly-digests/           │ │
│  │ .obsidian/plugins/smart-connections/        │ │
│  │ .obsidian/plugins/dataview/                 │ │
│  │ scripts/scraper.py                          │ │
│  │ scripts/digest_generator.py                 │ │
│  │ config/sources.yaml                         │ │
│  │ config/notifications.yaml                   │ │
│  └──────────────────────────────────────────────┘ │
└────────────────┬───────────────────────────────────┘
                 │
                 ▼
┌────────────────────────────────────────────────────┐
│      Obsidian (Local) + Smart Connections          │
│  • Semantic search via OpenAI embeddings           │
│  • Dataview queries for timeline views             │
│  • Graph view for cross-references                 │
│  • Daily notes for synthesis                       │
└────────────────────────────────────────────────────┘
```

---

## Phase 1: MVP Setup (Week 1-2)

### 1.1 Obsidian Vault Structure

**Directory Layout:**
```
ai-thought-leadership/  (Git repo)
├── .github/
│   └── workflows/
│       ├── weekly-ingestion.yml       # Weekly cron job
│       └── weekly-digest.yml          # Weekly digest generation
│
├── content/
│   ├── authors/
│   │   ├── jesse-chen/
│   │   │   └── 2024-01-15-claude-code-vs-cursor.md
│   │   ├── kieran-klaassen/
│   │   ├── naveen-naidu/
│   │   ├── every-dan-shipper/
│   │   └── anthropic-engineering/
│   │
│   ├── topics/                        # MOCs (Maps of Content)
│   │   ├── claude-code.md
│   │   ├── ai-agents.md
│   │   ├── cursor.md
│   │   ├── prompt-engineering.md
│   │   └── agent-native-architecture.md
│   │
│   └── synthesis/
│       ├── weekly-digests/
│       │   └── 2024-W04.md
│       ├── thought-evolutions/
│       │   └── ai-coding-tools-evolution.md
│       └── cross-references.md
│
├── scripts/
│   ├── scraper.py                     # Main ingestion script
│   ├── content_processor.py           # GPT-4 analysis
│   ├── digest_generator.py            # Weekly digest
│   ├── notification_sender.py         # Email/Slack notifications
│   └── requirements.txt
│
├── config/
│   ├── sources.yaml                   # Blog URLs & metadata
│   ├── notifications.yaml             # Notification settings
│   └── topics.yaml                    # Topic taxonomy
│
├── .obsidian/
│   ├── plugins/
│   │   ├── smart-connections/         # AI semantic search
│   │   ├── dataview/                  # Timeline queries
│   │   └── obsidian-timeline/         # Visual timeline
│   └── workspace.json
│
└── README.md
```

### 1.2 Initial Content Sources (sources.yaml)

```yaml
sources:
  - name: Jesse Chen
    url: https://blog.fsck.com/
    type: blog
    rss: https://blog.fsck.com/feed.xml
    tags: [ai-coding, cursor, claude-code]

  - name: Naveen Naidu
    url: https://www.naveennaidu.com/writing/
    type: blog
    rss: null  # Manual scraping
    tags: [agent-native, architecture]

  - name: Kieran Klaassen
    url: https://www.kieranklaassen.com/
    type: blog
    rss: https://www.kieranklaassen.com/rss.xml
    tags: [ai-tools, development]

  - name: Dan Shipper (Every)
    url: https://every.to/source-code/
    type: blog
    rss: https://every.to/source-code/feed
    tags: [claude-code, ai-workflow]

  - name: Anthropic Engineering
    url: https://www.anthropic.com/engineering/
    type: blog
    rss: null  # Manual scraping
    tags: [claude, ai-safety, engineering]
```

### 1.3 Article Markdown Template

**Frontmatter Structure:**
```yaml
---
title: "Claude Code vs Cursor: My Experience"
author: Jesse Chen
author_id: jesse-chen
url: https://blog.fsck.com/2024/01/claude-code-vs-cursor
published: 2024-01-15
fetched: 2024-01-20
topics:
  - AI Coding Tools
  - Claude Code
  - Cursor
key_quotes:
  - text: "Cursor's inline suggestions feel more natural for small edits"
    context: Comparing inline completion UX
  - text: "Claude Code's agentic approach is better for complex refactors"
    context: Workflow differences
stance:
  claude_code: positive
  cursor: neutral
  ai_coding_general: positive
evolution_note: "Early exploration phase, comparing tools on surface features"
tags: [ai-coding, cursor, claude-code, comparison]
---

# Claude Code vs Cursor: My Experience

[Article content in markdown...]

## Key Takeaways
- ...

## Related Posts
- [[2024-02-10-my-month-with-claude-code]]
- [[topics/claude-code]]
```

### 1.4 Scraper Script (Python)

**scripts/scraper.py**
```python
import feedparser
import requests
from bs4 import BeautifulSoup
import yaml
from datetime import datetime
import os
from pathlib import Path

def load_sources():
    with open('config/sources.yaml', 'r') as f:
        return yaml.safe_load(f)['sources']

def fetch_rss_posts(rss_url):
    feed = feedparser.parse(rss_url)
    return [{
        'title': entry.title,
        'url': entry.link,
        'published': entry.published_parsed,
        'content': entry.get('content', [{}])[0].get('value', '')
    } for entry in feed.entries]

def scrape_web_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    # Extract article content (custom logic per site)
    # This will need site-specific selectors
    return soup.get_text()

def process_with_gpt4(content, author):
    """Extract topics, key quotes, and stance using GPT-4"""
    # Implementation in content_processor.py
    pass

def save_article(article_data, author_slug):
    date_str = article_data['published'].strftime('%Y-%m-%d')
    slug = article_data['title'].lower().replace(' ', '-')[:50]
    filename = f"content/authors/{author_slug}/{date_str}-{slug}.md"

    Path(filename).parent.mkdir(parents=True, exist_ok=True)

    with open(filename, 'w') as f:
        f.write(generate_markdown(article_data))

def generate_markdown(data):
    # Generate frontmatter + content
    pass

if __name__ == '__main__':
    sources = load_sources()
    for source in sources:
        print(f"Processing {source['name']}...")
        if source.get('rss'):
            posts = fetch_rss_posts(source['rss'])
        else:
            # Manual scraping logic
            posts = scrape_web_posts(source['url'])

        for post in posts:
            # Check if already exists
            # Process with GPT-4
            # Save to vault
            pass
```

### 1.5 Content Processor (GPT-4 Analysis)

**scripts/content_processor.py**
```python
import openai
import yaml

def extract_metadata(content, author, url):
    """Use GPT-4 to extract structured metadata"""

    prompt = f"""Analyze this blog post and extract:
1. Main topics (3-5 topics)
2. Key quotes (2-4 impactful quotes with context)
3. Author's stance on mentioned tools/concepts (positive/neutral/negative/critical)
4. Brief evolution note (how this fits into their thought journey)

Article by {author}:
{content[:4000]}  # First 4000 chars

Return as YAML:
topics:
  - Topic 1
  - Topic 2
key_quotes:
  - text: "quote"
    context: "what they're discussing"
stance:
  claude_code: positive
  cursor: neutral
evolution_note: "brief summary"
"""

    response = openai.ChatCompletion.create(
        model="gpt-4-turbo-preview",
        messages=[
            {"role": "system", "content": "You are an expert at extracting structured metadata from technical blog posts."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    metadata = yaml.safe_load(response.choices[0].message.content)
    return metadata
```

### 1.6 GitHub Actions Workflow

**.github/workflows/weekly-ingestion.yml**
```yaml
name: Weekly Content Ingestion

on:
  schedule:
    - cron: '0 9 * * 1'  # Every Monday at 9am UTC
  workflow_dispatch:      # Manual trigger

jobs:
  ingest:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -r scripts/requirements.txt

      - name: Run scraper
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: |
          python scripts/scraper.py

      - name: Commit new content
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add content/
          git diff --quiet && git diff --staged --quiet || git commit -m "Weekly ingestion: $(date +%Y-%m-%d)"
          git push

      - name: Generate weekly digest
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: |
          python scripts/digest_generator.py

      - name: Send notifications
        env:
          SENDGRID_API_KEY: ${{ secrets.SENDGRID_API_KEY }}
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
        run: |
          python scripts/notification_sender.py
```

### 1.7 Obsidian Plugins Setup

**Required Plugins:**
1. **Smart Connections** (AI semantic search)
   - Settings → API Key: OpenAI key
   - Model: text-embedding-3-small
   - Enable: Chat view, search view

2. **Dataview** (Timeline queries)
   - Enable JavaScript queries
   - Used for thought evolution views

3. **Obsidian Timeline** (Visual timeline)
   - For graph-based timeline visualization

**Installation:**
```bash
# In Obsidian:
# Settings → Community Plugins → Browse
# Search and install:
# - Smart Connections
# - Dataview
# - Obsidian Timeline
```

---

## Phase 2: Automation & Intelligence (Week 3-4)

### 2.1 Thought Evolution Timeline

**Topic MOC Template** (content/topics/claude-code.md):
````markdown
---
topic: Claude Code
related_topics: [AI Coding Tools, Cursor, Agent-Native Architecture]
---

# Claude Code: Thought Evolution

## Timeline View

```dataview
TABLE
  author,
  published as "Date",
  stance.claude_code as "Stance",
  evolution_note as "Evolution Note"
FROM "content/authors"
WHERE contains(topics, "Claude Code")
SORT published ASC
```

## Key Insights by Author

### Jesse Chen's Journey
```dataview
LIST key_quotes
FROM "content/authors/jesse-chen"
WHERE contains(topics, "Claude Code")
SORT published ASC
```

### Cross-Author Comparison
- **Early adopters**: [[authors/jesse-chen]], [[authors/dan-shipper]]
- **Skeptics turned believers**: [TBD as content grows]
- **Critical perspectives**: [TBD]

## Evolution Pattern
[Manual synthesis of how collective thought on Claude Code evolved]

## Related Topics
- [[topics/cursor]]
- [[topics/ai-agents]]
- [[topics/agent-native-architecture]]
````

### 2.2 Weekly Digest Generator

**scripts/digest_generator.py**
```python
import openai
from datetime import datetime, timedelta
import glob
import os

def get_this_weeks_posts():
    """Find all posts from the last 7 days"""
    one_week_ago = datetime.now() - timedelta(days=7)
    posts = []

    for filepath in glob.glob('content/authors/**/*.md', recursive=True):
        # Parse frontmatter date
        # Filter by date
        # Add to posts list
        pass

    return posts

def generate_digest(posts):
    """Use GPT-4 to create a synthesized weekly digest"""

    content_summary = "\n\n".join([
        f"**{post['title']}** by {post['author']}\n{post['url']}\nKey topics: {', '.join(post['topics'])}"
        for post in posts
    ])

    prompt = f"""Create a weekly digest email for AI coding thought leadership updates.

This week's posts ({len(posts)} total):
{content_summary}

Generate:
1. Executive summary (2-3 sentences)
2. Highlights by theme (group related posts)
3. Notable quotes (2-3 most impactful)
4. Emerging trends (what's new or changing)
5. Recommended reads (top 3 with brief why)

Format as clean HTML for email.
"""

    response = openai.ChatCompletion.create(
        model="gpt-4-turbo-preview",
        messages=[
            {"role": "system", "content": "You are an expert at synthesizing technical content into insightful digests."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    return response.choices[0].message.content

def save_digest(digest_html, week_number):
    """Save digest to synthesis folder"""
    filename = f"content/synthesis/weekly-digests/{week_number}.md"

    with open(filename, 'w') as f:
        f.write(f"---\nweek: {week_number}\ngenerated: {datetime.now()}\n---\n\n")
        f.write(digest_html)

if __name__ == '__main__':
    posts = get_this_weeks_posts()
    if posts:
        week_num = datetime.now().strftime('%Y-W%U')
        digest = generate_digest(posts)
        save_digest(digest, week_num)
        print(f"Digest generated: {week_num}")
    else:
        print("No new posts this week")
```

### 2.3 Notification System

**config/notifications.yaml**
```yaml
notifications:
  enabled: true
  frequency: weekly  # Options: daily, weekly, biweekly, monthly

  email:
    enabled: true
    recipients:
      - your.email@example.com
    subject_prefix: "[AI Thought Leadership]"

  slack:
    enabled: true
    webhook_url: env:SLACK_WEBHOOK_URL
    channel: "#ai-research"

  content:
    include_new_posts: true
    include_digest: true
    include_top_quotes: true
    max_posts_per_notification: 10
```

**scripts/notification_sender.py**
```python
import yaml
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import requests

def load_config():
    with open('config/notifications.yaml', 'r') as f:
        return yaml.safe_load(f)

def send_email(digest_html, config):
    if not config['notifications']['email']['enabled']:
        return

    message = Mail(
        from_email='noreply@yourdomain.com',
        to_emails=config['notifications']['email']['recipients'],
        subject=f"{config['notifications']['email']['subject_prefix']} Weekly Digest",
        html_content=digest_html
    )

    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    response = sg.send(message)
    print(f"Email sent: {response.status_code}")

def send_slack(digest_text, config):
    if not config['notifications']['slack']['enabled']:
        return

    webhook_url = os.environ.get('SLACK_WEBHOOK_URL')

    payload = {
        "text": "📚 Weekly AI Thought Leadership Digest",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": digest_text[:3000]  # Slack has char limits
                }
            }
        ]
    }

    response = requests.post(webhook_url, json=payload)
    print(f"Slack sent: {response.status_code}")

if __name__ == '__main__':
    config = load_config()

    # Load latest digest
    # Convert to formats
    # Send via configured channels
    pass
```

---

## Phase 3: Advanced Features (Month 2+)

### 3.1 Automatic Topic MOC Generation

Use GPT-4 to automatically generate and update topic MOCs when new content arrives:
- Extract all posts mentioning a topic
- Generate chronological timeline
- Identify evolution patterns
- Create cross-references

### 3.2 Multi-Modal Content

Extend to YouTube transcripts and tweets:

**sources.yaml additions:**
```yaml
sources:
  - name: Jesse Chen Twitter
    url: https://twitter.com/jesseychen
    type: twitter
    handle: jesseychen

  - name: AI Coding Tools (YouTube)
    url: https://www.youtube.com/@aicodingtools
    type: youtube
    channel_id: UC...
```

### 3.3 Trend Detection

Weekly analysis of emerging themes:
- New topics appearing across multiple authors
- Sentiment shifts (e.g., "Cursor mentions declining")
- Controversy detection (opposing viewpoints)

---

## Technical Requirements

### Python Dependencies (scripts/requirements.txt)
```
feedparser==6.0.10
beautifulsoup4==4.12.2
requests==2.31.0
PyYAML==6.0.1
openai==1.12.0
sendgrid==6.11.0
python-frontmatter==1.0.0
```

### GitHub Secrets Setup
```bash
# In your GitHub repo settings → Secrets and variables → Actions
OPENAI_API_KEY=sk-...
SENDGRID_API_KEY=SG...
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...
```

### Obsidian Setup
1. Download Obsidian: https://obsidian.md/
2. Open vault: File → Open vault → Select `ai-thought-leadership/`
3. Install plugins (listed in 1.7)
4. Configure Smart Connections with OpenAI API key

---

## Cost Estimation

| Service | Usage | Monthly Cost |
|---------|-------|--------------|
| OpenAI Embeddings | ~100 articles/month @ $0.00002/1K tokens | $1-2 |
| OpenAI GPT-4 Analysis | ~100 articles @ 1K tokens each | $3-5 |
| SendGrid Email | 100 emails/month (free tier) | $0 |
| Slack Webhooks | Unlimited (free) | $0 |
| GitHub Actions | ~4 runs/month (free tier) | $0 |
| **Total** | | **~$5-10/month** |

---

## Success Metrics

### Week 1-2 (MVP)
- [ ] 5+ sources configured and scraping successfully
- [ ] 20+ posts ingested and searchable in Obsidian
- [ ] Smart Connections working with semantic search
- [ ] First weekly digest generated

### Week 3-4 (Automation)
- [ ] GitHub Actions running automatically
- [ ] Email + Slack notifications delivered
- [ ] 3+ topic MOCs with thought evolution timelines
- [ ] Zero manual intervention for ingestion

### Month 2+ (Maturity)
- [ ] 100+ posts in knowledge base
- [ ] 10+ topic MOCs with clear evolution patterns
- [ ] Cross-references reveal non-obvious connections
- [ ] Regularly used for quick reference during coding

---

## Next Steps

1. **Set up GitHub repository** for the Obsidian vault
2. **Configure initial sources** in `sources.yaml`
3. **Build scraper script** (Phase 1.4)
4. **Test manual ingestion** of 5-10 posts
5. **Set up GitHub Actions** for automation
6. **Configure notifications** (email/Slack)
7. **Create first weekly digest**

---

## Maintenance

### Weekly (Automated)
- Content ingestion via GitHub Actions
- Digest generation and distribution
- Vector database re-indexing (Smart Connections)

### Monthly (Manual - 30 min)
- Review and update topic MOCs
- Add new sources to `sources.yaml`
- Clean up broken links
- Update topic taxonomy

### Quarterly (Manual - 2 hours)
- Major synthesis: "Quarterly AI Coding Trends Report"
- Archive old digests
- Review and optimize scraping logic
- Update cross-references

---

## Notes

- **Privacy**: Keep repo private if content includes copyrighted material
- **Attribution**: Always include original URLs and author credits
- **Expansion**: Easy to add new sources by editing `sources.yaml`
- **Customization**: Modify GPT-4 prompts to extract different metadata
- **Backup**: Obsidian vault is just markdown files - easy to backup/migrate
