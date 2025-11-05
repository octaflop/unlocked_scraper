"""
Python 3.14 No-GIL Web Scraping Demo - Beautiful Terminal Edition
Demonstrates the performance difference between GIL and GIL-free Python
for web scraping workloads (I/O + CPU work).

Install: pip install rich aiohttp beautifulsoup4
Run: python demos/terminal_demo.py              # With GIL
 or: python -X gil=0 demos/terminal_demo.py     # Without GIL (FREE-THREADING!)
"""

import asyncio
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from typing import List

import aiohttp
from bs4 import BeautifulSoup
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.progress import (BarColumn, Progress, SpinnerColumn,
                           TaskProgressColumn, TextColumn)
from rich.table import Table
from rich.text import Text

console = Console()


class WebScrapingDemo:
    """Demonstrates web scraping performance with/without GIL"""

    def __init__(self):
        self.gil_status = self._check_gil_status()
        self.test_urls = [
            f"https://news.ycombinator.com/news?p={i}"
            for i in range(1, 11)  # 10 pages
        ]

    def _check_gil_status(self) -> str:
        """Check if GIL is enabled or disabled"""
        try:
            return "DISABLED ✓" if not sys._is_gil_enabled() else "ENABLED"
        except AttributeError:
            return "ENABLED"

    async def fetch_and_parse(self, session: aiohttp.ClientSession, url: str) -> int:
        """Fetch a page and parse it (I/O + CPU work)"""
        try:
            async with session.get(url, timeout=10) as response:
                html = await response.text()

                # CPU-bound work: Parse HTML with BeautifulSoup
                soup = BeautifulSoup(html, "html.parser")
                stories = soup.select(".athing")

                # More CPU work: extract data from each story
                story_count = 0
                for story in stories:
                    title_tag = story.select_one(".titleline > a")
                    if title_tag:
                        # Simulate some text processing (CPU work)
                        _ = title_tag.text.strip().lower().split()
                        story_count += 1

                return story_count
        except Exception as e:
            return 0

    async def scrape_pages(self, urls: List[str], worker_id: int = 0) -> int:
        """Scrape multiple pages in one async session"""
        total_stories = 0
        async with aiohttp.ClientSession() as session:
            tasks = [self.fetch_and_parse(session, url) for url in urls]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            total_stories = sum(r for r in results if isinstance(r, int))
        return total_stories


def create_header(gil_status: str) -> Panel:
    """Create a beautiful header"""
    gil_color = "green" if "DISABLED" in gil_status else "red"

    title = Text()
    title.append("🕷️  Python 3.14 Web Scraping Demo\n", style="bold cyan")
    title.append("GIL Status: ", style="white")
    title.append(f"{gil_status}", style=f"bold {gil_color}")

    return Panel(title, border_style="cyan")


def run_single_threaded(demo: WebScrapingDemo) -> tuple[float, int]:
    """Run async scraping in a single thread"""
    console.print("\n[bold yellow]▶ Running Single-Threaded (1 async loop)...[/bold yellow]\n")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console
    ) as progress:
        task = progress.add_task("[cyan]Scraping pages...", total=1)

        start = time.perf_counter()
        total_stories = asyncio.run(demo.scrape_pages(demo.test_urls))
        elapsed = time.perf_counter() - start

        progress.update(task, completed=1)

    console.print(
        f"✓ [bold green]Single-threaded Complete![/bold green] "
        f"Time: [bold]{elapsed:.2f}s[/bold] | "
        f"Stories: {total_stories}\n"
    )
    return elapsed, total_stories


def run_multi_threaded(demo: WebScrapingDemo, num_workers: int = 4) -> tuple[float, int]:
    """Run async scraping across multiple threads"""
    console.print(f"\n[bold green]▶▶▶ Running Multi-threaded ({num_workers} workers)...[/bold green]\n")

    # Split URLs among workers
    urls_per_worker = len(demo.test_urls) // num_workers
    url_chunks = [
        demo.test_urls[i:i + urls_per_worker]
        for i in range(0, len(demo.test_urls), urls_per_worker)
    ]

    results = [0] * len(url_chunks)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console
    ) as progress:
        # Create progress bars for each worker
        tasks = {}
        for i in range(len(url_chunks)):
            tasks[i] = progress.add_task(f"[magenta]Worker {i + 1}", total=1)

        start = time.perf_counter()

        with ThreadPoolExecutor(max_workers=num_workers) as executor:
            futures = {
                executor.submit(asyncio.run, demo.scrape_pages(chunk, i)): i
                for i, chunk in enumerate(url_chunks)
            }

            for future in futures:
                worker_id = futures[future]
                results[worker_id] = future.result()
                progress.update(tasks[worker_id], completed=1)

        elapsed = time.perf_counter() - start

    total_stories = sum(results)
    console.print(
        f"✓ [bold green]Multi-threaded Complete![/bold green] "
        f"Time: [bold]{elapsed:.2f}s[/bold] | "
        f"Stories: {total_stories}\n"
    )
    return elapsed, total_stories


