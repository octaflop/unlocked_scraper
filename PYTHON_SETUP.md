# Python Setup Guide for GIL vs GIL-Free Development

This guide covers how to work with both standard Python 3.14 (with GIL) and free-threaded Python 3.14 (GIL-free) using `uv`.

## Quick Start

```bash
# Install dependencies
uv sync

# Run demo with GIL (default)
uv run python scraper.py --multithreaded

# Run demo without GIL (free-threaded)
uv run python -X gil=0 scraper.py --multithreaded
```

## Understanding Python Builds

Python 3.13+ comes in two build variants:

1. **Standard build** (default): Includes the GIL
   - Compatible with all existing packages
   - Some parallelism during I/O operations
   - Single-threaded CPU-bound operations

2. **Free-threaded build** (`-X gil=0`): GIL can be disabled
   - Experimental feature (PEP 703)
   - True multi-core parallelism
   - Requires thread-safe code
   - May have slight single-threaded overhead

## Installing Python 3.14 with uv

### Method 1: Let uv manage Python (Recommended)

```bash
# uv automatically downloads and manages Python versions
uv sync
```

That's it! `uv` will:
- Read `requires-python = ">=3.14"` from `pyproject.toml`
- Download Python 3.14 if needed
- Create a virtual environment
- Install all dependencies

### Method 2: Use system Python 3.14

```bash
# Install Python 3.14 first (example with pyenv)
pyenv install 3.14.0
pyenv local 3.14.0

# Then use uv with that Python
uv sync --python $(which python)
```

### Method 3: Specify Python version explicitly

```bash
# Tell uv exactly which Python version to use
uv sync --python 3.14
```

## Checking Your Python Build

To verify if your Python supports free-threading:

```bash
# Check Python version and build info
uv run python --version
uv run python -VV

# Try to disable the GIL
uv run python -X gil=0 -c "import sys; print('GIL-free mode:', not hasattr(sys, '_is_gil_enabled') or not sys._is_gil_enabled())"
```

Expected output:
- `GIL-free mode: True` → Free-threading supported!
- `GIL-free mode: False` → Standard build (GIL always on)
- Error → Python version too old (need 3.13+)

## Running the Demo in Different Modes

### 1. Single-threaded (baseline)

```bash
uv run python scraper.py
```

Uses one asyncio event loop, one CPU core.

### 2. Multi-threaded with GIL (default Python)

```bash
uv run python scraper.py --multithreaded
```

Uses 8 threads, each with its own event loop. GIL provides some parallelism during I/O.

### 3. Multi-threaded GIL-free (free-threaded Python)

```bash
uv run python -X gil=0 scraper.py --multithreaded
```

Uses 8 threads with true multi-core parallelism. Maximum performance!

## Working with Dependencies

### Installing dependencies

```bash
# Install all dependencies
uv sync

# Install with dev dependencies
uv sync --dev

# Add a new dependency
uv add requests

# Add a dev dependency
uv add --dev pytest
```

### Upgrading dependencies

```bash
# Update all dependencies
uv sync --upgrade

# Update specific package
uv add --upgrade aiohttp
```

## Building the Presentation

The presentation doesn't require Python, just Node.js and npm:

```bash
# Install npm dependencies (Marp CLI)
npm install

# Build HTML
npm run build:html

# Build PDF
npm run build:pdf

# Build both
npm run build

# Watch mode (auto-rebuild on changes)
npm run watch

# Preview in browser
npm run preview
```

### Building presentation while developing with Python

You can work on both simultaneously:

```bash
# Terminal 1: Watch presentation changes
npm run watch

# Terminal 2: Run Python demo with GIL
uv run python scraper.py --multithreaded

# Terminal 3: Run Python demo without GIL
uv run python -X gil=0 scraper.py --multithreaded
```

## Common Workflows

### Development workflow

```bash
# 1. Clone the repo
git clone https://github.com/[your-repo]/unlocked_scraper.git
cd unlocked_scraper

# 2. Install Python dependencies
uv sync

# 3. Install npm dependencies for presentations
npm install

# 4. Make changes to code or slides
# ...

# 5. Test the demo
uv run python scraper.py --multithreaded

# 6. Build presentation
npm run build

# 7. Commit changes
git add .
git commit -m "Update demo and slides"
```

### Testing different configurations

```bash
# Test all three modes and compare results
echo "=== Mode 1: Single-threaded ===" && \
uv run python scraper.py && \
echo "\n=== Mode 2: Multi-threaded (with GIL) ===" && \
uv run python scraper.py --multithreaded && \
echo "\n=== Mode 3: Multi-threaded (GIL-free) ===" && \
uv run python -X gil=0 scraper.py --multithreaded
```

## Troubleshooting

### "Python 3.14 not found"

```bash
# Let uv download it
uv python install 3.14

# Or specify a different version
uv python install 3.13
uv sync --python 3.13
```

### "GIL cannot be disabled"

Your Python build doesn't support free-threading. Options:

1. **Use uv-managed Python**: `uv python install 3.14` (may include free-threading)
2. **Build from source**: See [Python docs](https://docs.python.org/3.14/using/configure.html#cmdoption-disable-gil)
3. **Use Python 3.13t**: Some distributions provide a separate `python3.13t` binary with free-threading

### "Module not found" errors

```bash
# Reinstall dependencies
uv sync --reinstall

# Or clear cache and reinstall
rm -rf .venv
uv sync
```

### npm/Marp issues

```bash
# Reinstall npm dependencies
rm -rf node_modules package-lock.json
npm install

# Or use npx to run without installing
npx @marp-team/marp-cli talk/presentation.md -o talk/presentation.html
```

## Advanced: Multiple Python Versions

If you need to test with multiple Python versions:

```bash
# Install multiple versions
uv python install 3.13
uv python install 3.14

# Create separate environments
uv venv --python 3.13 .venv-313
uv venv --python 3.14 .venv-314

# Activate specific environment
source .venv-313/bin/activate  # Python 3.13
# or
source .venv-314/bin/activate  # Python 3.14

# Or use uv run with specific Python
uv run --python 3.13 python scraper.py
uv run --python 3.14 python scraper.py
```

## CI/CD Considerations

The GitHub Actions workflow (`.github/workflows/build-presentation.yml`) handles:
- Building HTML and PDF presentations
- Uploading artifacts
- Deploying to GitHub Pages (on main branch)

For local CI testing:

```bash
# Install act (GitHub Actions local runner)
brew install act  # macOS
# or
sudo apt install act  # Linux

# Run the workflow locally
act push
```

## Resources

- [uv documentation](https://github.com/astral-sh/uv)
- [Python 3.14 free-threading docs](https://docs.python.org/3.14/howto/free-threading-python.html)
- [PEP 703: Making the GIL Optional](https://peps.python.org/pep-0703/)
- [Marp CLI documentation](https://github.com/marp-team/marp-cli)
