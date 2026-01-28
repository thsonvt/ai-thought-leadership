# AI Thought Leadership Knowledge Base

An automated system for tracking and synthesizing AI-assisted coding thought leadership content. Built with Obsidian, Python, and GPT-4.

## Features

- ✅ **Automated Weekly Ingestion**: RSS and web scraping from 5-10+ thought leaders
- 🤖 **AI-Powered Analysis**: GPT-4 extracts topics, key quotes, stance, and evolution insights
- 📊 **Thought Evolution Timeline**: Track how perspectives change over time
- 📧 **Weekly Digest**: Automated email and Slack summaries
- 🔍 **Semantic Search**: AI-powered search via Obsidian Smart Connections
- 📝 **Cross-Referencing**: Connect ideas across authors and topics
- ⚙️ **Configurable Notifications**: Turn on/off, adjust frequency

## Quick Start

### 1. Clone and Setup

```bash
# Clone this repository
git clone https://github.com/yourusername/ai-thought-leadership.git
cd ai-thought-leadership

# Install Python dependencies
pip install -r scripts/requirements.txt

# Configure sources (edit as needed)
vim config/sources.yaml

# Configure notifications
vim config/notifications.yaml
# Update email recipients and other settings
```

### 2. Set Environment Variables

```bash
# OpenAI API key (required for GPT-4 analysis)
export OPENAI_API_KEY='sk-...'

# SendGrid API key (optional, for email notifications)
export SENDGRID_API_KEY='SG...'

# Slack webhook URL (optional, for Slack notifications)
export SLACK_WEBHOOK_URL='https://hooks.slack.com/services/...'
```

### 3. Test Manual Scraping

```bash
cd scripts

# Dry run (test without saving)
python scraper.py --dry-run

# Fetch first 5 articles
python scraper.py --limit 5
```

### 4. Set Up Obsidian

```bash
# Download Obsidian: https://obsidian.md/
# Open this folder as a vault in Obsidian

# Install required plugins:
# Settings → Community Plugins → Browse
# 1. Smart Connections (AI semantic search)
# 2. Dataview (timeline queries)
# 3. Obsidian Timeline (visual timeline)

# Configure Smart Connections:
# Settings → Smart Connections
# - Add OpenAI API key
# - Model: text-embedding-3-small
```

### 5. Set Up GitHub Actions (Optional)

```bash
# Push to GitHub
git init
git add .
git commit -m "Initial setup"
git remote add origin https://github.com/yourusername/ai-thought-leadership.git
git push -u origin main

# Add secrets in GitHub:
# Repository → Settings → Secrets and variables → Actions
# - OPENAI_API_KEY
# - SENDGRID_API_KEY
# - SLACK_WEBHOOK_URL

# GitHub Actions will run automatically every Monday at 9am UTC
```

## Usage

### Manual Scraping

```bash
cd scripts

# Fetch all new posts
python scraper.py

# Fetch with limit
python scraper.py --limit 10

# Dry run (test)
python scraper.py --dry-run
```

### Generate Digest

```bash
cd scripts

# Generate digest for last 7 days
python digest_generator.py

# Last 14 days
python digest_generator.py --days 14

# Without GPT-4 (simple digest)
python digest_generator.py --no-gpt4
```

### Send Notifications

```bash
cd scripts

# Send email and Slack notifications
python notification_sender.py

# Test configuration
python notification_sender.py --test
```

### Obsidian Workflows

1. **Semantic Search**: Use Smart Connections to ask questions
   - Cmd/Ctrl + P → "Smart Connections: Chat"
   - Ask: "What does Jesse think about Claude Code vs Cursor?"

2. **Browse Timeline**: Open a topic MOC (e.g., `content/topics/claude-code.md`)
   - View chronological evolution
   - See all related posts

3. **Daily Synthesis**: Create synthesis notes in `content/synthesis/`
   - Link to related posts
   - Add your own insights

## Configuration

### Add New Sources

Edit `config/sources.yaml`:

```yaml
sources:
  - name: Your Author
    id: your-author
    url: https://blog.example.com/
    type: blog
    rss: https://blog.example.com/feed.xml
    tags: [ai, coding]
    active: true
```

### Adjust Notifications

Edit `config/notifications.yaml`:

