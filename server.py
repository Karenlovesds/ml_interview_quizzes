#!/usr/bin/env python3
"""Tiny dependency-free server for the ML Interview Quiz POC.

Serves:
  - the web SPA from ./web
  - the quiz bank     ./data/questions.json
  - the knowledge base ./corpus/*.md
  - a persisted attempt history ./data/history.json (wrong-answer tracking)
"""

from __future__ import annotations

import json
import mimetypes
import os
import re
import threading
import time
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse, parse_qs

ROOT = Path(__file__).resolve().parent
CORPUS_DIR = ROOT / "corpus"
WEB_DIR = ROOT / "web"
QUESTIONS_FILE = ROOT / "data" / "questions.json"
HISTORY_FILE = ROOT / "data" / "history.json"

_LOCK = threading.Lock()

MIME_OVERRIDES = {
    ".js": "text/javascript",
    ".mjs": "text/javascript",
    ".css": "text/css",
    ".json": "application/json",
    ".svg": "image/svg+xml",
    ".html": "text/html",
}


def load_json(path: Path, default):
    if not path.exists():
        return default
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def load_questions():
    return load_json(QUESTIONS_FILE, {"version": 1, "topics": [], "questions": []})


def load_history():
    return load_json(HISTORY_FILE, {"attempts": []})


def save_history(history):
    HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    tmp = HISTORY_FILE.with_suffix(".json.tmp")
    with tmp.open("w", encoding="utf-8") as fh:
        json.dump(history, fh, indent=2)
    os.replace(tmp, HISTORY_FILE)


def sanitize(q):
    """Strip answer/explanation before sending to the client."""
    return {
        "id": q["id"],
        "topic": q["topic"],
        "difficulty": q.get("difficulty", "medium"),
        "question": q["question"],
        "options": q["options"],
    }


def weakness_report():
    bank = load_questions()
    history = load_history()
    topics = {t["slug"]: t for t in bank["topics"]}
    q_by_id = {q["id"]: q for q in bank["questions"]}

    per_topic = {
        slug: {"slug": slug, "name": t.get("name", slug), "attempts": 0,
               "correct": 0, "wrong": 0}
        for slug, t in topics.items()
    }
    per_question = {}
    recent_wrong = []

    for a in history["attempts"]:
        slug = a.get("topic", "unknown")
        bucket = per_topic.setdefault(
            slug, {"slug": slug, "name": slug, "attempts": 0, "correct": 0, "wrong": 0}
        )
        bucket["attempts"] += 1
        if a.get("correct"):
            bucket["correct"] += 1
        else:
            bucket["wrong"] += 1
            q = q_by_id.get(a.get("question_id"))
            if q:
                pq = per_question.setdefault(
                    q["id"],
                    {
                        "id": q["id"],
                        "topic": q["topic"],
                        "topic_name": topics.get(q["topic"], {}).get("name", q["topic"]),
                        "question": q["question"],
                        "options": q["options"],
                        "answer": q["answer"],
                        "explanation": q["explanation"],
                        "wrong_count": 0,
                        "last_wrong": None,
                    },
                )
                pq["wrong_count"] += 1
                pq["last_wrong"] = a.get("ts")

    for bucket in per_topic.values():
        bucket["accuracy"] = (
            round(bucket["correct"] / bucket["attempts"], 3) if bucket["attempts"] else None
        )

    ranked = [b for b in per_topic.values() if b["attempts"] > 0]
    ranked.sort(key=lambda b: (b["accuracy"], -b["attempts"]))

    wrong_questions = sorted(
        per_question.values(), key=lambda q: (-q["wrong_count"], q["topic"])
    )

    total_attempts = sum(b["attempts"] for b in per_topic.values())
    total_correct = sum(b["correct"] for b in per_topic.values())

    return {
        "total_attempts": total_attempts,
        "total_correct": total_correct,
        "overall_accuracy": round(total_correct / total_attempts, 3) if total_attempts else None,
        "topics": ranked,
        "weak_topics": [b for b in ranked if b["accuracy"] is not None and b["accuracy"] < 0.8],
        "wrong_questions": wrong_questions,
    }


