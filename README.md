# Pi Coding Agent Skills

A collection of specialized skills that extend the [Pi Coding Agent](https://github.com/mariozechner/pi-coding-agent) with domain-specific capabilities.

## Skills Overview

| Skill | Description |
|-------|-------------|
| **[docx](/docx)** | Create, read, edit, and manipulate Word documents (.docx). Supports formatting, tables of contents, headers, page numbers, and tracked changes. |
| **[pdf-to-markdown](/pdf-to-markdown)** | Extract PDF files to Markdown format using pymupdf4llm. Supports text, table, and image extraction with page-chunked JSON output. |
| **[pdf-utils](/pdf-utils)** | PDF manipulation toolkit using PyMuPDF (fitz). Merge, split, rotate, watermark, encrypt, redact, extract text (plain), and convert pages to images. |
| **[playwright-cli](/playwright-cli)** | Automate browser interactions and run Playwright tests via CLI. |
| **[pptx](/pptx)** | Create, edit, and parse PowerPoint presentations. Handle slides, templates, speaker notes, and layouts. |
| **[product-catalog-downloader](/product-catalog-downloader)** | Download semiconductor product catalogs from webpages using Playwright CLI. |
| **[skill-creator](/skill-creator)** | Create new skills, improve existing ones, run evals, and optimize skill descriptions for better triggering accuracy. |
| **[xlsx](/xlsx)** | Spreadsheet operations on .xlsx, .xlsm, .csv, .tsv files. Create, edit, format, chart, clean messy data. |

## Repository Structure

```
skills/
├── docx/                   # Word document skill
├── pdf-to-markdown/        # PDF to Markdown extraction
├── pdf-utils/              # PDF manipulation (PyMuPDF)
├── playwright-cli/         # Browser automation skill
├── pptx/                   # PowerPoint skill
├── product-catalog-downloader/  # Product catalog downloader
├── skill-creator/          # Skill creation & eval tool
├── xlsx/                   # Spreadsheet skill
└── README.md
```

## Adding a Skill to Pi

Skills are YAML-based. Each skill directory should contain:

- **`SKILL.md`** — The skill definition (name, description, instructions, allowed tools, etc.)
- **`LICENSE.txt`** — (optional) License terms for the skill
- **Supporting files** — Any scripts, helpers, or assets the skill needs

### Skill Definition Format

Skills are defined as Markdown files with YAML front matter:

```markdown
---
name: my-skill
description: "What this skill does and when to use it."
allowed-tools:
  - Bash(my-skill:*)
  - Bash(helper-script:*)
---

# Instructions for the skill
...
```

### Loading Skills into Pi

Place skill directories in your Pi skills directory (default: `~/.pi/agent/skills/`). Pi will automatically detect and register them on startup.

For more details on skill creation, use the **skill-creator** skill.

## License

Individual skills may have their own licenses. See each skill's `LICENSE.txt` for terms.

## Contributing

1. Create a new skill directory with a `SKILL.md` file
2. Test it using Pi's skill evaluation tools
3. Submit a pull request or share with the community

For help creating skills, see the **[skill-creator](/skill-creator)** skill.
