#!/usr/bin/env python3
"""
Automated GitHub Profile README Updater for @imgolamrabbani
-----------------------------------------------------------
Automatically fetches:
1. Credited GitHub Security Advisories (GHSAs & CVEs) via `/advisories?credit=imgolamrabbani`
   + checks status/CVE assignment for pre-disclosure advisories (e.g. InvoicePlane GHSAs).
2. All upstream Pull Requests (`author:imgolamrabbani type:pr -user:imgolamrabbani`),
   automatically grouping 2+ PRs to the same repo into collapsible `<details>` dropdowns
   (akasakariko style) with live star & PR state badges.
3. All upstream Issues / Bug Reports (`author:imgolamrabbani type:issue -user:imgolamrabbani`)
   with live star badges.

Usage in GitHub Actions (`.github/workflows/update-readme.yml`):
----------------------------------------------------------------
Create `.github/workflows/update-readme.yml` in your `imgolamrabbani/imgolamrabbani` repo:

```yaml
name: Auto-Update Profile README

on:
  schedule:
    - cron: '0 */6 * * *' # Runs automatically every 6 hours
  workflow_dispatch:      # Allows manual 1-click run from Actions tab
  push:
    branches: [ main ]
    paths:
      - 'update_readme.py'
      - '.github/workflows/update-readme.yml'

permissions:
  contents: write

jobs:
  update-readme:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Run README Auto-Updater
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          GH_USERNAME: imgolamrabbani
        run: python3 update_readme.py

      - name: Commit and push if changed
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
          git add README.md
          git diff --staged --quiet || git commit -m "chore(readme): auto-update PRs, issues, and advisories [skip ci]"
          git push
```
"""

import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request
from collections import OrderedDict
from datetime import datetime, timezone

USERNAME = os.environ.get("GH_USERNAME", "imgolamrabbani")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
README_PATH = os.environ.get("README_PATH", "README.md")

# Pre-disclosure / draft advisories credited in upstream changelogs while awaiting public GHSA/CVE release.
# Once the upstream maintainer publishes the GHSA, the script automatically fetches its live CVE ID & severity.
SEED_ADVISORIES = [
    {
        "ghsa_id": "GHSA-2849-wpq6-pq9g",
        "repo": "InvoicePlane/InvoicePlane",
        "url": "https://github.com/InvoicePlane/InvoicePlane/security/advisories/GHSA-2849-wpq6-pq9g#event-1234159",
        "changelog_url": "https://github.com/InvoicePlane/InvoicePlane/blob/develop/.github/CHANGELOG.md",
        "cwe": "CWE-284 / CWE-200",
        "title": "Unauthenticated direct route access to `Payment_information::stripe()` and `paypal()` disclosed gateway public key / client ID and settings even with online payments disabled",
        "fix_prs": [
            ("#1837", "https://github.com/InvoicePlane/InvoicePlane/pull/1837"),
            ("#1838", "https://github.com/InvoicePlane/InvoicePlane/pull/1838"),
        ],
    },
    {
        "ghsa_id": "GHSA-ppgp-rvmx-2wp5",
        "repo": "InvoicePlane/InvoicePlane",
        "url": "https://github.com/InvoicePlane/InvoicePlane/security/advisories/GHSA-ppgp-rvmx-2wp5#event-1234161",
        "changelog_url": "https://github.com/InvoicePlane/InvoicePlane/blob/develop/.github/CHANGELOG.md",
        "cwe": "CWE-639 / CWE-862",
        "title": "Client assignments of any user readable by a secondary administrator via `users/ajax/load_user_client_table`, `users/ajax/modal_add_user_client`, and `user_clients/user/<id>`",
        "fix_prs": [
            ("#1836", "https://github.com/InvoicePlane/InvoicePlane/pull/1836"),
        ],
    },
]


def gh_api_get(url: str):
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": f"{USERNAME}-readme-updater",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode("utf-8"))