```yaml
notifications:
  enabled: true
  frequency: weekly  # daily, weekly, biweekly, monthly

  email:
    enabled: true
    recipients:
      - your.email@example.com

  slack:
    enabled: true
    channel: "#ai-research"
```

### Customize Topics

Edit `config/topics.yaml` to add pre-defined topics for better organization.

## Project Structure

```
ai-thought-leadership/
├── .github/workflows/      # GitHub Actions automation
│   ├── weekly-ingestion.yml
│   └── manual-digest.yml
├── content/
│   ├── authors/            # Blog posts organized by author
│   ├── topics/             # MOCs (Maps of Content)
│   └── synthesis/          # Weekly digests and manual synthesis
├── scripts/                # Python automation scripts
│   ├── scraper.py          # Main scraper
│   ├── content_processor.py # GPT-4 analysis
│   ├── digest_generator.py  # Weekly digest
│   ├── notification_sender.py
│   └── requirements.txt
├── config/                 # Configuration files
│   ├── sources.yaml        # Content sources
│   ├── notifications.yaml  # Notification settings
│   └── topics.yaml         # Topic taxonomy
└── .obsidian/             # Obsidian configuration
```

## Thought Evolution Timeline

The system tracks how thought leaders' perspectives evolve over time:

1. **During Ingestion**: GPT-4 extracts:
   - Topics discussed
   - Key quotes with context
   - Stance on tools/concepts (positive/neutral/negative)
   - Evolution note (where this fits in their journey)

2. **In Topic MOCs**: Dataview queries display chronologically:
   ```dataview
   TABLE author, published, stance.claude_code, evolution_note
   FROM "content/authors"
   WHERE contains(topics, "Claude Code")
   SORT published ASC
   ```

3. **Visual Timeline**: Use Obsidian Timeline plugin for graph view

**Example Timeline**:
```
📅 2024-01-15: "Cursor feels more natural" (🟡 Neutral)
📅 2024-02-10: "Claude Code changed my workflow" (🟢 Positive)
📅 2024-03-05: "Can't build agent-native with Cursor" (🟢 Strong)

Evolution: Surface comparison → Workflow impact → Architectural philosophy
```

## Cost Estimation

| Service | Monthly Cost |
|---------|-------------|
| OpenAI (embeddings + GPT-4) | $5-10 |
| SendGrid (email) | $0 (free tier) |
| Slack (webhooks) | $0 |
| GitHub Actions | $0 (free tier) |
| **Total** | **~$5-10/month** |

## Customization

### Scraper Logic

Customize `scripts/scraper.py` for specific blog structures:

```python
def scrape_single_article(url, source):
    # Add custom selectors
    article_elem = soup.find(source.get('scrape_selector', 'article'))
```

### GPT-4 Prompts

Customize `scripts/content_processor.py` to extract different metadata:

```python
prompt = f"""
Extract custom fields:
- technical_depth: beginner|intermediate|advanced
- code_examples: true|false
...
"""
```

## Troubleshooting

### No New Posts Found

- Check `config/sources.yaml` - ensure `active: true`
- Verify RSS URLs are valid
- Check if posts are recent (within date range)

### GPT-4 Errors

- Verify `OPENAI_API_KEY` is set
- Check API quota/credits
- Review error logs

### Email Not Sending

- Verify `SENDGRID_API_KEY` is set
- Check `config/notifications.yaml` recipients
- Ensure SendGrid account is verified

### Obsidian Plugins Not Working

- Ensure plugins are enabled: Settings → Community Plugins
- Smart Connections needs OpenAI API key configured
- Restart Obsidian after plugin installation

## Contributing

This is a personal knowledge base, but feel free to:
- Fork and customize for your own use
- Suggest improvements via issues
- Share your experience and learnings

## License

MIT License - feel free to use and modify for your own knowledge management needs.

## Acknowledgments

Inspired by thought leaders in AI-assisted coding:
- Jesse Chen (blog.fsck.com)
- Naveen Naidu (naveennaidu.com)
- Kieran Klaassen (kieranklaassen.com)
- Dan Shipper (every.to)
- Anthropic Engineering team

---

**Built with**: Obsidian, Python, OpenAI GPT-4, GitHub Actions
