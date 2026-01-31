# AI Thought Leadership Knowledge System — Implementation Status

**Date**: 2026-02-01
**Status**: Phase 4 In Progress (Related Articles ✅)
**Reference**: [Original Design](./2026-01-31-knowledge-system-design.md)

---

## Project Overview

A knowledge system that ingests AI thought leadership content daily, enriches it with semantic embeddings and Diátaxis classification, and provides a searchable UI for research and content planning.

---

## Repository Locations

| Component | Path |
|-----------|------|
| **Main Project** (Python ingestion) | `/Users/sonle/Github/ai-thought-leadership/` |
| **Mintlify Site + Widget** | `/Users/sonle/Github/mintlify-starter/` |
| **API (Hono)** | `/Users/sonle/Github/mintlify-starter/docs-assistant/apps/api/` |
| **Widget (React)** | `/Users/sonle/Github/mintlify-starter/docs-assistant/apps/widget/` |

---

## Phase 1: Foundation ✅ COMPLETE

### Scripts Created

| Script | Purpose | Location |
|--------|---------|----------|
| `diataxis_classifier.py` | GPT-4 Diátaxis type classification | `scripts/diataxis_classifier.py` |
| `embedding_generator.py` | OpenAI text-embedding-3-small (1536 dims) | `scripts/embedding_generator.py` |
| `supabase_sync.py` | Upsert articles to Supabase with embeddings | `scripts/supabase_sync.py` |
| `load_env.py` | Environment variable loader | `scripts/load_env.py` |

### Database Setup

| Item | Status | Notes |
|------|--------|-------|
| Supabase project | ✅ Done | pgvector enabled |
| `articles` table | ✅ Done | With embedding column (VECTOR 1536) |
| `match_articles` RPC function | ✅ Done | `scripts/sql/match_articles.sql` |
| HNSW index on embeddings | ✅ Done | For fast similarity search |
| GIN index on topics | ✅ Done | For array queries |

### GitHub Actions

| Workflow | Schedule | Location |
|----------|----------|----------|
| `daily-ingestion.yml` | 8am UTC daily | `.github/workflows/daily-ingestion.yml` |
| `weekly-ingestion.yml` | Mondays 9am UTC | `.github/workflows/weekly-ingestion.yml` |
| `supabase-keepalive.yml` | Prevents Supabase sleep | `.github/workflows/supabase-keepalive.yml` |

### Content Backfill

- **Articles scraped**: 15 (in `content/authors/`)
- **Articles synced to Supabase**: Verify by running `python scripts/supabase_sync.py --test`

---

## Phase 2: Search API ✅ COMPLETE

### API Endpoints

| Endpoint | Method | Purpose | Status |
|----------|--------|---------|--------|
| `/api/search` | POST | Semantic search with filters | ✅ Done |
| `/api/filters` | GET | Filter options for dropdowns | ✅ Done |
| `/api/gaps` | GET | Content gap matrix | ✅ Done |
| `/api/article/:id` | GET | Article detail | ✅ Done |
| `/health` | GET | Health check | ✅ Done |

### Implementation Details

- **Framework**: Hono (TypeScript)
- **Deployment targets**:
  - Vercel: `apps/api/api/index.ts`
  - Cloudflare Workers: `apps/api/src/index.ts`
- **Vector search**: Uses Supabase RPC `match_articles` with threshold 0.2

### API File Locations

```
mintlify-starter/docs-assistant/apps/api/
├── api/index.ts          # Vercel serverless entry
├── src/index.ts          # Cloudflare Workers entry
├── vercel.json           # Vercel config
├── wrangler.toml         # Cloudflare config
└── package.json          # Dependencies (hono, supabase, openai)
```

### Environment Variables Required

```
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_ANON_KEY=eyJ...
OPENAI_API_KEY=sk-...
```

---

## Phase 3: Mintlify UI ✅ COMPLETE

### React Widget Components

| Component | Purpose | Location | Lines |
|-----------|---------|----------|-------|
| `SearchWidget.tsx` | Semantic search with filters | `apps/widget/src/components/` | 337 |
| `GapDashboard.tsx` | Topic × Diátaxis coverage matrix | `apps/widget/src/components/` | 273 |
| `App.tsx` | Tab navigation (search/gaps) | `apps/widget/src/` | ~90 |
| `api.ts` | API client wrapper | `apps/widget/src/` | ~70 |
| `types.ts` | TypeScript interfaces | `apps/widget/src/` | ~60 |

### SearchWidget Features

- [x] Natural language search input with debounce (300ms)
- [x] Filter panel (toggle visibility)
- [x] Diátaxis type filter buttons
- [x] Author filter buttons with counts
- [x] Topic filter buttons (top 8)
- [x] Clear filters button
- [x] Loading spinner
- [x] Error handling with user-friendly messages
- [x] Result cards with:
  - Title, author, date
  - Summary (2-line clamp)
  - Topics (up to 3)
  - Diátaxis badge (color-coded)
  - Similarity score percentage
  - Key quote preview (first quote, 150 chars)
- [x] Empty state with search tips
- [x] Example query buttons

### GapDashboard Features

