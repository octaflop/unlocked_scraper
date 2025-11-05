# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python meetup talk/workshop repository focused on **web scraping with and without async and with and without the GIL**. The repository serves as both a presentation and live demo showcase for novice coders learning about:

- Synchronous vs asynchronous web scraping
- The Global Interpreter Lock (GIL) and its impact on performance
- Free-threaded Python 3.14 (GIL-free mode)
- How web scraping benefits from concurrent programming (callback nature of following links)

**Repository name:** `unlocked_scraper` (referring to "unlocking" Python's GIL)

## Critical Requirements

**MUST use Python 3.14 with free-threading support** - this is a core requirement for demonstrating GIL-free performance.

### Environment Setup

```bash
# Install dependencies (requires Python 3.14)
uv sync

# Activate virtual environment if needed
source .venv/bin/activate  # or use uv run
```

### Required Dependencies

The demo requires:
- `aiohttp` - Asynchronous HTTP requests
- `beautifulsoup4` (bs4) - HTML parsing
- `qrcode` - QR code generation for talk materials
- Python 3.14+ with free-threading support

## Running the Web Scraping Demos

The main demo script scrapes Hacker News stories and comments to demonstrate performance differences across three configurations:

### Single-threaded (baseline)
```bash
python scraper.py
```

### Multi-threaded with GIL (default Python build)
```bash
python scraper.py --multithreaded
```

### Multi-threaded GIL-free (free-threaded Python 3.14)
```bash
python -X gil=0 scraper.py --multithreaded
```

### Expected Performance Results (on 12-core CPU)

| Configuration                      | Stories/sec | Speedup |
| ---------------------------------- | ----------- | ------- |
| default build, single thread       | ~12         | 1x      |
| default build, multithreaded       | ~35         | ~3x     |
| free-threaded build, multithreaded | ~80         | ~7x     |

**Key Learning Points for Novices:**
- Default Python gets *some* parallelism during I/O (GIL released during network waits)
- Free-threaded Python achieves true multi-core parallelism
- Web scraping is I/O-bound, making it ideal for async and concurrent approaches
- Following links has a natural callback structure that maps well to async patterns

## Repository Structure

- `talk/` - Presentation slides and materials (Marp-based)
- `demos/` - Live code demonstrations for the talk
  - Old demos (FastAPI/Jinja) can serve as templates but will be replaced with scraping demos
- `tools/` - Utilities like QR code generation for sharing talk materials
- `main.py` - Entry point (currently minimal, can be developed into main demo launcher)

## Presentation Materials

### Talk Directory (`talk/`)
Contains Marp-based presentation slides explaining:
- What web scraping is and why it's challenging
- Synchronous approach limitations
- Asyncio and concurrent scraping
- The callback nature of following links (novice-friendly explanation)
- GIL impact and free-threaded Python benefits

To preview slides in an IDE that supports Marp, right-click the .md file and select "Open with > Marp Preview".

### Tools
`tools/qrslide.py` - Generates SVG QR codes for sharing talk materials (repo link, resources, etc.)

## Web Scraping Demo Architecture

### Core Concepts for Novices

**Why web scraping is a good async example:**
- Each page fetch is independent (can be done in parallel)
- Pages contain links to other pages (natural callback/recursive structure)
- I/O-bound workload (waiting for network, not CPU)
- Easy to understand: "fetch page → parse links → fetch those pages"

### Demo Script Structure (scraper.py pattern)

```python
# Key functions:
async def fetch(session, url) -> str
    # Fetches a single page

def parse_stories(html) -> list[dict]
    # Extracts story data from HTML

def parse_comments(html) -> list[dict]
    # Extracts comments from story pages

async def fetch_story_with_comments(session, story) -> dict
    # Fetches story details including all comments

async def worker(queue, all_stories) -> None
    # Worker coroutine that processes pages from queue
    # Uses TaskGroup for concurrent comment fetching

def main(multithreaded: bool) -> None
    # Orchestrates workers across threads (if multithreaded)
    # Uses ThreadPoolExecutor + asyncio.run() for each thread
```

**Threading Strategy:**
- Each thread runs its own asyncio event loop via `asyncio.run(worker(...))`
- Threads share a thread-safe `Queue` for work distribution
- With GIL: limited parallelism (only during I/O waits)
- Without GIL (`-X gil=0`): true multi-core parallelism

## Development Guidelines

### For Talk Content
- Keep explanations accessible to novice coders
- Use concrete examples (e.g., "imagine scraping 100 pages...")
- Emphasize the callback nature: "each page has links to more pages"
- Show real performance numbers from live demos

### For Demo Code
- Use clear variable names and comments
- Structure code to match talk narrative
- Include timing/performance metrics in output
- Make it easy to run different configurations for comparison

## Legacy Content

The repository previously contained FastAPI/Jinja2/HTMX demos. These serve as templates for potential interactive demos but are not the primary focus. The current focus is web scraping performance demonstrations.