# ---------------------------------------------------------------- markdown

_MD_LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


def render_markdown(md: str) -> str:
    """Minimal, safe-enough Markdown -> HTML for the bundled corpus."""
    lines = md.splitlines()
    html = []
    in_ul = in_ol = in_code = False
    in_table = False
    table_rows = []

    def close_lists():
        nonlocal in_ul, in_ol
        if in_ul:
            html.append("</ul>")
            in_ul = False
        if in_ol:
            html.append("</ol>")
            in_ol = False

    def flush_table():
        nonlocal in_table, table_rows
        if not table_rows:
            in_table = False
            return
        html.append('<table class="md-table">')
        for i, row in enumerate(table_rows):
            tag = "th" if i == 0 else "td"
            html.append("<tr>" + "".join(f"<{tag}>{c}</{tag}>" for c in row) + "</tr>")
        html.append("</table>")
        table_rows = []
        in_table = False

    def inline(text):
        text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
        text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
        text = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", text)
        text = _MD_LINK.sub(r'<a href="\2">\1</a>', text)
        return text

    for raw in lines:
        line = raw.rstrip()
        if line.strip().startswith("```"):
            if in_code:
                html.append("</code></pre>")
                in_code = False
            else:
                close_lists()
                html.append("<pre><code>")
                in_code = True
            continue
        if in_code:
            html.append(line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))
            continue
        if not line.strip():
            close_lists()
            flush_table()
            continue
        if line.lstrip().startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if all(set(c) <= set("-: ") and c for c in cells):
                continue
            in_table = True
            table_rows.append(cells)
            continue
        if in_table:
            flush_table()
        if line.startswith("######"):
            close_lists(); html.append(f"<h6>{inline(line[6:].strip())}</h6>")
        elif line.startswith("#####"):
            close_lists(); html.append(f"<h5>{inline(line[5:].strip())}</h5>")
        elif line.startswith("####"):
            close_lists(); html.append(f"<h4>{inline(line[4:].strip())}</h4>")
        elif line.startswith("###"):
            close_lists(); html.append(f"<h3>{inline(line[3:].strip())}</h3>")
        elif line.startswith("##"):
            close_lists(); html.append(f"<h2>{inline(line[2:].strip())}</h2>")
        elif line.startswith("#"):
            close_lists(); html.append(f"<h1>{inline(line[1:].strip())}</h1>")
        elif re.match(r"^\s*[-*]\s+", line):
            if not in_ul:
                close_lists(); html.append("<ul>"); in_ul = True
            item = re.sub(r"^\s*[-*]\s+", "", line)
            html.append("<li>" + inline(item) + "</li>")
        elif re.match(r"^\s*\d+\.\s+", line):
            if not in_ol:
                close_lists(); html.append("<ol>"); in_ol = True
            item = re.sub(r"^\s*\d+\.\s+", "", line)
            html.append("<li>" + inline(item) + "</li>")
        else:
            close_lists(); html.append(f"<p>{inline(line)}</p>")
    if in_code:
        html.append("</code></pre>")
    close_lists()
    flush_table()
    return "\n".join(html)


