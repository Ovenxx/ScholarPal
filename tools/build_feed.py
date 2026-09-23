#!/usr/bin/env python3
"""ScholarPal: build docs/feed.json for the web app.

Pipeline (coarse -> fine, to keep LLM cost tiny):
  1. load papers already filtered by keyword by the arxiv engine
  2. load news items from TrendRadar's SQLite store
  3. ONE LLM call per module  -> importance score + one-line summary + tags
  4. ONE LLM call per panel   -> hot-topic summary (academic / industry)
  5. write docs/feed.json

Only deepseek-v4-flash is used, with reasoning disabled (much cheaper).
"""
import datetime
import glob
import json
import os
import re
import sqlite3
import sys
import urllib.error
import urllib.request

API = "https://api.deepseek.com/v1/chat/completions"
MODEL = "deepseek-v4-flash"
KEY = os.environ.get("AI_API_KEY", "").strip()
TOP_N = int(os.environ.get("TOP_N", "18"))
NEWS_MAX = int(os.environ.get("NEWS_MAX", "40"))

MODULES = [
    ("llm4or", "LLM4OR / L2O", "docs/llm4or/data.json"),
    ("agentic", "Agentic AI", "docs/agentic/data.json"),
]

PAPER_RE = re.compile(r"\|(.*?)\|(.*?)\|(.*?)\|\[(.*?)\]\((.*?)\)\|(.*?)\|")


def log(*a):
    print("[build_feed]", *a, flush=True)


def llm(prompt, max_tokens=2400, retries=2):
    """Single chat completion. Returns text content ('' on failure)."""
    if not KEY:
        log("AI_API_KEY empty -> skipping LLM call")
        return ""
    body = json.dumps({
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": 0,
        "reasoning_effort": "none",
    }).encode("utf-8")
    req = urllib.request.Request(API, data=body, method="POST", headers={
        "Authorization": "Bearer " + KEY,
        "Content-Type": "application/json; charset=utf-8",
    })
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                data = json.loads(r.read().decode("utf-8"))
            usage = data.get("usage", {})
            log(f"  llm ok: completion={usage.get('completion_tokens')} total={usage.get('total_tokens')}")
            return (data["choices"][0]["message"].get("content") or "").strip()
        except Exception as e:  # noqa: BLE001
            detail = ""
            if isinstance(e, urllib.error.HTTPError):
                try:
                    detail = e.read().decode("utf-8")[:200]
                except Exception:  # noqa: BLE001
                    pass
            log(f"  llm error (attempt {attempt + 1}): {e} {detail}")
    return ""


def extract_json(text):
    """Lenient JSON extraction: models sometimes wrap it in prose or fences."""
    if not text:
        return None
    text = re.sub(r"^```(?:json)?|```$", "", text.strip(), flags=re.M).strip()
    for opener, closer in (("[", "]"), ("{", "}")):
        i, j = text.find(opener), text.rfind(closer)
        if i != -1 and j > i:
            try:
                return json.loads(text[i:j + 1])
            except json.JSONDecodeError:
                continue
    return None


def load_papers(path):
    """Parse the arxiv engine's data.json into flat item dicts."""
    if not os.path.exists(path):
        log(f"missing {path}")
        return []
    try:
        with open(path, encoding="utf-8") as f:
            raw = json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        log(f"unreadable {path}: {e}")
        return []

    items, seen = [], {}
    for topic, papers in (raw or {}).items():
        for _pid, blob in (papers or {}).items():
            m = PAPER_RE.search(str(blob))
            if not m:
                continue
            date, title, author, _key, url, _code = (x.strip() for x in m.groups())
            date = date.replace("**", "").strip()
            title = title.replace("**", "").strip()
            author = author.replace("**", "").strip()
            if not title:
                continue
            dedupe = title.lower()
            if dedupe in seen:
                seen[dedupe]["topics"].append(topic)
                continue
            rec = {
                "id": "p:" + re.sub(r"\W+", "", url)[-24:],
                "kind": "paper",
                "date": date,
                "title": title,
                "authors": author,
                "url": url,
                "topic": topic,
                "topics": [topic],
            }
            seen[dedupe] = rec
            items.append(rec)
    items.sort(key=lambda x: x.get("date") or "", reverse=True)
    return items


