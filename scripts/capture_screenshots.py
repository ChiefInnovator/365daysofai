from __future__ import annotations

import csv
import re
from pathlib import Path
from typing import Iterable

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / "365daysofai.csv"
IMAGES_DIR = ROOT / "images"


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", text.lower()).strip("-")
    return slug or "screenshot"


def read_rows(csv_path: Path) -> Iterable[dict[str, str]]:
    with csv_path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            yield row


def capture_all(rows: Iterable[dict[str, str]]) -> None:
    IMAGES_DIR.mkdir(exist_ok=True)
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 720})
        for row in rows:
            url = (row.get("GitHub Page") or "").strip()
            if not url:
                continue
            title = row.get("Title") or ""
            name_source = row.get("Repo") or title
            screenshot_name = slugify(name_source)
            destination = IMAGES_DIR / f"{screenshot_name}.png"
            print(f"Capturing {url} -> {destination.relative_to(ROOT)}")
            try:
                page.goto(url, wait_until="networkidle", timeout=30000)
                page.wait_for_timeout(1000)
                page.screenshot(path=str(destination), full_page=True)
            except Exception as exc:  # noqa: BLE001
                print(f"Failed to capture {url}: {exc}")
        browser.close()


def main() -> None:
    rows = list(read_rows(CSV_PATH))
    capture_all(rows)


if __name__ == "__main__":
    main()