def corpus_index():
    items = []
    for path in sorted(CORPUS_DIR.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        title = path.stem
        for line in text.splitlines():
            if line.startswith("#"):
                title = line.lstrip("#").strip()
                break
        items.append({"slug": path.stem, "title": title,
                      "words": len(text.split())})
    return items


# ---------------------------------------------------------------- handler


class Handler(BaseHTTPRequestHandler):
    server_version = "MLQuizPOC/1.0"

    def log_message(self, fmt, *args):
        print(f"[{self.log_date_time_string()}] {self.address_string()} {fmt % args}")

    # --- helpers
    def send_json(self, obj, status=200):
        body = json.dumps(obj).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def send_text(self, text, content_type="text/plain; charset=utf-8", status=200):
        body = text.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def read_body(self):
        length = int(self.headers.get("Content-Length", 0))
        if not length:
            return {}
        try:
            return json.loads(self.rfile.read(length) or "{}")
        except json.JSONDecodeError:
            return {}

    # --- routing
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        if path == "/api/topics":
            bank = load_questions()
            return self.send_json(bank["topics"])

        if path == "/api/quiz":
            bank = load_questions()
            history = load_history()
            topic = query.get("topic", [None])[0]
            mode = query.get("mode", ["all"])[0]
            questions = list(bank["questions"])
            if topic and topic != "all":
                questions = [q for q in questions if q["topic"] == topic]
            if mode == "wrong":
                wrong_ids = {a["question_id"] for a in history["attempts"]
                             if not a.get("correct")}
                questions = [q for q in questions if q["id"] in wrong_ids]
            elif mode == "unseen":
                seen = {a["question_id"] for a in history["attempts"]}
                questions = [q for q in questions if q["id"] not in seen]
            return self.send_json({"count": len(questions),
                                   "questions": [sanitize(q) for q in questions]})

        if path == "/api/weakness":
            return self.send_json(weakness_report())

        if path == "/api/history":
            return self.send_json(load_history())

        if path == "/api/corpus":
            return self.send_json(corpus_index())

        if path.startswith("/api/corpus/"):
            slug = path[len("/api/corpus/"):]
            if not re.fullmatch(r"[A-Za-z0-9_-]+", slug):
                return self.send_json({"error": "bad slug"}, 400)
            fpath = CORPUS_DIR / f"{slug}.md"
            if not fpath.exists():
                return self.send_json({"error": "not found"}, 404)
            md = fpath.read_text(encoding="utf-8")
            return self.send_json({"slug": slug, "markdown": md,
                                   "html": render_markdown(md)})

        return self.serve_static(path)

    def do_POST(self):
        path = urlparse(self.path).path

        if path == "/api/submit":
            payload = self.read_body()
            qid = payload.get("question_id")
            choice = payload.get("choice")
            bank = load_questions()
            q = next((x for x in bank["questions"] if x["id"] == qid), None)
            if q is None:
                return self.send_json({"error": "unknown question"}, 404)
            if not isinstance(choice, int) or not (0 <= choice < len(q["options"])):
                return self.send_json({"error": "invalid choice"}, 400)
            correct = choice == q["answer"]
            attempt = {
                "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "question_id": q["id"],
                "topic": q["topic"],
                "choice": choice,
                "answer": q["answer"],
                "correct": correct,
            }
            with _LOCK:
                history = load_history()
                history["attempts"].append(attempt)
                save_history(history)
            return self.send_json({
                "correct": correct,
                "answer": q["answer"],
                "answer_text": q["options"][q["answer"]],
                "explanation": q["explanation"],
                "topic": q["topic"],
            })

        if path == "/api/reset":
            with _LOCK:
                save_history({"attempts": []})
            return self.send_json({"ok": True})

        return self.send_json({"error": "not found"}, 404)

    # --- static
    def serve_static(self, path):
        rel = "index.html" if path in ("/", "") else path.lstrip("/")
        target = (WEB_DIR / rel).resolve()
        if not str(target).startswith(str(WEB_DIR.resolve())) or not target.is_file():
            return self.send_text("Not found", status=404)
        ctype = MIME_OVERRIDES.get(target.suffix)
        if not ctype:
            ctype = mimetypes.guess_type(str(target))[0] or "application/octet-stream"
        if ctype.startswith("text/") or ctype in ("application/json",):
            ctype += "; charset=utf-8"
        data = target.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


def main():
    import argparse

    parser = argparse.ArgumentParser(description="ML Interview Quiz POC server")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--host", default="127.0.0.1")
    args = parser.parse_args()

    httpd = ThreadingHTTPServer((args.host, args.port), Handler)
    url = f"http://{args.host}:{args.port}"
    print(f"ML Interview Quiz POC running at {url}")
    print("Press Ctrl+C to stop.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down.")
        httpd.shutdown()


if __name__ == "__main__":
    main()
