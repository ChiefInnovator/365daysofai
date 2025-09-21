from __future__ import annotations

import csv
import html
import random
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / "365daysofai.csv"
OUTPUT_PATH = ROOT / "index.html"
IMAGES_DIR = ROOT / "images"


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", text.lower()).strip("-")
    return slug or "screenshot"


def load_projects() -> list[dict[str, str]]:
    projects: list[dict[str, str]] = []
    with CSV_PATH.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            title = (row.get("Title") or "").strip()
            description = (row.get("Description") or "").strip()
            repo_url = (row.get("Repo") or "").strip()
            page_url = (row.get("GitHub Page") or "").strip()
            screenshot_name = slugify(repo_url or title)
            screenshot_path = f"images/{screenshot_name}.png"
            projects.append(
                {
                    "title": title,
                    "description": description,
                    "repo": repo_url,
                    "page": page_url,
                    "screenshot": screenshot_path,
                }
            )
    return projects


def build_html(projects: list[dict[str, str]]) -> str:
    cards = []
    for project in projects:
        title = html.escape(project["title"])
        description = html.escape(project["description"])
        page_url = html.escape(project["page"])
        repo_url = html.escape(project["repo"])
        screenshot = html.escape(project["screenshot"])
        alt_text = f"Screenshot of {project['title'] or 'project'}"
        alt = html.escape(alt_text)
        card = f"""
            <article class=\"card\">
                <a class=\"card__image\" href=\"{page_url}\" target=\"_blank\" rel=\"noopener noreferrer\">
                    <img src=\"{screenshot}\" alt=\"{alt}\">
                </a>
                <div class=\"card__body\">
                    <h2><a href=\"{page_url}\" target=\"_blank\" rel=\"noopener noreferrer\">{title}</a></h2>
                    <p>{description}</p>
                    <a class=\"card__repo\" href=\"{repo_url}\" target=\"_blank\" rel=\"noopener noreferrer\">View source on GitHub</a>
                </div>
            </article>
        """
        cards.append(card)

    cards_html = "\n".join(cards)
    return f"""
<!DOCTYPE html>
<html lang=\"en\">
<head>
    <meta charset=\"UTF-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
    <title>365 Days of AI – Project Gallery</title>
    <style>
        :root {{
            color-scheme: light dark;
            font-family: 'Inter', 'Helvetica Neue', Helvetica, Arial, sans-serif;
            background-color: #f3f4f6;
            color: #111827;
        }}
        body {{
            margin: 0;
            padding: 2.5rem 1.5rem 3rem;
            background: linear-gradient(180deg, #f9fafb 0%, #e5e7eb 100%);
        }}
        header {{
            max-width: 960px;
            margin: 0 auto 2rem;
            text-align: center;
        }}
        header h1 {{
            margin-bottom: 0.5rem;
            font-size: clamp(2rem, 4vw, 2.75rem);
        }}
        header p {{
            margin: 0 auto;
            max-width: 720px;
            line-height: 1.6;
            font-size: 1.05rem;
            color: #374151;
        }}
        .grid {{
            max-width: 1200px;
            margin: 0 auto;
            display: grid;
            gap: 1.75rem;
            grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
        }}
        .card {{
            background: #ffffff;
            border-radius: 16px;
            box-shadow: 0 20px 45px -18px rgba(15, 23, 42, 0.35);
            overflow: hidden;
            display: flex;
            flex-direction: column;
            transition: transform 160ms ease, box-shadow 160ms ease;
        }}
        .card:hover {{
            transform: translateY(-6px);
            box-shadow: 0 24px 60px -20px rgba(15, 23, 42, 0.45);
        }}
        .card__image {{
            display: block;
            background: #0f172a;
        }}
        .card__image img {{
            display: block;
            width: 100%;
            height: 190px;
            object-fit: cover;
        }}
        .card__body {{
            padding: 1.25rem 1.5rem 1.5rem;
            display: flex;
            flex-direction: column;
            gap: 0.75rem;
        }}
        .card__body h2 {{
            margin: 0;
            font-size: 1.35rem;
        }}
        .card__body p {{
            margin: 0;
            flex: 1;
            line-height: 1.55;
            color: #4b5563;
        }}
        .card__body a {{
            color: #2563eb;
            text-decoration: none;
            font-weight: 600;
        }}
        .card__body a:hover,
        .card__body a:focus {{
            text-decoration: underline;
        }}
        .card__repo {{
            align-self: flex-start;
            font-size: 0.95rem;
        }}
        @media (prefers-color-scheme: dark) {{
            :root {{
                background-color: #0f172a;
                color: #f9fafb;
            }}
            body {{
                background: radial-gradient(circle at top, #1e293b, #0f172a 60%);
            }}
            header p {{
                color: #e2e8f0;
            }}
            .card {{
                background: rgba(15, 23, 42, 0.85);
                box-shadow: 0 24px 60px -30px rgba(15, 23, 42, 0.8);
            }}
            .card__body p {{
                color: #cbd5f5;
            }}
        }}
    </style>
</head>
<body>
    <header>
        <h1>365 Days of AI Projects</h1>
        <p>A growing collection of daily builds. Explore each app, see it in action, and dive into the source code to follow along with the journey.</p>
    </header>
    <section class=\"grid\">
        {cards_html}
    </section>
</body>
</html>
"""


def write_html(content: str) -> None:
    OUTPUT_PATH.write_text(content, encoding="utf-8")


def main() -> None:
    projects = load_projects()
    random.shuffle(projects)
    html_content = build_html(projects)
    write_html(html_content)


if __name__ == "__main__":
    main()