- [x] Summary stat cards (total articles, topics, gaps, reference docs)
- [x] Diátaxis type legend with descriptions
- [x] Sort toggle (by coverage or gaps)
- [x] Coverage matrix table
- [x] Color-coded gap cells (red=0, yellow=1-2, blue=3-5, green=6+)
- [x] Gap warnings per row
- [x] Content suggestions based on gaps

### Mintlify Pages

| Page | Path | Embeds |
|------|------|--------|
| Semantic Search | `kb/search.mdx` | Widget with `?tab=search` |
| Browse Content | `kb/browse.mdx` | Static accordions + cards |
| Content Gaps | `kb/content-gaps.mdx` | Widget with `?tab=gaps` |

### Navigation (docs.json)

```json
{
  "tab": "Knowledge Base",
  "groups": [
    { "group": "Research", "pages": ["kb/search", "kb/browse"] },
    { "group": "Planning", "pages": ["kb/content-gaps"] }
  ]
}
```

### Deployment URLs

| Service | URL |
|---------|-----|
| Widget | `https://thought-leadership-widget.vercel.app/` |
| API | (configure in widget or use local) |

---

## Phase 4: Polish 🟡 IN PROGRESS

### Completed

| Feature | Status | Notes |
|---------|--------|-------|
| Basic quote display | ✅ Done | Shows first quote in search results |

### Completed (Phase 4)

| Feature | Status | Notes |
|---------|--------|-------|
| **Related articles** | ✅ Done | Expandable cards show 4 related articles by embedding similarity |
| **Days back parameter** | ✅ Done | `--days-back` CLI arg + `days_back` workflow input for controlling article lookback |
| **GitHub Actions permissions** | ✅ Done | Fixed `contents: write` permission for workflow push |

### Pending Tasks

| Feature | Priority | Description | Affected Files |
|---------|----------|-------------|----------------|
| **Quote copy-to-clipboard** | Medium | Add copy button next to key quotes in search results | `SearchWidget.tsx` |
| **"Use for content" workflow** | Low | Track when articles are used as sources for your own content | New component + `my_content` table |
| **Monitor and iterate** | Ongoing | Track usage, fix bugs, improve UX | — |

---

## Related Articles Feature — IMPLEMENTED ✅

### What Was Built

Added a "Related Articles" section that shows 4 similar articles based on embedding similarity when expanding an article card in search results.

### Files Changed

**API (both entry points updated):**
- `mintlify-starter/docs-assistant/apps/api/api/index.ts` — Added `GET /api/article/:id/related`
- `mintlify-starter/docs-assistant/apps/api/src/index.ts` — Added `GET /api/article/:id/related`

**Widget:**
- `mintlify-starter/docs-assistant/apps/widget/src/types.ts` — Added `RelatedArticlesResponse` type
- `mintlify-starter/docs-assistant/apps/widget/src/api.ts` — Added `getArticle()` and `getRelatedArticles()` methods
- `mintlify-starter/docs-assistant/apps/widget/src/components/RelatedArticles.tsx` — **NEW** component
- `mintlify-starter/docs-assistant/apps/widget/src/components/index.ts` — Export RelatedArticles
- `mintlify-starter/docs-assistant/apps/widget/src/components/SearchWidget.tsx` — Made ArticleCard expandable with related articles

### How It Works

1. User clicks an article card in search results
2. Card expands to show full summary, all topics, additional quotes
3. "Open article" link appears to view original
4. RelatedArticles component fetches `/api/article/:id/related`
5. API uses the article's embedding to find similar articles via `match_articles` RPC
6. 4 related articles displayed with similarity scores

### Testing

```bash
# Test API endpoint directly
curl "http://localhost:8787/api/article/YOUR_ARTICLE_UUID/related?limit=4"

# Start widget dev server
cd /Users/sonle/Github/mintlify-starter/docs-assistant/apps/widget
pnpm dev
```

---

## Quick Reference: Running Locally

### Main Project (Python)

```bash
cd /Users/sonle/Github/ai-thought-leadership
source venv/bin/activate
python scripts/supabase_sync.py --test  # Test connection
python scripts/supabase_sync.py         # Sync articles
```

### API (Hono)

```bash
cd /Users/sonle/Github/mintlify-starter/docs-assistant/apps/api
pnpm install
pnpm dev  # Runs on localhost:8787 (Wrangler)
```

### Widget (React)

```bash
cd /Users/sonle/Github/mintlify-starter/docs-assistant/apps/widget
pnpm install
pnpm dev  # Runs on localhost:5173 (Vite)
```

### Mintlify Docs

```bash
cd /Users/sonle/Github/mintlify-starter
npx mintlify dev  # Runs on localhost:3000
```

---

## Notes for Next Session

1. **Remaining Phase 4 tasks**: Quote copy-to-clipboard, "Use for content" workflow
2. **Test the workflow**: Go to GitHub Actions → Daily Content Ingestion → Run workflow
   - Use `days_back` parameter (default: 7) to control lookback period
   - Example: Set `days_back: 30` for 1 month, `90` for 3 months
3. **Deploy widget changes**: Push to mintlify-starter repo to trigger Vercel auto-deploy

---

*Last updated: 2026-02-01 (Days back parameter and permissions fix committed)*
