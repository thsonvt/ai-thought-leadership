# AI Thought Leadership Knowledge System — Design

**Date**: 2026-01-31
**Status**: Approved
**Author**: Son Le + Claude

## Overview

A knowledge system that ingests AI thought leadership content daily, enriches it with semantic embeddings and Diátaxis classification, and provides a searchable UI for research and content planning.

### Goals

1. **Research mode**: Explore broadly — "What are people saying about AI agents lately?"
2. **Idea hunting mode**: Targeted search — "Find quotes about context window management"
3. **Gap analysis mode**: Strategic planning — "What Diátaxis content types am I missing?"

### Constraints

- Zero infrastructure management overhead
- Simple daily updates via GitHub Actions
- Semantic search as primary discovery method
- Diátaxis framework for both input classification and output planning

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     GitHub Actions (Daily)                      │
│  scraper.py → content_processor.py → embedding_generator.py     │
│         → supabase_sync.py → trigger Mintlify rebuild           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Supabase (Single Backend)                    │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────────────────┐    │
│  │  articles   │  │ embeddings  │  │ my_content_tracker   │    │
│  │  (metadata) │  │ (pgvector)  │  │ (Diátaxis gap view)  │    │
│  └─────────────┘  └─────────────┘  └──────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                         Mintlify Site                           │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────────────┐     │
│  │  Framework   │  │ Knowledge    │  │  Content Planner  │     │
│  │  (your docs) │  │ Base (search)│  │  (gap dashboard)  │     │
│  └──────────────┘  └──────────────┘  └───────────────────┘     │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Vercel (Search API)                          │
│            docs-assistant API → Supabase pgvector               │
└─────────────────────────────────────────────────────────────────┘
```

### Tech Stack

| Component | Service |
|-----------|---------|
| Article storage + embeddings | Supabase (pgvector) |
| Docs site (framework content) | Mintlify (managed hosting) |
| Search widget/API | Vercel (serverless functions) |
| Daily ingestion | GitHub Actions |

---

## Data Model

### Table: `articles`

```sql
id              UUID PRIMARY KEY
url             TEXT UNIQUE
url_hash        TEXT                 -- first 8 chars MD5
title           TEXT
author          TEXT
author_id       TEXT                 -- matches sources.yaml
published       DATE
fetched         DATE
content         TEXT
summary         TEXT                 -- GPT-4 generated

-- Metadata from GPT-4 extraction
topics          TEXT[]
key_quotes      JSONB                -- [{text, context}, ...]
stance          JSONB                -- {tool_name: sentiment}
evolution_note  TEXT
tags            TEXT[]

-- New enrichments
diataxis_type   TEXT                 -- 'tutorial' | 'how-to' | 'reference' | 'explanation'
embedding       VECTOR(1536)         -- OpenAI text-embedding-3-small

created_at      TIMESTAMPTZ DEFAULT NOW()
```

### Table: `my_content`

```sql
id              UUID PRIMARY KEY
title           TEXT
topic           TEXT
diataxis_type   TEXT
status          TEXT                 -- 'idea' | 'draft' | 'published'
mintlify_path   TEXT
source_articles UUID[]
created_at      TIMESTAMPTZ
published_at    TIMESTAMPTZ
```

### View: `content_gaps`

Topic × Diátaxis type matrix showing scraped article counts and your published content counts.

### Indexes

- `articles_embedding_idx` — HNSW for vector similarity
- `articles_topics_idx` — GIN for array queries
- `articles_author_published_idx` — B-tree for filtering

---

## Ingestion Pipeline

### Current Flow

```
scraper.py → content_processor.py → markdown files → git commit
```

### Enhanced Flow

```
scraper.py
    → content_processor.py (GPT-4 metadata extraction)
    → diataxis_classifier.py (classify article type)
    → embedding_generator.py (generate vector)
    → markdown files (Obsidian compatibility)
    → supabase_sync.py (upsert to database)
    → git commit
    → trigger Mintlify rebuild
