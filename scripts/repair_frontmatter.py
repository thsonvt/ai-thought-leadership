#!/usr/bin/env python3
"""
Repair Frontmatter - Fixes malformed YAML frontmatter in existing markdown files
"""

import re
import yaml
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent


def extract_frontmatter_raw(content: str) -> tuple[str, str]:
    """
    Extract raw frontmatter and body from markdown content.
    Returns (frontmatter_text, body_text)
    """
    if not content.startswith('---'):
        return '', content

    # Find the closing ---
    lines = content.split('\n')
    end_idx = None

    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == '---':
            end_idx = i
            break

    if end_idx is None:
        return '', content

    frontmatter_text = '\n'.join(lines[1:end_idx])
    body_text = '\n'.join(lines[end_idx + 1:])

    return frontmatter_text, body_text


def parse_malformed_frontmatter(fm_text: str) -> dict:
    """
    Parse malformed frontmatter by extracting fields manually.
    """
    data = {}

    # Extract simple fields using regex
    patterns = {
        'title': r'^title:\s*"(.+)"',
        'author': r'^author:\s*(.+?)$',
        'author_id': r'^author_id:\s*(.+?)$',
        'url': r'^url:\s*(.+?)$',
        'published': r'^published:\s*(.+?)$',
        'fetched': r'^fetched:\s*(.+?)$',
        'evolution_note': r'^evolution_note:\s*"(.+)"',
    }

    for field, pattern in patterns.items():
        match = re.search(pattern, fm_text, re.MULTILINE)
        if match:
            data[field] = match.group(1).strip()

    # Extract topics (list format)
    topics_match = re.search(r"^topics:\s*\[(.+?)\]", fm_text, re.MULTILINE)
    if topics_match:
        topics_str = topics_match.group(1)
        # Parse the list items
        data['topics'] = [t.strip().strip("'\"") for t in topics_str.split(',')]

    # Extract tags (list format)
    tags_match = re.search(r"^tags:\s*\[(.+?)\]", fm_text, re.MULTILINE)
    if tags_match:
        tags_str = tags_match.group(1)
        data['tags'] = [t.strip().strip("'\"") for t in tags_str.split(',')]

    # Extract key_quotes (complex multi-line)
    key_quotes = []
    # Find all quote blocks
    quote_pattern = r"-\s*(?:context|text):\s*(.+?)(?=\n\s*-|\n\s*stance:|$)"

    # Try to find key_quotes section
    kq_start = fm_text.find('key_quotes:')
    if kq_start != -1:
        # Find where stance: starts (end of key_quotes section)
        stance_start = fm_text.find('\nstance:', kq_start)
        if stance_start == -1:
            stance_start = fm_text.find('\nevolution_note:', kq_start)

        if stance_start != -1:
            kq_section = fm_text[kq_start:stance_start]
        else:
            kq_section = fm_text[kq_start:]

        # Parse individual quotes
        current_quote = {}
        for line in kq_section.split('\n'):
            line = line.strip()
            if line.startswith('- text:') or line.startswith('text:'):
                if current_quote and 'text' in current_quote:
                    key_quotes.append(current_quote)
                    current_quote = {}
                text_val = line.split(':', 1)[1].strip().strip("'\"")
                current_quote['text'] = text_val
            elif line.startswith('- context:') or line.startswith('context:'):
                context_val = line.split(':', 1)[1].strip().strip("'\"")
                current_quote['context'] = context_val
            elif 'text' in current_quote and line and not line.startswith('-') and not line.startswith('key_quotes'):
                # Continuation of previous field
                if 'context' in current_quote:
                    current_quote['context'] += ' ' + line.strip("'\"")
                else:
                    current_quote['text'] += ' ' + line.strip("'\"")

        if current_quote and 'text' in current_quote:
            key_quotes.append(current_quote)

    data['key_quotes'] = key_quotes

    # Extract stance (may be malformed)
    stance = {}
    stance_start = fm_text.find('\nstance:')
    if stance_start != -1:
        evo_start = fm_text.find('\nevolution_note:', stance_start)
        if evo_start != -1:
            stance_section = fm_text[stance_start:evo_start]
        else:
            stance_section = fm_text[stance_start:]

        # Parse stance lines like "AI_Agents: positive"
        for line in stance_section.split('\n'):
            line = line.strip()
            if ':' in line and line != 'stance:':
                parts = line.split(':')
                if len(parts) == 2:
                    key = parts[0].strip()
                    val = parts[1].strip()
                    if val in ['positive', 'negative', 'neutral', 'critical']:
                        stance[key] = val

    data['stance'] = stance

    return data


def repair_file(filepath: Path) -> bool:
    """
    Repair a single markdown file's frontmatter.
    Returns True if file was modified.
    """
    content = filepath.read_text()

    # Extract raw frontmatter and body
    fm_text, body = extract_frontmatter_raw(content)

    if not fm_text:
        print(f"  No frontmatter found: {filepath.name}")
        return False

    # Try to parse with standard YAML first
    try:
        data = yaml.safe_load(fm_text)
        if data:
            print(f"  Already valid: {filepath.name}")
            return False
    except yaml.YAMLError:
        pass

    # Parse malformed frontmatter
    print(f"  Repairing: {filepath.name}")
    data = parse_malformed_frontmatter(fm_text)

    if not data.get('title'):
        print(f"    Could not extract title, skipping")
        return False

    # Rebuild the file with proper frontmatter
    new_frontmatter = yaml.dump(data, default_flow_style=False, allow_unicode=True, sort_keys=False)
    new_content = f"---\n{new_frontmatter}---\n{body}"

    filepath.write_text(new_content)
    print(f"    ✅ Repaired")
    return True


def repair_all_files():
    """Repair all markdown files in content/authors/"""
    print("🔧 Repairing Frontmatter")
    print("=" * 50)

    authors_dir = PROJECT_ROOT / 'content' / 'authors'
    if not authors_dir.exists():
        print(f"❌ Authors directory not found: {authors_dir}")
        return

    md_files = list(authors_dir.glob('**/*.md'))
    print(f"\nFound {len(md_files)} markdown files\n")

    repaired = 0
    failed = 0

    for filepath in md_files:
        try:
            if repair_file(filepath):
                repaired += 1
        except Exception as e:
            print(f"  ❌ Error: {e}")
            failed += 1

    print("\n" + "=" * 50)
    print(f"✅ Complete!")
    print(f"   Repaired: {repaired}")
    print(f"   Failed: {failed}")
    print(f"   Already valid: {len(md_files) - repaired - failed}")


if __name__ == '__main__':
    repair_all_files()
