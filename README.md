# Unlocked! 🔓 Web Scraping with GIL-Free Python 3.14

A Python meetup talk demonstrating the performance benefits of free-threaded Python 3.14 for web scraping workloads.

## What This Talk Covers

This repository contains a presentation and live demo showing:

- **Synchronous vs Asynchronous web scraping** - Why async matters for I/O-bound work
- **The Global Interpreter Lock (GIL)** - Python's traditional performance limitation
- **Free-threaded Python 3.14** - The new GIL-free mode (`python -X gil=0`)
- **Real-world performance comparison** - See 7x speedup in action!

Perfect for novice coders wanting to understand async programming and Python's new capabilities.

## Quick Start

### Requirements

- **Python 3.14** (or 3.13 with experimental free-threading support)
- **uv** package manager ([installation guide](https://github.com/astral-sh/uv))
- **Node.js & npm** (for building presentation slides)

### Installation

```bash
# Clone the repository
git clone https://github.com/octaflop/unlocked_scraper.git
cd unlocked_scraper

# Install Python dependencies with uv (automatically manages Python 3.14)
uv sync

# Install npm dependencies for presentation building
npm install
```

> **💡 Tip**: See [PYTHON_SETUP.md](PYTHON_SETUP.md) for detailed instructions on working with GIL vs GIL-free Python, switching versions, and troubleshooting.

## Running the Demo

The demo scrapes Hacker News stories and comments to show performance differences:

### 1. Single-threaded (baseline)
```bash
uv run python scraper.py
```
Expected: ~12 stories/sec on a 12-core CPU

### 2. Multi-threaded with GIL
```bash
uv run python scraper.py --multithreaded
```
Expected: ~35 stories/sec (3x improvement)

### 3. Multi-threaded GIL-free 🚀
```bash
uv run python -X gil=0 scraper.py --multithreaded
```
Expected: ~80 stories/sec (7x improvement!)

## Interactive Learning & Demos 🎨

### Terminal Demo with Rich UI

Beautiful, interactive demonstration with live progress bars:

```bash
# Run with GIL
uv run python demos/terminal_demo.py

# Run without GIL (free-threading)
uv run python -X gil=0 demos/terminal_demo.py
```

Features: 🎨 Rich TUI | 📊 Progress bars | 📈 Performance graphs | 💡 Explanations

### Local Test Server

Start a FastAPI server to test your scrapers against:

```bash
# Start the server
uv run uvicorn demos.test_server:app --reload

# Access at http://127.0.0.1:8000
```

The test server provides:
- 100 articles across 10 pages
- Pagination links for crawler testing
- Related articles for deep crawling
- Real-time statistics at `/stats`
- JSON API endpoints at `/api/stats` and `/api/articles`

Perfect for developing and testing scrapers locally!

## Understanding the Results

| Configuration                      | Stories/sec | Speedup | Why?                                    |
| ---------------------------------- | ----------- | ------- | --------------------------------------- |
| Single thread                      | ~12         | 1x      | Baseline: one task at a time            |
| Multi-threaded (with GIL)          | ~35         | ~3x     | GIL released during I/O, but parsing serialized |
| Multi-threaded (GIL-free)          | **~80**     | **~7x** | True parallelism on all cores!          |

Web scraping has both **I/O work** (fetching pages) and **CPU work** (parsing HTML). Without the GIL, both can happen in true parallel across all CPU cores.

## Repository Structure

```
unlocked_scraper/
├── scraper.py                      # Main demo: Hacker News scraper
├── demos/
│   ├── terminal_demo.py            # Beautiful terminal demo with Rich TUI
│   ├── test_server.py              # FastAPI local test server
│   └── templates/                  # Jinja2 templates for test server
│       ├── base.html
│       ├── index.html
│       ├── article.html
│       └── stats.html
├── lessons/                        # Modular learning path
│   ├── __init__.py
│   └── utils.py                    # Stats tracking & visualization
├── talk/
│   └── presentation.md             # Marp slides with Mermaid diagrams
├── tools/
│   └── qrslide.py                  # QR code generator
├── .github/workflows/
│   └── build-presentation.yml      # CI/CD for presentations
├── pyproject.toml                  # Python dependencies (uv)
├── package.json                    # npm scripts for Marp
├── PYTHON_SETUP.md                 # Setup guide
├── CLAUDE.md                       # AI assistant docs
└── README.md                       # This file
```

## Building the Presentation

The talk slides are in `talk/presentation.md` and use [Marp](https://marp.app/) with Mermaid diagrams.

### Local Development

```bash
# Build HTML presentation
npm run build:html

# Build PDF presentation
npm run build:pdf

# Build both HTML and PDF
npm run build

# Watch mode (auto-rebuild on changes)
npm run watch

# Preview in browser
npm run preview
```

### VS Code Preview

1. Install the [Marp for VS Code](https://marketplace.visualstudio.com/items?itemName=marp-team.marp-vscode) extension
2. Right-click `talk/presentation.md`
3. Select "Open with > Marp Preview"

### CI/CD Build

Presentations are automatically built on push via GitHub Actions:
- **HTML** and **PDF** artifacts are uploaded to GitHub Actions
- **GitHub Pages** deployment (on main branch) makes slides available at `https://[your-username].github.io/unlocked_scraper/presentation.html`

See `.github/workflows/build-presentation.yml` for details.

## Continuous Integration

The repository includes three GitHub Actions workflows:

### 1. CI/CD Pipeline (`.github/workflows/ci.yml`)
Main workflow that runs on every push:
- ✅ Validates Python syntax for all modules
- ✅ Checks all dependencies
- 📊 Builds HTML and PDF presentations
- 🚀 Deploys to GitHub Pages (main branch only)

### 2. Build Presentation (`.github/workflows/build-presentation.yml`)
Standalone presentation builder:
- Triggers on changes to `talk/` directory
- Builds HTML and PDF with Marp
- Uploads artifacts with 90-day retention

### 3. Test Python (`.github/workflows/test-python.yml`)
Tests Python code across versions:
- Tests Python 3.13 and 3.14
- Validates all Python files
- Checks imports and dependencies
- Smoke tests the FastAPI server

All workflows use `uv` for Python dependency management and install Marp CLI globally (no package-lock.json required).

## Key Concepts (For Novices)

### Why is web scraping a good async example?

Web scraping has a natural callback structure:
1. Fetch a page → **when it arrives**, parse it
2. The page has links → **for each link**, fetch that page too
3. Keep going → **until all pages** are processed

This "do something, then do something else" pattern is perfect for async programming!

### What's the GIL?

The Global Interpreter Lock (GIL) is a mechanism in Python that allows only one thread to execute Python code at a time, even on multi-core processors. It's been in Python since 1992 for memory safety.

### What's GIL-free Python?

Python 3.13+ introduced an experimental free-threading mode (PEP 703) that removes the GIL. This enables true parallel execution of Python code across multiple CPU cores.

Enable it with: `python -X gil=0`

## Tools

- `tools/qrslide.py` - Generate QR codes for sharing talk materials

## Contributing

This is a talk repository, but suggestions for improvements are welcome! Feel free to open issues or PRs.

## Resources

- [PEP 703: Making the Global Interpreter Lock Optional](https://peps.python.org/pep-0703/)
- [Python 3.13 Free-Threading Documentation](https://docs.python.org/3.13/howto/free-threading-python.html)
- [aiohttp Documentation](https://docs.aiohttp.org/)
- [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

## License

See LICENSE.md for details.