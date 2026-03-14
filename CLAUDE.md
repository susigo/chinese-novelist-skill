# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository purpose

This repository is a Claude Code skill package for generating complete Chinese novels chapter by chapter. Most of the "implementation" lives in prompt/spec files and reference templates rather than application code.

## Key files

- `SKILL.md` - source of truth for the skill behavior and the end-to-end workflow.
- `README.md` - user-facing usage and installation notes.
- `references/` - operational writing guides and templates, not passive docs.
  - `outline-template.md` -> `novels/<小说名>/00-大纲.md`
  - `character-template.md` -> `novels/<小说名>/01-人物档案.md`
  - `chapter-template.md` -> per-chapter files
  - `chapter-guide.md`, `hook-techniques.md`, `dialogue-writing.md`, `consistency.md`, `quality-checklist.md` -> chapter-writing and QA rules
- `scripts/check_chapter_wordcount.py` - the only executable validation utility; it strips common Markdown and counts Chinese Han characters.
- `.claude/settings.local.json` - local permissions currently allow the `chinese-humanizer` and `skill-creator` skills.

## Common commands

There is no build, lint, CI, or automated test setup in this repository. Do not invent one. The practical validation flow is manual skill testing plus the chapter word-count script.

```bash
# Check one generated chapter against the default 3000-character minimum
python scripts/check_chapter_wordcount.py novels/小说名/第01章.md

# Check all generated chapters in a novel directory
python scripts/check_chapter_wordcount.py --all novels/小说名/

# Check with a custom minimum
python scripts/check_chapter_wordcount.py novels/小说名/第01章.md 3500
```

Manual usage from the docs:

- Install by placing this directory under `~/.claude/skills/chinese-novelist/`
- Trigger with a prompt such as `使用 chinese-novelist 帮我写一部小说`

## High-level architecture

The skill is organized as a 3-phase workflow defined in `SKILL.md`:

1. **Interactive intake** - ask 5 questions with `AskUserQuestion` to collect genre, protagonist setup, protagonist personality, core conflict, and chapter count.
2. **Planning + confirmation** - create `novels/<小说名>/`, generate `00-大纲.md` from the outline template and `01-人物档案.md` from the character template, then present a summary and wait for user confirmation.
3. **Sequential chapter generation** - create each chapter from the chapter template, update outline progress, append chapter summaries, run the word-count check, and continue chapter by chapter until completion.

## Important conventions

- `00-大纲.md` is the continuity/state file for long runs. Read completed chapter summaries and the previous chapter before writing a new one; update TODO status and append a new chapter summary after writing.
- The effective enforced chapter target is **3000-5000 Chinese characters**. Some reference docs mention broader ranges or a 2500 minimum, but `SKILL.md` and `scripts/check_chapter_wordcount.py` treat 3000 as the practical minimum.
- The chapter opening and ending are hard requirements, not optional style notes:
  - the first 20% must hook immediately with conflict, tension, or a major event
  - the ending must leave a suspense hook for the next chapter
- Generated output is expected under `novels/<小说名>/` with:
  - `00-大纲.md`
  - `01-人物档案.md`
  - `第XX章-*.md` chapter files

## When changing behavior

Because the workflow is distributed across prose instructions, templates, and one validation script, behavior changes usually require synchronized updates across multiple files:

- `SKILL.md` for the canonical workflow
- `README.md` for public-facing behavior
- the relevant files in `references/`
- `scripts/check_chapter_wordcount.py` if chapter length rules change

Keep these in sync instead of changing only one document.