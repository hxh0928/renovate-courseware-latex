#!/usr/bin/env python3
"""Update release download history and render a small SVG line chart."""

from __future__ import annotations

import datetime as dt
import json
import os
import pathlib
import urllib.error
import urllib.request


ROOT = pathlib.Path(__file__).resolve().parents[1]
HISTORY_PATH = ROOT / "metrics" / "download-history.json"
SVG_PATH = ROOT / "assets" / "downloads-line.svg"
REPO = os.environ.get("GITHUB_REPOSITORY", "hxh0928/renovate-courseware-latex")
TOKEN = os.environ.get("GITHUB_TOKEN")


def fetch_release_downloads() -> int:
    req = urllib.request.Request(
        f"https://api.github.com/repos/{REPO}/releases",
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "renovate-courseware-latex-metrics",
        },
    )
    if TOKEN:
        req.add_header("Authorization", f"Bearer {TOKEN}")

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            releases = json.load(resp)
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return 0
        raise
    except urllib.error.URLError:
        return 0

    total = 0
    for release in releases:
        for asset in release.get("assets", []):
            total += int(asset.get("download_count", 0))
    return total


def load_history() -> list[dict[str, object]]:
    if not HISTORY_PATH.exists():
        return []
    with HISTORY_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_history(history: list[dict[str, object]]) -> None:
    HISTORY_PATH.parent.mkdir(parents=True, exist_ok=True)
    with HISTORY_PATH.open("w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)
        f.write("\n")


def update_history(history: list[dict[str, object]], total: int) -> list[dict[str, object]]:
    today = dt.date.today().isoformat()
    if history and history[-1].get("date") == today:
        history[-1]["release_downloads"] = total
    else:
        history.append({"date": today, "release_downloads": total})
    return history[-180:]


def render_svg(history: list[dict[str, object]]) -> str:
    width, height = 780, 260
    margin_left, margin_right = 54, 24
    margin_top, margin_bottom = 28, 46
    plot_w = width - margin_left - margin_right
    plot_h = height - margin_top - margin_bottom

    values = [int(row["release_downloads"]) for row in history] or [0]
    labels = [str(row["date"]) for row in history] or [dt.date.today().isoformat()]
    max_v = max(values + [1])
    min_v = min(values + [0])
    span = max(max_v - min_v, 1)

    def point(i: int, v: int) -> tuple[float, float]:
        x = margin_left + (plot_w * i / max(len(values) - 1, 1))
        y = margin_top + plot_h - ((v - min_v) / span * plot_h)
        return x, y

    points = [point(i, v) for i, v in enumerate(values)]
    polyline = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
    area = (
        f"{margin_left},{margin_top + plot_h} "
        + polyline
        + f" {margin_left + plot_w},{margin_top + plot_h}"
    )
    last_x, last_y = points[-1]
    first_label = labels[0]
    last_label = labels[-1]
    total = values[-1]

    grid = []
    for step in range(5):
        y = margin_top + plot_h * step / 4
        value = round(max_v - span * step / 4)
        grid.append(
            f'<line x1="{margin_left}" y1="{y:.1f}" x2="{margin_left + plot_w}" y2="{y:.1f}" class="grid"/>'
        )
        grid.append(
            f'<text x="{margin_left - 10}" y="{y + 4:.1f}" text-anchor="end" class="axis">{value}</text>'
        )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="Release downloads over time">
  <style>
    .bg {{ fill: #ffffff; }}
    .title {{ fill: #503025; font: 700 18px -apple-system,BlinkMacSystemFont,Segoe UI,sans-serif; }}
    .axis {{ fill: #5f5f5f; font: 12px -apple-system,BlinkMacSystemFont,Segoe UI,sans-serif; }}
    .grid {{ stroke: #e0e8ec; stroke-width: 1; }}
    .line {{ fill: none; stroke: #2a7e91; stroke-width: 3; stroke-linejoin: round; stroke-linecap: round; }}
    .area {{ fill: #e8f1f5; opacity: 0.9; }}
    .dot {{ fill: #d05c2a; stroke: #ffffff; stroke-width: 2; }}
  </style>
  <rect class="bg" width="{width}" height="{height}" rx="8"/>
  <text x="{margin_left}" y="22" class="title">Release Download Trend</text>
  {''.join(grid)}
  <line x1="{margin_left}" y1="{margin_top + plot_h}" x2="{margin_left + plot_w}" y2="{margin_top + plot_h}" class="grid"/>
  <polygon points="{area}" class="area"/>
  <polyline points="{polyline}" class="line"/>
  <circle cx="{last_x:.1f}" cy="{last_y:.1f}" r="5" class="dot"/>
  <text x="{margin_left}" y="{height - 16}" class="axis">{first_label}</text>
  <text x="{margin_left + plot_w}" y="{height - 16}" text-anchor="end" class="axis">{last_label}</text>
  <text x="{last_x - 8:.1f}" y="{last_y - 12:.1f}" text-anchor="end" class="axis">total {total}</text>
</svg>
"""


def main() -> None:
    total = fetch_release_downloads()
    history = update_history(load_history(), total)
    save_history(history)
    SVG_PATH.parent.mkdir(parents=True, exist_ok=True)
    SVG_PATH.write_text(render_svg(history), encoding="utf-8")


if __name__ == "__main__":
    main()
