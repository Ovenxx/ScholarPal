# Attribution and licensing

This repository **contains no upstream source code**. Both upstream projects are fetched at run time at a pinned revision; the clone directories are excluded via `.gitignore`.

## Vincentqyw/cv-arxiv-daily

- **Role**: daily paper engine for modules A / B
- **License**: Apache License 2.0
- **Source**: <https://github.com/Vincentqyw/cv-arxiv-daily>
- **Pinned revision**: `2c6fa8569db604f448adb82124a2e352c78da6b0`
- **How it is used**: fetched into `.engine/` at run time by `.github/workflows/{llm4or,agentic}-daily.yml`
- **Our changes to it**: **none to its source.** Keywords and output paths are supplied through `config/*.yml`. The workflows additionally apply a one-line compatibility shim to its **dependency** (`arxiv` 2.x removed the API the engine calls); that is a dependency adaptation, not a modification of upstream code.

## sansan0/TrendRadar

- **Role**: news aggregation engine for module C
- **License**: **GNU GPL-3.0**
- **Source**: <https://github.com/sansan0/TrendRadar>
- **Pinned revision**: `792bcc3928b1617bba09df34989fd5675c159b86`
- **How it is used**: fetched into `.news/` at run time by `.github/workflows/news-daily.yml`
- **Our changes to it**: **none to its source.** Two config files are overlaid from `news/config/` — `config.yaml`, derived from the upstream full config with only switches and the feed list changed, and `frequency_words.txt`.
- **Note**: upstream ships a 7-day check-in mechanism inside its own Actions workflow and recommends a Docker deployment for long-term use. This project uses its own workflow on a low-frequency, once-daily schedule.

## GPL-3.0 propagation

Because TrendRadar is incorporated, this repository as a whole is released under GPL-3.0. That is the licensing trade-off implied by the decision to merge everything into a single platform.

## Reference lists (linked only; no content copied)

- <https://github.com/xianchaoxiu/LLM4OR>
- <https://github.com/punkpeye/awesome-mcp-servers>
- <https://github.com/a2aproject/A2A>
- <https://github.com/e2b-dev/awesome-ai-agents>

## Data sources

Paper metadata comes from arXiv; news items come from the configured feeds. Both are used under their respective terms of service.