def display_results(single_time: float, multi_time: float, gil_status: str):
    """Display comparison results"""
    speedup = single_time / multi_time if multi_time > 0 else 0

    table = Table(title="📊 Performance Comparison", border_style="cyan")
    table.add_column("Mode", style="cyan", justify="left")
    table.add_column("Time", style="yellow", justify="right")
    table.add_column("Speedup", style="white", justify="right")
    table.add_column("Notes", style="white")

    table.add_row(
        "Single-threaded",
        f"{single_time:.2f}s",
        "1.00x",
        "Baseline: 1 async loop"
    )

    speedup_text = f"{speedup:.2f}x"
    if speedup > 3:
        speedup_style = "bold green"
        emoji = "🚀 Excellent!"
    elif speedup > 2:
        speedup_style = "bold yellow"
        emoji = "👍 Good!"
    else:
        speedup_style = "bold red"
        emoji = "😐 Limited"

    table.add_row(
        "Multi-threaded",
        f"{multi_time:.2f}s",
        speedup_text,
        emoji,
        style=speedup_style
    )

    console.print(table)

    # Explanation panel
    console.print()
    if "DISABLED" in gil_status:
        if speedup > 3:
            message = (
                "[bold green]🎉 SUCCESS![/bold green]\n\n"
                "Free-threading is working! You're seeing true multi-core\n"
                "parallelism for both I/O (fetching) and CPU work (parsing).\n\n"
                "[bold]Why web scraping benefits:[/bold]\n"
                "• I/O: Fetching pages (network bound)\n"
                "• CPU: Parsing HTML with BeautifulSoup\n"
                "• Without GIL: Both can happen in parallel! 🚀"
            )
            style = "green"
        else:
            message = (
                "[bold yellow]⚠️  Moderate Speedup[/bold yellow]\n\n"
                "GIL is disabled but speedup is moderate. Possible reasons:\n"
                "• Network latency dominates (I/O bound)\n"
                "• Not enough CPU-intensive parsing\n"
                "• Try with more pages or heavier parsing"
            )
            style = "yellow"
    else:
        message = (
            "[bold red]ℹ️  GIL is Enabled[/bold red]\n\n"
            "The GIL limits parallelism during HTML parsing.\n"
            "I/O gets some parallelism, but CPU work is serialized.\n\n"
            "To see the full power of free-threading:\n\n"
            "[cyan]python -X gil=0 demos/terminal_demo.py[/cyan]\n\n"
            "[bold]Expected improvement:[/bold] 2-4x faster! 🚀"
        )
        style = "red"

    console.print(Panel(message, border_style=style))


def main():
    demo = WebScrapingDemo()

    # Display header
    console.clear()
    console.print(create_header(demo.gil_status))
    console.print()

    # Display Python version
    console.print(f"[dim]Python {sys.version}[/dim]\n")

    # Show instructions
    info_panel = Panel(
        "[bold]What This Demonstrates:[/bold]\n\n"
        "• [yellow]Single-threaded:[/yellow] 1 async event loop (baseline)\n"
        "• [green]Multi-threaded:[/green] 4 async loops running in parallel\n\n"
        "[bold]Why Web Scraping?[/bold]\n"
        "• [blue]I/O work:[/blue] Fetching pages over network\n"
        "• [blue]CPU work:[/blue] Parsing HTML with BeautifulSoup\n\n"
        "[bold]Expected Results:[/bold]\n"
        "• [red]With GIL:[/red] ~2-3x speedup (I/O helps, CPU limited)\n"
        "• [green]Without GIL:[/green] ~3-5x speedup (true parallelism!) 🚀\n\n"
        "[dim]Scraping 10 pages from Hacker News...\nPress Ctrl+C to exit[/dim]",
        border_style="blue",
        title="ℹ️  Info"
    )
    console.print(info_panel)
    console.print()

    try:
        # Run single-threaded test
        single_time, single_stories = run_single_threaded(demo)

        # Run multi-threaded test
        multi_time, multi_stories = run_multi_threaded(demo, num_workers=4)

        # Display results
        console.print()
        display_results(single_time, multi_time, demo.gil_status)
        console.print()

    except KeyboardInterrupt:
        console.print("\n\n[yellow]Test interrupted by user[/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n[bold red]Error:[/bold red] {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
