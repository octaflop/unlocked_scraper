.PHONY: help demo-single demo-multi demo-nogil demo-all qr-repo install test clean

# Default target
help:
	@echo "Available commands:"
	@echo "  make install       - Install dependencies with uv"
	@echo "  make demo-single   - Run single-threaded demo (baseline)"
	@echo "  make demo-multi    - Run multi-threaded demo with GIL"
	@echo "  make demo-nogil    - Run multi-threaded demo GIL-free"
	@echo "  make demo-all      - Run all three demos sequentially"
	@echo "  make qr-repo       - Generate QR code for repository"
	@echo "  make test          - Run tests"
	@echo "  make clean         - Clean temporary files"
	@echo ""
	@echo "Or use 'uv run' commands:"
	@echo "  uv run python scraper.py"
	@echo "  uv run python scraper.py --multithreaded"
	@echo "  uv run python -X gil=0 scraper.py --multithreaded"

# Installation
install:
	uv sync

# Demo commands
demo-single:
	@echo "=== Single-threaded Demo (Baseline) ==="
	uv run python scraper.py

demo-multi:
	@echo "=== Multi-threaded Demo (with GIL) ==="
	uv run python scraper.py --multithreaded

demo-nogil:
	@echo "=== Multi-threaded Demo (GIL-free) ==="
	uv run python -X gil=0 scraper.py --multithreaded

demo-all:
	@echo "=== Running all demos for comparison ==="
	@echo ""
	@echo "=== 1/3: Single-threaded (baseline) ==="
	@uv run python scraper.py
	@echo ""
	@echo "=== 2/3: Multi-threaded (with GIL) ==="
	@uv run python scraper.py --multithreaded
	@echo ""
	@echo "=== 3/3: Multi-threaded (GIL-free) ==="
	@uv run python -X gil=0 scraper.py --multithreaded
	@echo ""
	@echo "=== All demos completed! ==="

# Presentation tools
qr-repo:
	@echo "Generating QR code for repository..."
	@uv run python -c "from tools.qrslide import generate_qr_code; filepath = generate_qr_code('https://github.com/octaflop/unlocked_scraper', 'talk/repo-qr.svg'); print(f'✓ QR code saved: {filepath}')"

# Testing
test:
	@echo "Running tests..."
	uv run pytest tests/ -v

# Cleanup
clean:
	@echo "Cleaning temporary files..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@echo "✓ Clean complete"
