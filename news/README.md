# News layer (module C)

Driven by [TrendRadar](https://github.com/sansan0/TrendRadar). Tracks AI and large-model developments beyond papers.

- **Config**: `config/config.yaml` (derived from the upstream full config — only switches and the feed list changed) and `config/frequency_words.txt`
- **Runs**: `.github/workflows/news-daily.yml`, daily at 06:30 Asia/Shanghai
- **Consumed by**: `tools/build_feed.py`, which reads the engine's SQLite store at run time and writes `docs/feed.json`
- **Engine**: fetched at a pinned revision at run time; never copied into this repository

## Switch states

| Feature | State | Note |
|---|---|---|
| Hot-search platforms | **On (required)** | See the gotcha below; trimmed to three Chinese platforms |
| RSS feeds | On | arXiv cs.AI / cs.MA / cs.LG / math.OC, plus Hacker News |
| Keyword filter | On | Defined in `config/frequency_words.txt`; costs no model tokens |
| AI filter / translation | Off | Requires an API key |
| Push notifications | Off | No channel configured |

## Gotcha: the hot-search switch must stay on

Upstream **short-circuits** when `platforms.enabled: false`: it loads the config and exits without fetching even the RSS feeds, and produces no report at all. This was confirmed by experiment.

That switch therefore has to remain `true` in `config.yaml`. To limit unrelated noise the platform list was trimmed; on the display side `display.regions.hotlist` stays `false`, so hot-search items only surface when one of our keywords matches.

## Which part of the store we read

The engine writes two separate sets of tables:

- `news_items` — hot-search entries from the Chinese platforms. **Deliberately ignored**: general-interest material rather than AI/OR signal.
- `rss_items` — feed entries with summary and publication time. **This is what we read**, excluding arXiv feeds, because those papers already arrive in far richer form through modules A and B.

## Why the raw engine report is not published

The engine only emits a Chinese-language HTML page, while the public site is English-only. That report is therefore not published; the app's **Industry** tab carries the same material with English summaries.

## Enabling the engine's own AI filter and translation

1. Add `AI_API_KEY` under Settings → Secrets and variables → Actions
2. Set `ai_analysis.enabled` and `ai_translation.enabled` to `true` in `config/config.yaml`
3. The model defaults to `deepseek/deepseek-v4-flash`; change it under `ai.model`

With those enabled the engine filters, translates and summarizes its own content — its main advantage over pure keyword matching. Note that this affects only the engine's own report, not `docs/feed.json`.
