#!/usr/bin/env python3
"""
Renders the projects section of index.html from live GitHub data.

Replaces everything between <!-- PROJECTS:START --> and <!-- PROJECTS:END -->
with one card per public owned repo, sorted by most-recently-pushed.
Each card shows language, stars/forks, pushed-ago, and (if available from
the public events feed) the latest commit message.

Invoked by .github/workflows/update-projects.yml on an hourly cron.
Uses GH_TOKEN (the default GITHUB_TOKEN) for a 1000 req/hr rate limit.
"""
import json
import os
import re
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone

USER = "Ssureshbantubilli"
INDEX = "index.html"
TOKEN = os.environ.get("GH_TOKEN", "")

GH_ICO = (
    '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 0C5.37 0 0 '
    '5.37 0 12c0 5.3 3.44 9.8 8.2 11.38.6.11.82-.26.82-.58v-2.02c-3.34.72-'
    '4.04-1.61-4.04-1.61-.54-1.37-1.32-1.74-1.32-1.74-1.08-.74.08-.72.08-.'
    '72 1.2.08 1.83 1.23 1.83 1.23 1.06 1.82 2.78 1.29 3.46.99.11-.77.42-1'
    '.3.76-1.6-2.66-.3-5.47-1.33-5.47-5.93 0-1.31.47-2.38 1.24-3.22-.12-.3'
    '-.54-1.52.12-3.18 0 0 1.01-.32 3.3 1.23a11.5 11.5 0 013.01-.4c1.02.01'
    ' 2.05.14 3.01.4 2.28-1.55 3.29-1.23 3.29-1.23.66 1.66.25 2.88.12 3.18'
    '.77.84 1.23 1.91 1.23 3.22 0 4.61-2.81 5.63-5.48 5.93.43.37.82 1.1.82'
    ' 2.22v3.29c0 .32.22.7.83.58C20.57 21.8 24 17.3 24 12c0-6.63-5.37-12-'
    '12-12z"/></svg>'
)


def api(path):
    req = urllib.request.Request(
        f"https://api.github.com{path}",
        headers={
            "Authorization": f"Bearer {TOKEN}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "skb-profile-updater",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())


def esc(s):
    return (
        (s or "")
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def tago(iso):
    if not iso:
        return ""
    dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
    d = (datetime.now(timezone.utc) - dt).total_seconds()
    if d < 60:
        return "just now"
    if d < 3600:
        return f"{int(d/60)}m ago"
    if d < 86400:
        return f"{int(d/3600)}h ago"
    if d < 2592000:
        return f"{int(d/86400)}d ago"
    return f"{int(d/2592000)}mo ago"


def lang_cls(l):
    l = (l or "").lower()
    if "python" in l:
        return "pl-py"
    if "dart" in l or "flutter" in l:
        return "pl-dt"
    return "pl-ai"


def main():
    if not TOKEN:
        print("ERROR: GH_TOKEN env var is required", file=sys.stderr)
        sys.exit(1)

    repos = api(f"/users/{USER}/repos?per_page=100&sort=pushed&type=owner")

    # GitHub's public events feed no longer includes commit details in
    # PushEvent payloads, so we call the commits endpoint once per repo
    # to get the latest message. With <30 repos this is well under any
    # rate limit (authenticated = 5000/hr).
    last_commit = {}
    for r in repos:
        if r.get("fork") or r.get("private"):
            continue
        name = r["name"]
        try:
            default_branch = r.get("default_branch") or "main"
            commits = api(
                f"/repos/{USER}/{name}/commits?per_page=1&sha={default_branch}"
            )
            if commits and isinstance(commits, list):
                msg = (commits[0].get("commit") or {}).get("message") or ""
                if msg:
                    last_commit[name] = msg
        except urllib.error.HTTPError as e:
            # 404/409 for empty repos is fine; skip commit line for this one
            print(f"warn: commits fetch failed for {name} ({e})")

    cards = []
    for r in repos:
        if r.get("fork") or r.get("private"):
            continue
        name = r["name"]
        desc = r.get("description") or "No description provided."
        lang = r.get("language") or "Repo"
        stars = r.get("stargazers_count", 0)
        forks = r.get("forks_count", 0)
        pushed = r.get("pushed_at") or ""
        topics = r.get("topics") or []
        url = r["html_url"]

        meta = (
            f'<div style="font-family:var(--mono);font-size:.56rem;color:var(--muted);'
            f'margin-top:.35rem;letter-spacing:.03em;">pushed {tago(pushed)} '
            f"&middot; &#9733;{stars} &middot; &#8889;{forks}</div>"
            if pushed
            else ""
        )

        cm_html = ""
        if name in last_commit and last_commit[name]:
            msg_line = last_commit[name].split("\n")[0][:90]
            cm_html = (
                f'<div style="font-family:var(--mono);font-size:.6rem;color:var(--cyan2);'
                f"margin-top:.5rem;padding-top:.45rem;border-top:1px dashed var(--border);"
                f'white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">'
                f"&#9656; {esc(msg_line)}</div>"
            )

        tag_source = topics if topics else ([lang] if lang else [])
        tags = "".join(f'<span class="ptag">{esc(t)}</span>' for t in tag_source[:4])

        card = (
            f'<a class="proj-card" href="{esc(url)}" target="_blank" rel="noopener">'
            f'<div class="proj-top"><div class="proj-ico">{GH_ICO}</div>'
            f'<span class="proj-lang {lang_cls(lang)}">{esc(lang)}</span></div>'
            f'<div class="proj-name">{esc(name)}</div>'
            f'<div class="proj-desc">{esc(desc)}</div>'
            f"{meta}{cm_html}"
            f'<div class="proj-tags">{tags}</div>'
            f"</a>"
        )
        cards.append(card)

    now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    body = "\n    " + "\n    ".join(cards) + f"\n    <!-- last_refresh: {now_utc} -->\n    "

    with open(INDEX, "r", encoding="utf-8") as f:
        html = f.read()

    pattern = re.compile(
        r"(<!-- PROJECTS:START -->)[\s\S]*?(<!-- PROJECTS:END -->)"
    )
    if not pattern.search(html):
        print("ERROR: PROJECTS:START/END markers not found in index.html", file=sys.stderr)
        sys.exit(1)

    new_html = pattern.sub(lambda m: m.group(1) + body + m.group(2), html)

    with open(INDEX, "w", encoding="utf-8") as f:
        f.write(new_html)

    print(f"rendered {len(cards)} cards at {now_utc}")


if __name__ == "__main__":
    main()
