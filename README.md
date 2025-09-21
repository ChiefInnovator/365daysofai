# 365 Days of AI Gallery

This repository tracks the "365 Days of AI" builds and generates a visual gallery highlighting each project. Screenshots are harvested from the live GitHub Pages deployments listed in `365daysofai.csv`, then rendered in a responsive grid (`index.html`).

## Prerequisites

- Python 3.10+
- [Playwright](https://playwright.dev/python/)

Install Playwright and its Chromium browser once:

```bash
python3 -m pip install playwright
python3 -m playwright install chromium
```

## CSV Source

Projects are defined in `365daysofai.csv` with the following columns:

| Column        | Description                             |
| ------------- | --------------------------------------- |
| `#`           | Entry number (for tracking only)        |
| `Title`       | Project name                            |
| `Description` | Short summary displayed on the card     |
| `Repo`        | GitHub repository URL                   |
| `GitHub Page` | Live deployment URL (used for captures) |

Update the CSV to add or modify projects. Ensure each row includes a valid GitHub Pages URL before taking screenshots.

## Generate Screenshots

Use the helper script to visit every GitHub Pages link and store an image under `images/`:

```bash
python3 scripts/capture_screenshots.py
```

Screenshots are saved as PNGs whose filenames are derived from the repository URL (e.g., `images/https-github-com-user-project.png`). Re-run the script whenever the CSV gains new entries or a deployment changes.

## Build the Gallery

Create or refresh the gallery after capturing screenshots:

```bash
python3 scripts/build_gallery.py
```

The script:

- Reads `365daysofai.csv`
- Randomizes project order
- Embeds the stored screenshots
- Writes a responsive grid to `index.html`

Open `index.html` in a browser to verify the layout.

## Repository Layout

- `365daysofai.csv` — single source of truth for project metadata
- `images/` — Playwright-generated screenshots (ignored by Git by default)
- `scripts/capture_screenshots.py` — automates screenshot capture
- `scripts/build_gallery.py` — renders the HTML gallery
- `index.html` — generated gallery page

Feel free to customize the styling in `scripts/build_gallery.py` or extend the scripts to support additional metadata as the challenge evolves.
