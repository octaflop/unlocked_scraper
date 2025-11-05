"""
Utility functions for lessons - stats tracking and visualization
"""

import time
from dataclasses import dataclass, field
from typing import List, Dict
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
import plotext as plt

console = Console()


@dataclass
class BenchmarkResult:
    """Stores benchmark results with timing data"""
    name: str
    duration: float
    requests_made: int
    pages_scraped: int
    bytes_downloaded: int = 0
    errors: int = 0
    timestamp: float = field(default_factory=time.time)

    @property
    def requests_per_second(self) -> float:
        return self.requests_made / self.duration if self.duration > 0 else 0

    @property
    def pages_per_second(self) -> float:
        return self.pages_scraped / self.duration if self.duration > 0 else 0


class StatsTracker:
    """Tracks and displays statistics across lessons"""

    def __init__(self):
        self.results: List[BenchmarkResult] = []

    def add_result(self, result: BenchmarkResult):
        """Add a benchmark result"""
        self.results.append(result)

    def display_comparison(self, baseline_name: str = None):
        """Display comparison table of all results"""
        if not self.results:
            console.print("[yellow]No results to display[/yellow]")
            return

        # Find baseline
        baseline = None
        if baseline_name:
            baseline = next((r for r in self.results if r.name == baseline_name), None)
        if not baseline:
            baseline = self.results[0]

        # Create table
        table = Table(title="📊 Performance Comparison", show_header=True, header_style="bold cyan")
        table.add_column("Configuration", style="cyan")
        table.add_column("Duration", justify="right", style="yellow")
        table.add_column("Pages/sec", justify="right", style="green")
        table.add_column("Speedup", justify="right", style="magenta")
        table.add_column("Efficiency", style="white")

        for result in self.results:
            speedup = baseline.duration / result.duration if result.duration > 0 else 0
            speedup_text = f"{speedup:.2f}x"

            # Determine efficiency rating
            if speedup >= 5:
                efficiency = "🚀 Excellent"
                style = "bold green"
            elif speedup >= 3:
                efficiency = "⚡ Great"
                style = "green"
            elif speedup >= 2:
                efficiency = "👍 Good"
                style = "yellow"
            else:
                efficiency = "😐 Limited"
                style = "red"

            table.add_row(
                result.name,
                f"{result.duration:.2f}s",
                f"{result.pages_per_second:.1f}",
                speedup_text,
                efficiency,
                style=style if result != baseline else None
            )

        console.print(table)

    def plot_performance_graph(self):
        """Display a terminal-based line graph of performance"""
        if len(self.results) < 2:
            return

        console.print("\n[bold cyan]📈 Performance Over Time[/bold cyan]\n")

        # Prepare data
        names = [r.name[:15] for r in self.results]  # Truncate long names
        durations = [r.duration for r in self.results]
        pages_per_sec = [r.pages_per_second for r in self.results]

        # Duration bar chart
        plt.clf()
        plt.title("Execution Time Comparison")
        plt.bar(names, durations, label="Duration (seconds)")
        plt.xlabel("Configuration")
        plt.ylabel("Time (s)")
        plt.theme("dark")
        plt.plotsize(80, 15)
        plt.show()
        console.print()

        # Throughput bar chart
        plt.clf()
        plt.title("Throughput Comparison")
        plt.bar(names, pages_per_sec, label="Pages/second", color="green")
        plt.xlabel("Configuration")
        plt.ylabel("Pages/sec")
        plt.theme("dark")
        plt.plotsize(80, 15)
        plt.show()
        console.print()

    def display_detailed_stats(self, result: BenchmarkResult):
        """Display detailed statistics for a single result"""
        stats_text = f"""
[bold]Configuration:[/bold] {result.name}
[bold]Duration:[/bold] {result.duration:.3f} seconds
[bold]Requests Made:[/bold] {result.requests_made}
[bold]Pages Scraped:[/bold] {result.pages_scraped}
[bold]Throughput:[/bold] {result.pages_per_second:.2f} pages/sec
[bold]Avg Request Time:[/bold] {(result.duration / result.requests_made * 1000):.2f}ms
"""
        if result.errors > 0:
            stats_text += f"[bold red]Errors:[/bold red] {result.errors}\n"

        console.print(Panel(stats_text.strip(), title="📊 Detailed Statistics", border_style="cyan"))


def display_lesson_header(lesson_number: int, title: str, description: str):
    """Display a beautiful lesson header"""
    header = Text()
    header.append(f"📚 Lesson {lesson_number}: ", style="bold yellow")
    header.append(f"{title}\n", style="bold cyan")
    header.append(f"{description}", style="white")

    console.print(Panel(header, border_style="yellow", padding=(1, 2)))
    console.print()


def display_concept_box(title: str, content: str, style: str = "blue"):
    """Display a concept explanation box"""
    console.print(Panel(content, title=f"💡 {title}", border_style=style, padding=(1, 2)))
    console.print()


def display_code_example(title: str, code: str):
    """Display a code example"""
    console.print(f"\n[bold cyan]{title}:[/bold cyan]")
    console.print(Panel(code, border_style="green", padding=(1, 2)))
    console.print()


def display_progress_summary(total_lessons: int, completed: int):
    """Display overall progress"""
    progress_bar = "█" * completed + "░" * (total_lessons - completed)
    percentage = (completed / total_lessons * 100) if total_lessons > 0 else 0

    summary = f"""
[bold]Learning Progress:[/bold]
{progress_bar} {percentage:.0f}%

[bold]Completed:[/bold] {completed}/{total_lessons} lessons
"""
    console.print(Panel(summary.strip(), title="🎯 Your Progress", border_style="magenta"))
