# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository purpose

This repository is a Claude Code skill package for generating complete Chinese novels chapter by chapter. Most of the "implementation" lives in prompt/spec files and reference templates rather than application code.

## Key files

- `SKILL.md` - source of truth for the skill behavior and the end-to-end workflow.
- `README.md` - user-facing usage and installation notes.
- `references/` - operational writing guides and templates, not passive docs.
  - `outline-template.md` -> `novels/<小说名>/大纲/00-大纲.md`
  - `character-template.md` -> `novels/<小说名>/人物档案/01-人物档案.md`
  - `chapter-template.md` -> per-chapter files such as `novels/<小说名>/第01章-章节名.md`
  - `chapter-guide.md`, `hook-techniques.md`, `dialogue-writing.md`, `consistency.md`, `quality-checklist.md` -> chapter-writing and QA rules
  - `character-building.md`, `plot-structures.md`, `content-expansion.md` -> supplementary craft references
- `scripts/check_chapter_wordcount.py` - the only executable validation utility; it strips common Markdown and counts Chinese Han characters.
- `assets/` - example images for beginning/ending hook presentation.
- `.claude/settings.local.json` - local permissions currently allow the `chinese-humanizer` and `skill-creator` skills.
- `novels/` - working output area. The current sample project `novels/修真之创世纪/` is organized into `大纲/`, `人物档案/`, and `设定/`.

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
2. **Planning + confirmation** - create `novels/<小说名>/`, generate `大纲/00-大纲.md` from the outline template, generate `人物档案/01-人物档案.md` as the master index from the character template, create detailed role files under `人物档案/`, optionally create supporting worldbuilding notes under `设定/`, then present a summary and wait for user confirmation.
3. **Sequential chapter generation** - create each chapter from the chapter template in the novel root, update `大纲/00-大纲.md` progress, append chapter summaries, run the word-count check, and continue chapter by chapter until completion.

## Important conventions

- `novels/<小说名>/大纲/00-大纲.md` is the primary continuity/state file for long runs. Read completed chapter summaries and the previous chapter before writing a new one; update TODO status and append a new chapter summary after writing.
- `novels/<小说名>/人物档案/01-人物档案.md` is the character master index. It records where role files live and any migrations between directories.
- The effective enforced chapter target is **3000-5000 Chinese characters**. Some reference docs mention broader ranges or a 2500 minimum, but `SKILL.md` and `scripts/check_chapter_wordcount.py` treat 3000 as the practical minimum.
- The chapter opening and ending are hard requirements, not optional style notes:
  - the first 20% must hook immediately with conflict, tension, or a major event
  - the ending must leave a suspense hook for the next chapter
- Generated output is expected under `novels/<小说名>/` with:
  - `大纲/00-大纲.md`
  - optional additional outline files under `大纲/` such as `09-第一卷详细大纲-魂入边荒.md`
  - `人物档案/01-人物档案.md` as the character master index
  - `人物档案/` subdirectories for detailed character files
  - optional setting notes under `设定/`
  - chapter files in the novel root named `第XX章-*.md`
- Character archive layout conventions inside `人物档案/`:
  - long-term core roles go in `主角/`、`核心配角/`、`反派与镜像/`、`专业支柱/`、`创业班底/`、`历史人物/`、`阵营预留/`
  - temporary arc-specific roles go in `分卷角色/第X卷-卷名/`
  - directory-level `README.md` files may record roster notes and migrations
  - a role should have only one primary home at a time; if promoted from a volume directory into a long-term category, move the file and leave only a migration note in the old volume README

## When changing behavior

Because the workflow is distributed across prose instructions, templates, and one validation script, behavior changes usually require synchronized updates across multiple files:

- `SKILL.md` for the canonical workflow
- `README.md` for public-facing behavior
- the relevant files in `references/`
- `scripts/check_chapter_wordcount.py` if chapter length rules change

Keep these in sync instead of changing only one document.