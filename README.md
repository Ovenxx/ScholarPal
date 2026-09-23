# ScholarPal

> One list, one digest, one place — a daily tracker for **LLM4OR / L2O** and **Agentic AI**.
> Assembled from existing open-source projects. No crawler or aggregation engine written from scratch.

**Open it → <https://ovenxx.github.io/ScholarPal/>**

---

## What you get

A two-pane web app:

**Left pane — trending topics**
- **Academic** — themes distilled from the day's candidate papers, each with a short explanation
- **Industry** — themes distilled from the day's industry feeds

**Right pane — feed**, three tabs:

| Tab | Scope |
|---|---|
| `LLM4OR / L2O` | LLMs for optimization: automatic algorithm design (FunSearch / ReEvo / evolutionary heuristics), auto-formulation, learned optimizers, vehicle routing and combinatorial solving, solver intelligence |
| `Agentic AI` | Agent loops, context engineering, tool protocols, multi-agent orchestration, memory, planning and self-evolution |
| `Industry` | Engineering and industry news beyond papers (paper feeds are excluded here to avoid duplication) |

Every card carries a **model-assigned importance score**, a **one-line summary**, tags, a link to the source, and **Like / Dislike / Comment** actions.

**Personalization.** Likes and comments accumulate into a long-term interest profile, shown at the top of the left pane, which pushes relevant work to the top and highlights it. A short guided onboarding runs on first visit to solve the cold start. Comments are private — only you can see them.

Everything refreshes automatically **from 06:00 Asia/Shanghai daily**. Nothing to run by hand.

---

## The three data modules

| Module | Content | Output |
|---|---|---|
| **A · LLM4OR / L2O** | Keyword-filtered paper list | [`docs/llm4or/README.md`](docs/llm4or/README.md) |
| **B · Agentic AI** | Keyword-filtered paper list | [`docs/agentic/README.md`](docs/agentic/README.md) |
| **C · Industry + site build** | Industry feeds, trending-topic extraction, card scoring and summaries, page generation | `docs/news.html` · `docs/feed.json` |

Module C does the news crawl and the site build in the same job, because it needs direct access to the data the news engine produces at run time.

---

## Architecture: what we compose, what we don't build

```
        +------------ ScholarPal (this repo) -------------+
arXiv --+  config/*.yml ----> docs/llm4or/  docs/agentic/ |
        |                                                 |
RSS ----+  news/config/* ---> (news engine) -> docs/news.html
        |                          |                      |
        |                          v                      |
        |                tools/build_feed.py -> docs/feed.json
        |                          |                      |
        |                          v                      |
        |                docs/index.html (the app)        |
        +-------------------------------------------------+
                              |
                  private store: ScholarPal-memory
```

| Layer | Existing project used | What we actually wrote |
|---|---|---|
| **Paper engine** | [Vincentqyw/cv-arxiv-daily](https://github.com/Vincentqyw/cv-arxiv-daily) (Apache-2.0) | Two keyword configs. The engine is **fetched at a pinned revision at run time, never vendored** |
| **News engine** | [sansan0/TrendRadar](https://github.com/sansan0/TrendRadar) (GPL-3.0) | One derived config plus a keyword file. Also **fetched at run time, never vendored** |
| **Topics / scoring / summaries** | DeepSeek `deepseek-v4-flash` | One ~250-line build script, `tools/build_feed.py` |
| **Web app** | none — dependency-free vanilla page | A single file, `docs/index.html` |
| **Memory store** | A private GitHub repository | Cross-device sync of likes and comments |

---

## Cross-device memory (optional, one-time setup)

The app works without this; likes and comments simply stay in that one browser. To sync across devices, give the page a narrowly scoped token:

1. Open <https://github.com/settings/personal-access-tokens/new>
2. **Repository access** → `Only select repositories` → select **ScholarPal-memory**
3. **Permissions → Repository permissions → Contents** → set to **Read and write**
4. Generate and copy the token
5. Open the app → **"Connect memory"** in the top-right → paste it

The token is stored only in that device's browser storage; it never appears in the page source. Repeat once per device.

---

## Schedule

| Job | Time (Asia/Shanghai) | Manual trigger name |
|---|---|---|
| Module A · LLM4OR / L2O | 06:00 | `ScholarPal - Module A (LLM4OR/L2O) daily` |
| Module B · Agentic AI | 06:20 | `ScholarPal - Module B (Agentic AI) daily` |
| Module C · News + site build | 06:30 | `ScholarPal - Module C (News + Site build) daily` |

All three share one concurrency group and therefore run serially, so their commits cannot race.

**Reproducing the build locally** (requires an `AI_API_KEY` environment variable):

```bash
pip install arxiv requests pyyaml    # dependencies of the paper engine
AI_API_KEY=... python tools/build_feed.py
```

---

## Repository layout

```
ScholarPal/
├─ README.md
├─ ATTRIBUTION.md              # upstream credits
├─ LICENSE                     # GPL-3.0
├─ config/                     # module A / B keywords
│  ├─ llm4or.yml
│  └─ agentic.yml
├─ news/
│  ├─ README.md                # news layer notes
│  └─ config/
│     ├─ config.yaml           # derived from the upstream full config
│     └─ frequency_words.txt   # news keywords
├─ tools/
│  └─ build_feed.py            # topic extraction, scoring, summaries
├─ docs/
│  ├─ index.html               # the web app (hand-written, never overwritten)
│  ├─ feed.json                # generated daily
│  ├─ news.html                # raw report from the news engine
│  ├─ llm4or/                  # module A output
│  └─ agentic/                 # module B output
└─ .github/workflows/
   ├─ llm4or-daily.yml
   ├─ agentic-daily.yml
   └─ news-daily.yml
```

---

## Design decisions

**Cost.** Five model calls a day. Candidates are filtered by keyword first, then only the top 18 per column reach the model; reasoning is disabled, which cuts the same request from 201 tokens to 38 — roughly a 5x saving.

**Personalization lives in the browser, not on a server.** The site is static and public, so the interest profile is computed locally and re-ranking happens at view time; the cloud only classifies and summarizes. The memory itself sits in a **private** repository, which is why comments stay private.

**Why not a third-party backend.** Cross-device sync needs exactly one credential, and you already have a GitHub account — no new service to sign up for.

---

## Known limitations

- **Trending topics are a daily snapshot, not a live board.** A static site has no running server; true rolling updates would require one.
- **News keywords match on titles only.** Items whose body is relevant but whose title lacks the keyword will be missed. Enabling the news engine's AI filter mitigates this.
- **The paper engine's output accumulates.** It merges history into `data.json`, so the generated files grow daily. The `Code` column is always `null` because upstream retired the related API.
- **The news engine requires its hot-list switch to stay on.** Turning it off makes the whole pipeline short-circuit and skip even the RSS feeds. This is documented in `news/README.md`.

---

## License

Released under **GPL-3.0**; see [`LICENSE`](LICENSE).

GPL-3.0 rather than a more permissive license because the news engine this project incorporates is GPL-3.0, whose terms require derivative works to carry the same license. That was the trade-off accepted when choosing to merge everything into a single platform.

Upstream authors and licenses are listed in [`ATTRIBUTION.md`](ATTRIBUTION.md). This repository contains no upstream source code.
