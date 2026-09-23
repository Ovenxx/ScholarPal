# ScholarPal

Two research areas I follow: LLMs applied to optimization (LLM4OR / L2O), and agentic AI. Three jobs run each morning, collect new papers and industry news, and commit the result here. A small web page reads that output.

https://ovenxx.github.io/ScholarPal/

## What runs

| time (Asia/Shanghai) | job |
|---|---|
| 06:00 | papers for LLM4OR / L2O |
| 06:20 | papers for agentic AI |
| 06:30 | industry news, then the data the page needs |

All three share a concurrency group, so they run one after another and their commits do not collide.

## The page

Trending topics on the left, academic and industry. A feed on the right with three tabs: the two paper lists and industry news.

Each item gets an importance score from the model, a one line summary, tags and a link. You can mark it interested or not interested and leave a note. Those marks build an interest profile which reorders the feed, so things similar to what you marked move up. Nothing gets hidden, only reordered.

First visit asks you to tick a handful of items, because with no history there is nothing to rank against.

Your notes are private.

## What is borrowed, what is mine

All the collection work is third party. I wrote glue and config.

Papers come from [cv-arxiv-daily](https://github.com/Vincentqyw/cv-arxiv-daily), which queries arXiv and renders a markdown list. I hand it two keyword files and give each one its own output directory. The workflow clones it at a pinned commit and never checks it in.

News comes from [TrendRadar](https://github.com/sansan0/TrendRadar), which crawls feeds and hot lists, caches them in SQLite and does its own keyword filtering. Same arrangement, pinned and cloned at run time, with two of its config files replaced by mine.

`tools/build_feed.py` is mine. It reads the two paper stores and TrendRadar's database, sends a few batches to deepseek-v4-flash, and writes `docs/feed.json` with a score and a summary for each item plus the trending themes.

`docs/index.html` is one file with no dependencies. It fetches feed.json and does the ranking, likes and notes in the browser.

## Cost

About five model calls a day.

Keyword filtering happens first, so only the top 18 items per topic reach the model. Reasoning is switched off, and that matters: with it on the same request produced 201 output tokens instead of 38.

## Using it on a second device

The profile lives in the browser, so by default it stays on one machine. To sync, the page needs permission to read and write a private repo, `ScholarPal-memory`.

1. Go to https://github.com/settings/personal-access-tokens/new
2. Repository access: only select repositories, then pick `ScholarPal-memory`
3. Repository permissions, Contents: read and write
4. Generate, copy the token
5. Open the page, click "Connect memory" at the top right, paste it

The token is kept in that browser's local storage. It is never in the page source. Do this once per device.

## Layout

```
config/           keyword files for the two paper lists
news/config/      TrendRadar config and keywords
tools/build_feed.py
docs/index.html   the page
docs/feed.json    generated daily
docs/llm4or/      generated paper list
docs/agentic/     generated paper list
.github/workflows/
```

## Things that will bite you

Trending topics are a morning snapshot. There is no server behind this, so nothing changes during the day. If you want a live board you need to host something.

News keywords match against titles only. An item whose body is relevant but whose title is not gets missed.

TrendRadar has a switch for hot list platforms. Turning it off does not just drop those platforms, it makes the whole run exit early and skip the feeds as well. It has to stay on. This is written down in `news/README.md` because I lost time to it.

The paper engine merges new papers into its JSON store rather than replacing it, so the generated lists keep growing.

The Code column in the paper lists is always null. Upstream retired the API that used to fill it.

## License

GPL-3.0, because TrendRadar is GPL-3.0 and this repo incorporates it. See [LICENSE](LICENSE). Upstream authors are credited in [ATTRIBUTION.md](ATTRIBUTION.md).
