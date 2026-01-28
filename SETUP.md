# Setup Guide - Step by Step

Complete walkthrough for setting up the AI Thought Leadership Knowledge Base.

## Prerequisites

- Python 3.11+ installed
- Git installed
- Obsidian downloaded (https://obsidian.md/)
- GitHub account (for automation)
- OpenAI API account with credits

## Step 1: Repository Setup (5 minutes)

```bash
# Navigate to the project
cd ~/Github/ai-thought-leadership

# Initialize git repository
git init
git add .
git commit -m "Initial setup: AI Thought Leadership KB"

# Create GitHub repository (via GitHub.com UI or gh CLI)
# Then push:
git remote add origin https://github.com/YOUR_USERNAME/ai-thought-leadership.git
git push -u origin main
```

## Step 2: Python Environment (5 minutes)

```bash
# Option A: Using venv
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Option B: Using system Python (simpler)
# (No virtual environment needed)

# Install dependencies
pip install -r scripts/requirements.txt

# Verify installation
pip list | grep feedparser
pip list | grep openai
```

## Step 3: OpenAI API Setup (3 minutes)

1. Go to https://platform.openai.com/api-keys
2. Create new API key
3. Copy the key (starts with `sk-...`)

```bash
# Set environment variable (temporary)
export OPENAI_API_KEY='sk-your-key-here'

# Or add to shell profile for persistence:
echo 'export OPENAI_API_KEY="sk-your-key-here"' >> ~/.zshrc
source ~/.zshrc  # Reload

# Verify
echo $OPENAI_API_KEY
```

## Step 4: Configure Sources (5 minutes)

```bash
# Edit sources configuration
vim config/sources.yaml
# Or use any text editor

# Verify sources are active:
# - Jesse Chen: active: true
# - Naveen Naidu: active: true
# - Kieran Klaassen: active: true
# - Dan Shipper: active: true
# - Anthropic Engineering: active: true

# Add your own sources if desired
```

## Step 5: Configure Notifications (3 minutes)

```bash
# Edit notification settings
vim config/notifications.yaml

# Update:
# - Email recipients (your email)
# - From email (your domain)
# - Frequency (weekly recommended)

# For now, you can disable email/Slack if not ready:
email:
  enabled: false
slack:
  enabled: false
```

## Step 6: Test Scraping (10 minutes)

```bash
cd scripts

# Test with dry run first
python scraper.py --dry-run

# If successful, fetch first 5 articles
python scraper.py --limit 5

# Check results
ls -la ../content/authors/*/

# Should see markdown files created
```

Expected output:
```
🔍 AI Thought Leadership Scraper
==================================================
Configured sources: 5

📰 Processing: Jesse Chen
  Fetching RSS: https://blog.fsck.com/feed.xml
  Found 10 posts
  ✨ New article: Claude Code vs Cursor...
    Processing with GPT-4...
    Saved: content/authors/jesse-chen/2024-01-15-claude-code-vs-cursor-a1b2c3d4.md

...

✅ Complete!
  New articles: 5
  Skipped (existing): 0
```

## Step 7: Obsidian Setup (10 minutes)

1. **Open Vault**
   - Launch Obsidian
   - "Open folder as vault"
   - Select: `~/Github/ai-thought-leadership`

2. **Enable Community Plugins**
   - Settings (⚙️) → Community plugins
   - Turn off "Restricted mode"
   - Click "Browse"

3. **Install Required Plugins**
   - Search and install:
     - **Smart Connections** (by Brian Petro)
     - **Dataview** (by Michael Brenan)
     - **Obsidian Timeline** (by George  Xanthoudakis)

4. **Configure Smart Connections**
   - Settings → Smart Connections
   - API Provider: OpenAI
   - API Key: (paste your OpenAI key)
   - Model: text-embedding-3-small
   - Enable: Smart Chat View

5. **Verify Setup**
   - Open `content/topics/claude-code.md`
   - Should see Dataview tables render
   - Cmd/Ctrl + P → "Smart Connections: Chat"
   - Try asking: "What topics are covered?"

## Step 8: GitHub Actions Setup (10 minutes)

1. **Add GitHub Secrets**
   - Go to your repo on GitHub.com
   - Settings → Secrets and variables → Actions
   - Click "New repository secret"

   Add these secrets:
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `SENDGRID_API_KEY`: (optional, for email)
   - `SLACK_WEBHOOK_URL`: (optional, for Slack)

2. **Enable Actions**
   - Actions tab → "I understand my workflows, go ahead and enable them"

3. **Test Manual Run**
   - Actions tab → "Weekly Content Ingestion"
   - "Run workflow" → "Run workflow"
   - Wait for completion (~2-3 minutes)
   - Check if new commits appeared

## Step 9: Email Setup (Optional, 10 minutes)

Skip if not using email notifications.

1. **SendGrid Account**
   - Go to https://sendgrid.com/
   - Sign up for free account (100 emails/day free)
   - Verify your email

2. **Create API Key**
   - Settings → API Keys
   - Create API Key
   - Copy key (starts with `SG.`)

3. **Set Environment Variable**
   ```bash
   export SENDGRID_API_KEY='SG.your-key-here'
   # Or add to ~/.zshrc for persistence
   ```

4. **Update Config**
   ```bash
   vim config/notifications.yaml
   # Set email.enabled: true
   # Update recipients
   # Update from_email
   ```

5. **Test**
   ```bash
   cd scripts
   python notification_sender.py --test
   ```

## Step 10: Slack Setup (Optional, 5 minutes)

Skip if not using Slack notifications.

1. **Create Incoming Webhook**
   - Go to your Slack workspace
   - https://api.slack.com/apps
   - "Create New App" → "From scratch"
   - App Name: "AI Thought Leadership"
   - Select workspace

2. **Enable Incoming Webhooks**
   - Features → Incoming Webhooks → Toggle "On"
   - "Add New Webhook to Workspace"
   - Select channel (e.g., #ai-research)
   - Copy Webhook URL

3. **Set Environment Variable**
   ```bash
   export SLACK_WEBHOOK_URL='https://hooks.slack.com/services/...'
   # Or add to ~/.zshrc
   ```

4. **Update Config**
   ```bash
   vim config/notifications.yaml
   # Set slack.enabled: true
   # Update channel name (for display)
   ```

5. **Test**
   ```bash
   cd scripts
   python notification_sender.py --test
   ```

## Step 11: Generate First Digest (5 minutes)

```bash
cd scripts

# Generate digest from articles scraped so far
python digest_generator.py

# Check output
cat ../content/synthesis/weekly-digests/*.md

# If email/Slack enabled, send notifications
python notification_sender.py
```

## Step 12: Verification Checklist

- [ ] Python scripts run without errors
- [ ] At least 5 articles scraped and saved
- [ ] Articles have proper frontmatter (topics, quotes, stance)
- [ ] Obsidian vault opens without errors
- [ ] Smart Connections plugin works (can chat)
- [ ] Dataview tables render in topic MOCs
- [ ] GitHub Actions workflow runs successfully
- [ ] Weekly digest generated
- [ ] (Optional) Email notifications received
- [ ] (Optional) Slack notifications received

## Troubleshooting

### "Module not found" errors

```bash
# Reinstall dependencies
pip install -r scripts/requirements.txt --force-reinstall
```

### "OpenAI API error"

```bash
# Verify key is set
echo $OPENAI_API_KEY

# Check if key is valid
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY" | head -20
```

### Obsidian plugins not loading

- Settings → Community plugins → Reload
- Restart Obsidian
- Ensure "Restricted mode" is OFF

### GitHub Actions failing

- Check secrets are set correctly (no extra spaces)
- View workflow logs for specific error
- Ensure repository has write permissions

### Scraper finds no new posts

- Check if blogs have recent posts (published in last 7 days)
- Verify RSS URLs are correct
- Try with `--limit 50` to go back further

## Next Steps

### Daily Usage

1. **Browse Content**: Open Obsidian, explore `content/authors/`
2. **Search**: Use Smart Connections Chat (Cmd+P → Smart Connections)
3. **Track Evolution**: Open topic MOCs to see timelines

### Weekly (Automated)

- GitHub Actions runs every Monday at 9am UTC
- New posts ingested automatically
- Weekly digest generated
- Notifications sent

### Monthly Maintenance (30 min)

- Review and update topic MOCs manually
- Add new sources to `config/sources.yaml`
- Clean up any broken links
- Create synthesis notes

## Customization Ideas

### Add More Sources

```yaml
# config/sources.yaml
  - name: Simon Willison
    id: simon-willison
    url: https://simonwillison.net/
    rss: https://simonwillison.net/atom/everything/
    tags: [ai, llm]
    active: true
```

### Change Scraping Frequency

```yaml
# .github/workflows/weekly-ingestion.yml
on:
  schedule:
    - cron: '0 9 * * *'  # Daily instead of weekly
```

### Custom GPT-4 Prompts

Edit `scripts/content_processor.py` to extract different metadata fields.

### Different Notification Schedule

```yaml
# config/notifications.yaml
notifications:
  frequency: daily  # Instead of weekly
```

## Getting Help

- Check `README.md` for common issues
- Review GitHub Actions logs for automation errors
- Test scripts locally before relying on automation
- OpenAI API docs: https://platform.openai.com/docs

---

**Estimated Total Setup Time**: 60-90 minutes (including optional steps)