def fetch_advisories() -> str:
    """Fetches published GHSAs/CVEs credited to USERNAME and merges with pre-disclosure advisories."""
    published_by_id = {}
    try:
        url = f"https://api.github.com/advisories?credit={urllib.parse.quote(USERNAME)}&per_page=100"
        data = gh_api_get(url)
        if isinstance(data, list):
            for adv in data:
                ghsa_id = adv.get("ghsa_id")
                if ghsa_id:
                    published_by_id[ghsa_id] = adv
    except Exception as exc:
        print(f"[warn] Could not query global advisories API: {exc}")

    lines = []
    seen_ids = set()

    # 1. Process seeded advisories (automatically upgrading if now public)
    for seed in SEED_ADVISORIES:
        ghsa_id = seed["ghsa_id"]
        seen_ids.add(ghsa_id)
        repo = seed["repo"]
        adv = published_by_id.get(ghsa_id)

        # Also check repo-specific advisory endpoint in case it was published recently
        if not adv:
            try:
                adv = gh_api_get(f"https://api.github.com/repos/{repo}/security-advisories/{ghsa_id}")
            except Exception:
                adv = None

        star_badge = f"![stars](https://img.shields.io/github/stars/{repo}?style=flat-square&label=stars&color=DAA520)"
        if adv and adv.get("state") == "published":
            cve_id = adv.get("cve_id") or "CVE Pending"
            severity = (adv.get("severity") or "medium").upper()
            summary = adv.get("summary") or seed["title"]
            html_url = adv.get("html_url") or seed["url"]
            cve_badge = f"![CVE](https://img.shields.io/badge/{cve_id.replace('-', '--')}-{severity}-critical?style=flat-square)"
            lines.append(
                f"- **[{repo} · {ghsa_id}]({html_url})** {star_badge} {cve_badge} `{seed['cwe']}` — {summary}"
            )
        else:
            status_badge = "![Status](https://img.shields.io/badge/status-Patched_%2F_Pre--Release_GHSA-orange?style=flat-square)"
            fixes = ", ".join(f"[{num}]({u})" for num, u in seed.get("fix_prs", []))
            fix_suffix = f" *(Patched in {fixes} · [Changelog Credit]({seed['changelog_url']}))*" if fixes else ""
            lines.append(
                f"- **[{repo} · {ghsa_id}]({seed['url']})** {star_badge} {status_badge} `{seed['cwe']}` — {seed['title']}{fix_suffix}"
            )

    # 2. Append any newly published advisories discovered dynamically from GitHub API
    for ghsa_id, adv in published_by_id.items():
        if ghsa_id in seen_ids:
            continue
        cve_id = adv.get("cve_id") or ghsa_id
        severity = (adv.get("severity") or "info").upper()
        summary = adv.get("summary") or "Security advisory"
        html_url = adv.get("html_url") or f"https://github.com/advisories/{ghsa_id}"
        repo_url = adv.get("repository_advisory_url") or ""
        repo_match = re.search(r"repos/([^/]+/[^/]+)/", repo_url)
        repo_name = repo_match.group(1) if repo_match else "GitHub Advisory"
        star_badge = (
            f"![stars](https://img.shields.io/github/stars/{repo_name}?style=flat-square&label=stars&color=DAA520) "
            if "/" in repo_name
            else ""
        )
        cve_badge = f"![CVE](https://img.shields.io/badge/{cve_id.replace('-', '--')}-{severity}-critical?style=flat-square)"
        lines.append(f"- **[{repo_name} · {ghsa_id}]({html_url})** {star_badge}{cve_badge} — {summary}")

    return "\n".join(lines)


