# Demo Commands Reference

This document lists all the available commands for running demos and presentation tools.

## Prerequisites

```bash
# Install dependencies (requires Python 3.14)
uv sync
# or
make install
# or
just install

# Verify Python version
uv run python --version
```

## Quick Start

You can run demos using any of these command tools:
- **Make**: `make demo-single` (most universal, works everywhere)
- **Just**: `just demo-single` (modern alternative to Make, requires [just](https://just.systems/))
- **Direct Python**: `uv run python scraper.py` (most explicit)

All examples below show all three methods.

## Web Scraping Demos

### Single-threaded Baseline

Runs the scraper in single-threaded mode (baseline performance):

```bash
make demo-single
# or
just demo-single
# or
uv run python scraper.py
```

**What it does:** Scrapes 100 pages of Hacker News using a single async event loop in one thread.

**Expected performance:** ~12 stories/sec (1x baseline)

### Multi-threaded with GIL

Runs the scraper with multiple threads but with the GIL enabled (default Python):

```bash
make demo-multi
# or
just demo-multi
# or
uv run python scraper.py --multithreaded
```

**What it does:** Uses 8 worker threads, each running its own async event loop. The GIL limits true parallelism but some speedup occurs during I/O waits.

**Expected performance:** ~35 stories/sec (~3x speedup)

### Multi-threaded GIL-free

Runs the scraper with multiple threads and the GIL disabled (free-threaded Python 3.14):

```bash
make demo-nogil
# or
just demo-nogil
# or
uv run python -X gil=0 scraper.py --multithreaded
```

**What it does:** Uses 8 worker threads with GIL disabled, achieving true multi-core parallelism.

**Expected performance:** ~80 stories/sec (~7x speedup)

**Requirements:** Python 3.14 with free-threading support

### Run All Demos

Runs all three demos in sequence for easy comparison:

```bash
make demo-all
# or
just demo-all
```

**What it does:** Executes single-threaded, multi-threaded (with GIL), and GIL-free demos consecutively, displaying results for comparison.

## Presentation Tools

### Generate QR Code for Repository

Creates a QR code SVG for sharing the repository link:

```bash
make qr-repo
# or
just qr-repo
```

**What it does:** Generates `talk/repo-qr.svg` containing a QR code that links to the GitHub repository.

**Usage:** Embed this QR code in presentation slides for easy sharing with the audience.

### Custom QR Code

To generate a custom QR code, use Python directly:

```bash
uv run python -c "from tools.qrslide import generate_qr_code; generate_qr_code('YOUR_TEXT_HERE', 'output.svg')"
```

## Additional Commands

### Build Presentation (requires Node.js and Marp)

```bash
# Build HTML
just build-html

# Build PDF
just build-pdf

# Build both
just build-all
```

### Check Python and GIL Status

```bash
just check-python
```

### Clean Temporary Files

```bash
make clean
# or
just clean
```

### Run Tests

```bash
make test
# or
just test
```

## Understanding the Results

When you run a demo, you'll see output like:

```
============================================================
Total stories scraped: 2847
Time elapsed: 35.67 seconds
Scraping speed: 80 stories/sec
============================================================
```

### Key Learning Points

1. **Single-threaded is surprisingly fast** due to async I/O handling
2. **Multi-threaded with GIL** provides moderate speedup (2-3x) because the GIL is released during I/O waits
3. **GIL-free Python** achieves dramatic speedup (6-8x) with true multi-core parallelism
4. **Web scraping is ideal for async** because it's I/O-bound with a natural callback structure (following links)

## Performance Notes

- Results vary based on CPU cores, network speed, and system load
- Expected results shown are from a 12-core CPU with good network connectivity
- CI/CD environments may show different results due to limited resources
- For best results, run demos locally on a multi-core machine

## Troubleshooting

### Command not found

If commands don't work:

```bash
# For Make commands
make --version  # Ensure Make is installed

# For Just commands
just --version  # Install just from https://just.systems/

# For direct Python
uv sync  # Ensure dependencies are installed
uv run python scraper.py  # Use direct Python invocation
```

### GIL-free mode not working

The `demo-nogil` command requires Python 3.14 with free-threading support:

```bash
# Check if free-threading is available
uv run python -c "import sys; print('Free-threading:', hasattr(sys, '_is_gil_enabled'))"
```

If free-threading is not available, you may need to install a free-threaded build of Python 3.14.