NEWS_COLS = ("title", "name", "keyword", "platform", "source", "url", "link", "rank", "first_time", "last_time")


def load_news():
    """Industry-facing items from TrendRadar's RSS store.

    Two deliberate exclusions:
      * arXiv feeds - those papers already arrive, richer, via modules A/B.
      * the hot-search tables (news_items) - general-interest noise, not AI/OR signal.
    What remains is practitioner-facing material (e.g. Hacker News).
    """
    dbs = glob.glob(".news/output/**/*.db", recursive=True) + glob.glob(".news/output/**/*.sqlite*", recursive=True)
    if not dbs:
        log("no TrendRadar sqlite found under .news/output/")
        return []
    out = []
    for db in dbs:
        try:
            con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
            tables = [r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table'")]
            log(f"{os.path.basename(db)} tables: {tables}")
            if "rss_items" not in tables:
                con.close()
                continue
            feeds = {}
            if "rss_feeds" in tables:
                for fid, nm, furl in con.execute("SELECT id, name, COALESCE(feed_url,'') FROM rss_feeds"):
                    feeds[fid] = (str(nm or ""), str(furl or ""))
            log("  feeds=" + repr({v[0]: v[1] for v in feeds.values()}))
            rows = con.execute(
                "SELECT title, url, COALESCE(summary,''), COALESCE(published_at,''), feed_id "
                "FROM rss_items ORDER BY published_at DESC LIMIT ?",
                (NEWS_MAX * 20,)).fetchall()
            log("  rss_items rows=" + str(len(rows)))
            kept = 0
            for title, url, summary, published, fid in rows:
                title = (title or "").strip()
                if not title:
                    continue
                fname, furl = feeds.get(fid, ("", ""))
                if "arxiv" in (fname + " " + furl).lower():
                    continue
                kept += 1
                clean = re.sub(r"<[^>]+>", " ", summary or "")
                clean = re.sub(r"(Article|Comments) URL:\\s*\\S+", " ", clean)
                clean = re.sub(r"\\s+", " ", clean).strip()
                out.append({
                    "id": "n:" + str(abs(hash(title)) % (10 ** 10)),
                    "kind": "news",
                    "title": title,
                    "url": (url or "").strip(),
                    "source": fname.strip(),
                    "date": (published or "")[:10],
                    "summary": clean[:220],
                    "tags": [],
                    "extra": "",
                })
            log("  kept (non-arxiv): " + str(kept))
            con.close()
        except Exception as e:
            log(f"sqlite read failed for {db}: {e}")
    seen, uniq = set(), []
    for it in out:
        k = it["title"].lower()
        if k in seen:
            continue
        seen.add(k)
        uniq.append(it)
    log("industry items: " + str(len(uniq)) + " (with summary: " + str(sum(1 for x in uniq if x["summary"])) + ")")
    return uniq[:NEWS_MAX]



def score_items(module_label, items):
    """One LLM call: importance + Chinese one-line summary + tags for each item."""
    if not items:
        return {}
    lines = []
    for i, it in enumerate(items):
        lines.append(f"{i}. {it['title']}")
    prompt = (
        f"You are a research intelligence analyst. Below are the candidate titles collected today for the \"{module_label}\" track.\n"
        f"For each item give: importance (0-10, how important or novel it is for a researcher), "
        f"summary (one sentence, at most 30 words, in English), tags (1-3 short technical tags, preferably English).\n"
        f"Output only a JSON array, each element like {{\"i\": index, \"importance\": number, \"summary\": \"...\", \"tags\": [\"...\"]}}, with no commentary.\n\n"
        + "\n".join(lines)
    )
    parsed = extract_json(llm(prompt, max_tokens=3000))
    if not isinstance(parsed, list):
        log(f"  score parse failed for {module_label}")
        return {}
    out = {}
    for row in parsed:
        if not isinstance(row, dict):
            continue
        try:
            idx = int(row.get("i"))
        except (TypeError, ValueError):
            continue
        if 0 <= idx < len(items):
            out[items[idx]["id"]] = {
                "importance": max(0.0, min(10.0, float(row.get("importance") or 0))),
                "summary": str(row.get("summary") or "").strip()[:200],
                "tags": [str(t).strip()[:24] for t in (row.get("tags") or []) if str(t).strip()][:3],
            }
    log(f"  scored {len(out)}/{len(items)} for {module_label}")
    return out


def hot_topics(label, titles, n=5):
    """One LLM call: today's hot topics + a short summary."""
    if not titles:
        return []
    prompt = (
        f"Below are today's collected titles related to \"{label}\". Distil the {n} hottest themes.\n"
        f"For each theme give: title (at most 8 words, in English), summary (at most 40 words, in English, saying why it is hot), "
        f"keywords (1-3 source keywords).\n"
        f"Sort by heat, hottest first. Output only a JSON array of the form "
        f"[{{\"title\":\"...\",\"summary\":\"...\",\"keywords\":[\"...\"]}}], with no commentary.\n\n"
        + "\n".join(f"- {t}" for t in titles[:150])
    )
    parsed = extract_json(llm(prompt, max_tokens=1600))
    if not isinstance(parsed, list):
        log(f"  hot-topic parse failed for {label}")
        return []
    return [{
        "title": str(x.get("title") or "").strip()[:60],
        "summary": str(x.get("summary") or "").strip()[:240],
        "keywords": [str(k).strip()[:24] for k in (x.get("keywords") or []) if str(k).strip()][:3],
    } for x in parsed if isinstance(x, dict) and x.get("title")]


def main():
    log("AI key present:", bool(KEY))
    papers_by_module = {}
    for mid, label, path in MODULES:
        items = load_papers(path)
        log(f"{mid}: {len(items)} papers")
        papers_by_module[mid] = items[:TOP_N]

    news = load_news()
    news_scores = score_items("Industry / applied AI", news)
    for it in news:
        sc = news_scores.get(it["id"], {})
        it["importance"] = sc.get("importance", 0.0)
        it["tags"] = sc.get("tags", [])
        it["summary"] = (sc.get("summary") or it.get("summary") or "")[:220]
        it["module"] = "news"

    feed = {
        "generated_at": datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z",
        "model": MODEL,
        "modules": [],
        "hot": {"academic": [], "industry": []},
    }

    for mid, label, _path in MODULES:
        items = papers_by_module[mid]
        scores = score_items(label, items)
        for it in items:
            s = scores.get(it["id"], {})
            it["importance"] = s.get("importance", 0.0)
            it["summary"] = s.get("summary", "")
            it["tags"] = s.get("tags", [])
            it["module"] = mid
        items.sort(key=lambda x: (-x.get("importance", 0), x.get("date") or ""), reverse=False)
        feed["modules"].append({"id": mid, "label": label, "items": items})
        log(f"{mid}: {len(items)} items in feed")

    feed["news"] = news[:NEWS_MAX]

    acad_titles = [it["title"] for mid, _l, _p in MODULES for it in papers_by_module[mid]]
    feed["hot"]["academic"] = hot_topics("academic (LLMs for optimization + agents)", acad_titles)
    feed["hot"]["industry"] = hot_topics("industry (applied AI and large-model practice)", [n["title"] for n in news])

    os.makedirs("docs", exist_ok=True)
    with open("docs/feed.json", "w", encoding="utf-8") as f:
        json.dump(feed, f, ensure_ascii=False, indent=1)
    log(f"wrote docs/feed.json: modules={[ (m['id'], len(m['items'])) for m in feed['modules'] ]} "
        f"news={len(news)} hot={len(feed['hot']['academic'])}/{len(feed['hot']['industry'])}")


if __name__ == "__main__":
    sys.exit(main())