def fetch_prs() -> str:
    """Fetches all external PRs by USERNAME and formats them in akasakariko style."""
    q = urllib.parse.quote(f"author:{USERNAME} type:pr -user:{USERNAME}")
    url = f"https://api.github.com/search/issues?q={q}&sort=created&order=desc&per_page=100"
    data = gh_api_get(url)
    items = data.get("items", [])

    by_repo = OrderedDict()
    for item in items:
        repo_url = item.get("repository_url", "")
        repo = "/".join(repo_url.rstrip("/").split("/")[-2:])
        if not repo:
            continue
        by_repo.setdefault(repo, []).append(item)

    single_lines = []
    multi_blocks = []

    for repo, prs in by_repo.items():
        star_badge = f"![stars](https://img.shields.io/github/stars/{repo}?style=flat-square&label=stars&color=DAA520)"
        if len(prs) == 1:
            pr = prs[0]
            num = pr["number"]
            title = pr["title"]
            html_url = pr["html_url"]
            pr_badge = f"![pr](https://img.shields.io/github/pulls/detail/state/{repo}/{num}?style=flat-square&label=PR)"
            single_lines.append(f"- **[{repo}#{num}]({html_url})** {star_badge} {pr_badge} — {title}")
        else:
            block = [
                f"<details open>",
                f"<summary><strong>{repo}</strong> – {len(prs)} PRs <img alt=\"stars\" src=\"https://img.shields.io/github/stars/{repo}?style=flat-square&label=stars&color=DAA520\"></summary>",
                "",
            ]
            for pr in prs:
                num = pr["number"]
                title = pr["title"]
                html_url = pr["html_url"]
                pr_badge = f"![pr](https://img.shields.io/github/pulls/detail/state/{repo}/{num}?style=flat-square&label=PR)"
                block.append(f"- **[{repo}#{num}]({html_url})** {pr_badge} — {title}")
            block.append("")
            block.append("</details>")
            multi_blocks.append("\n".join(block))

    sections = []
    if single_lines:
        sections.append("\n".join(single_lines))
    if multi_blocks:
        sections.append("\n\n".join(multi_blocks))
    return "\n\n".join(sections)


def fetch_issues() -> str:
    """Fetches all external Issues / Bug Reports opened by USERNAME."""
    q = urllib.parse.quote(f"author:{USERNAME} type:issue -user:{USERNAME}")
    url = f"https://api.github.com/search/issues?q={q}&sort=created&order=desc&per_page=100"
    data = gh_api_get(url)
    items = data.get("items", [])

    lines = []
    for issue in items:
        repo_url = issue.get("repository_url", "")
        repo = "/".join(repo_url.rstrip("/").split("/")[-2:])
        num = issue["number"]
        title = issue["title"]
        html_url = issue["html_url"]
        star_badge = f"![stars](https://img.shields.io/github/stars/{repo}?style=flat-square&label=stars&color=DAA520)"
        state_badge = f"![issue](https://img.shields.io/github/issues/detail/state/{repo}/{num}?style=flat-square&label=issue)"
        lines.append(f"- **[{repo}#{num}]({html_url})** {star_badge} {state_badge} — {title}")

    return "\n".join(lines)


def replace_section(content: str, marker: str, new_body: str) -> str:
    pattern = re.compile(
        rf"(<!-- {marker}:START -->).*?(<!-- {marker}:END -->)",
        re.DOTALL,
    )
    replacement = f"\\1\n{new_body}\n\\2"
    return pattern.sub(replacement, content)


def main():
    with open(README_PATH, "r", encoding="utf-8") as f:
        readme = f.read()

    try:
        advisories_md = fetch_advisories()
        if advisories_md:
            readme = replace_section(readme, "AUTO-ADVISORIES", advisories_md)
    except Exception as exc:
        print(f"[warn] Skipping AUTO-ADVISORIES update: {exc}")

    try:
        prs_md = fetch_prs()
        if prs_md:
            readme = replace_section(readme, "AUTO-PRS", prs_md)
    except Exception as exc:
        print(f"[warn] Skipping AUTO-PRS update: {exc}")

    try:
        issues_md = fetch_issues()
        if issues_md:
            readme = replace_section(readme, "AUTO-ISSUES", issues_md)
    except Exception as exc:
        print(f"[warn] Skipping AUTO-ISSUES update: {exc}")

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(readme)
    print(f"Successfully updated {README_PATH} at {datetime.now(timezone.utc).isoformat()}")


if __name__ == "__main__":
    main()