```

### New Scripts

| Script | Purpose | API |
|--------|---------|-----|
| `diataxis_classifier.py` | Classify article by Diátaxis type | GPT-4 |
| `embedding_generator.py` | Generate 1536-dim vector | OpenAI embeddings |
| `supabase_sync.py` | Upsert to Supabase | Supabase Python client |

### GitHub Action

```yaml
name: Daily Content Ingestion
on:
  schedule:
    - cron: '0 8 * * *'  # 8am UTC daily
  workflow_dispatch:

jobs:
  ingest:
    steps:
      - Checkout repo
      - Setup Python
      - Install dependencies
      - Run: python scraper.py
      - Run: python supabase_sync.py
      - Commit new markdown files
      - Trigger Mintlify deploy
```

### Cost Estimate

- GPT-4 classification: ~$0.01/article
- Embeddings: ~$0.0001/article
- Supabase: Free tier (500MB)

---

## Search API

**Location**: `mintlify-starter/docs-assistant/apps/api/`

### Endpoints

#### `POST /api/search`

```json
// Request
{
  "query": "how do experts handle context window limits?",
  "filters": {
    "authors": ["dan-shipper-every"],
    "topics": ["Claude Code"],
    "diataxis_type": "how-to",
    "date_from": "2025-01-01"
  },
  "limit": 10
}

// Response
{
  "results": [
    {
      "id": "uuid",
      "title": "Stop Coding and Start Planning",
      "author": "Dan Shipper",
      "published": "2026-01-28",
      "summary": "Why planning beats vibe coding...",
      "diataxis_type": "explanation",
      "topics": ["Claude Code", "AI Workflow"],
      "relevance_score": 0.89,
      "key_quotes": [{"text": "...", "context": "..."}],
      "url": "https://every.to/..."
    }
  ],
  "total": 42
}
```

#### `GET /api/filters`

Returns available authors, topics, diataxis types for filter dropdowns.

#### `GET /api/gaps`

Returns content gap matrix for dashboard.

#### `GET /api/article/:id`

Full article detail with related articles by embedding similarity.

---

## Mintlify UI

### Navigation Structure

```json
{
  "tabs": [
    {
      "tab": "Framework",
      "groups": [/* existing modules */]
    },
    {
      "tab": "Knowledge Base",
      "groups": [
        { "group": "Search", "pages": ["kb/search"] },
        { "group": "Browse", "pages": ["kb/by-author", "kb/by-topic", "kb/recent"] },
        { "group": "Plan", "pages": ["kb/content-gaps", "kb/my-content"] }
      ]
    }
  ]
}
```

### Components

1. **SearchWidget** — Semantic search with filters and results list
2. **FilterPanel** — Author, topic, type, date range selectors
3. **GapDashboard** — Topic × Diátaxis matrix visualization
4. **ArticleDetail** — Full content, quotes, related articles

---

## Implementation Roadmap

### Phase 1: Foundation

- [ ] Set up Supabase project with pgvector
- [ ] Create `diataxis_classifier.py`
- [ ] Create `embedding_generator.py`
- [ ] Create `supabase_sync.py`
- [ ] Backfill existing 18 articles
- [ ] Update GitHub Action to daily schedule

### Phase 2: Search API

- [ ] Set up Vercel project for docs-assistant
- [ ] Implement `POST /api/search`
- [ ] Implement `GET /api/filters`
- [ ] Implement `GET /api/gaps`
- [ ] Add API tests

### Phase 3: Mintlify UI

- [ ] Build SearchWidget component
- [ ] Build FilterPanel component
- [ ] Build GapDashboard component
- [ ] Create Knowledge Base pages
- [ ] Integrate widgets into Mintlify

### Phase 4: Polish

- [ ] Add "Use for content" workflow
- [ ] Add related articles feature
- [ ] Add quote copy-to-clipboard
- [ ] Monitor and iterate

---

## Diátaxis Framework Reference

| Type | Purpose | User Need |
|------|---------|-----------|
| **Tutorial** | Learning-oriented | "Teach me" |
| **How-to** | Task-oriented | "Help me achieve X" |
| **Reference** | Information-oriented | "Give me the facts" |
| **Explanation** | Understanding-oriented | "Help me understand why" |

Used for:
1. Classifying scraped articles by type
2. Structuring your own content output
3. Identifying coverage gaps per topic
