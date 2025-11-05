# Justfile for unlocked_scraper
# Run with: just <command>
# List commands: just --list

# Default recipe to display help
default:
    @just --list

# Install dependencies
install:
    uv sync

# Run single-threaded demo (baseline)
demo-single:
    @echo "=== Single-threaded Demo (Baseline) ==="
    uv run python scraper.py

# Run multi-threaded demo with GIL
demo-multi:
    @echo "=== Multi-threaded Demo (with GIL) ==="
    uv run python scraper.py --multithreaded

# Run multi-threaded demo GIL-free
demo-nogil:
    @echo "=== Multi-threaded Demo (GIL-free) ==="
    uv run python -X gil=0 scraper.py --multithreaded

# Run all three demos in sequence for comparison
demo-all:
    @echo "=== Running all demos for comparison ==="
    @echo ""
    @echo "=== 1/3: Single-threaded (baseline) ==="
    @just demo-single
    @echo ""
    @echo "=== 2/3: Multi-threaded (with GIL) ==="
    @just demo-multi
    @echo ""
    @echo "=== 3/3: Multi-threaded (GIL-free) ==="
    @just demo-nogil
    @echo ""
    @echo "=== All demos completed! ==="

# Generate QR code for repository
qr-repo:
    @echo "Generating QR code for repository..."
    @uv run python -c "from tools.qrslide import generate_qr_code; filepath = generate_qr_code('https://github.com/octaflop/unlocked_scraper', 'talk/repo-qr.svg'); print(f'✓ QR code saved: {filepath}')"

# Run tests
test:
    uv run pytest tests/ -v

# Clean temporary files
clean:
    @echo "Cleaning temporary files..."
    @find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    @find . -type f -name "*.pyc" -delete 2>/dev/null || true
    @find . -type f -name "*.pyo" -delete 2>/dev/null || true
    @find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
    @echo "✓ Clean complete"

# Build presentation HTML
build-html:
    @echo "Building HTML presentation..."
    marp talk/presentation.md --html --allow-local-files -o talk/presentation.html
    @echo "✓ HTML presentation built: talk/presentation.html"

# Build presentation PDF
build-pdf:
    @echo "Building PDF presentation..."
    marp talk/presentation.md --html --allow-local-files --pdf -o talk/presentation.pdf
    @echo "✓ PDF presentation built: talk/presentation.pdf"

# Build both HTML and PDF presentations
build-all: build-html build-pdf
    @echo "✓ All presentations built"

# Check Python version and GIL status
check-python:
    @echo "Python version:"
    @uv run python --version
    @echo ""
    @echo "Detailed version info:"
    @uv run python -VV
    @echo ""
    @echo "GIL status:"
    @uv run python -c "import sys; print(f'Free-threading available: {hasattr(sys, \"_is_gil_enabled\")}')"
    @uv run python -c "import sys; print(f'GIL enabled: {not hasattr(sys, \"_is_gil_enabled\") or sys._is_gil_enabled()}') if hasattr(sys, '_is_gil_enabled') else print('GIL enabled: True (default)')"
