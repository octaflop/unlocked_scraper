# Quick Start Guide

## Installation

```bash
# Clone and install
git clone https://github.com/octaflop/unlocked_scraper.git
cd unlocked_scraper
uv sync
```

## Run Demos (Choose One Method)

### Method 1: Make (Recommended - Works Everywhere)
```bash
make demo-single    # Single-threaded
make demo-multi     # Multi-threaded with GIL
make demo-nogil     # GIL-free (requires Python 3.14 free-threading)
make demo-all       # Run all three
```

### Method 2: Just (Modern Alternative)
```bash
# Install just first: https://just.systems/
just demo-single
just demo-multi
just demo-nogil
just demo-all
```

### Method 3: Direct Python
```bash
uv run python scraper.py
uv run python scraper.py --multithreaded
uv run python -X gil=0 scraper.py --multithreaded
```

## Expected Results

| Mode | Speed | Speedup |
|------|-------|---------|
| Single-threaded | ~12 stories/sec | 1x (baseline) |
| Multi-threaded (GIL) | ~35 stories/sec | ~3x |
| Multi-threaded (no GIL) | ~80 stories/sec | ~7x |

## Other Useful Commands

```bash
# Generate QR code for sharing
make qr-repo

# Run tests
make test

# Clean temporary files
make clean

# Show all commands
make help
```

## Learn More

- Full documentation: [README.md](README.md)
- All commands: [DEMO_COMMANDS.md](DEMO_COMMANDS.md)
- What changed: [CHANGES_SUMMARY.md](CHANGES_SUMMARY.md)
