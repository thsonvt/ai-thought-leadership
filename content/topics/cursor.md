---
topic: Cursor
related_topics: [AI Coding Tools, Claude Code, GitHub Copilot]
---

# Cursor: Thought Evolution

## Overview

Tracking thought leadership perspectives on Cursor, the AI-first code editor.

## Timeline View

```dataview
TABLE
  author as "Author",
  published as "Date",
  stance.cursor as "Stance",
  evolution_note as "Evolution Note"
FROM "content/authors"
WHERE contains(topics, "Cursor")
SORT published ASC
```

## Key Insights

```dataview
LIST key_quotes
FROM "content/authors"
WHERE contains(topics, "Cursor")
SORT published ASC
```

## Related Topics

- [[topics/claude-code]] - Primary comparison point
- [[topics/github-copilot]] - Earlier AI coding tool
- [[topics/ai-coding-tools]] - Broader category
