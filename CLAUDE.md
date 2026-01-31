# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

An automated system for tracking AI-assisted coding thought leadership content. Scrapes blogs via RSS/web, uses GPT-4 for semantic analysis, stores as Obsidian-compatible markdown, and sends weekly digests.

## Commands

### Scraping
```bash
cd scripts
python scraper.py --dry-run          # Test without saving
python scraper.py --limit 5          # Fetch limited articles
python scraper.py                    # Fetch all new articles
```

### Digest Generation
```bash
cd scripts
python digest_generator.py           # Generate digest (last 7 days)
python digest_generator.py --days 14 # Custom date range
python digest_generator.py --no-gpt4 # Simple digest without GPT-4
```

### Notifications
```bash
cd scripts
python notification_sender.py --test  # Test configuration
python notification_sender.py         # Send latest digest
```

### Environment Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r scripts/requirements.txt
export OPENAI_API_KEY='sk-...'        # Required
export SENDGRID_API_KEY='SG...'       # Optional (email)
export SLACK_WEBHOOK_URL='https://...' # Optional (Slack)
```

## Architecture

```
scraper.py          → Fetches content via RSS (feedparser) or web scraping (BeautifulSoup)
        ↓
content_processor.py → GPT-4 extracts metadata: topics, key_quotes, stance, evolution_note
        ↓
content/authors/{id}/*.md → Obsidian markdown files with YAML frontmatter
        ↓
digest_generator.py → GPT-4 synthesizes weekly digest from recent posts
        ↓
notification_sender.py → SendGrid email + Slack webhook delivery
```

**Data Flow**: All scripts share `PROJECT_ROOT = Path(__file__).parent.parent` for consistent path resolution.

## Key Patterns

### Article Metadata Structure
Articles are saved with this frontmatter schema:
```yaml
title: "string"
author: "string"
author_id: "string"  # matches config/sources.yaml id
url: "string"
published: "YYYY-MM-DD"
fetched: "YYYY-MM-DD"
topics: ["Topic1", "Topic2"]
key_quotes:
  - text: "quote"
    context: "explanation"
stance:
  tool_name: positive|neutral|negative|critical
evolution_note: "string"
tags: [tag1, tag2]
```

### Source Configuration
Sources in `config/sources.yaml` require:
- `id`: used for author directory name
- `rss`: if null, falls back to web scraping with `scrape_selector`
- `active`: must be true to be processed

### URL Deduplication
Articles are identified by MD5 hash of URL (first 8 chars) appended to filename: `{date}-{slug}-{url_hash}.md`

## GitHub Actions

- `weekly-ingestion.yml`: Runs Mondays 9am UTC (scraper → digest → notifications)
- `manual-digest.yml`: On-demand digest generation

Required secrets: `OPENAI_API_KEY`, optionally `SENDGRID_API_KEY`, `SLACK_WEBHOOK_URL`

## Content Structure

```
content/
├── authors/{author-id}/     # Scraped articles per author
├── topics/                  # MOC (Map of Content) files
└── synthesis/weekly-digests/ # Generated digests (.md + .html)
```

## Obsidian Integration

This vault uses:
- Smart Connections plugin for AI semantic search
- Dataview plugin for timeline queries in topic MOCs
- Topic files use `[[topics/{topic-slug}]]` wikilinks
