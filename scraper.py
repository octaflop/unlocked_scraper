# scraper.py
# Web scraping demo for GIL-free Python 3.14 talk
# Demonstrates performance differences between:
# 1. Single-threaded async
# 2. Multi-threaded with GIL
# 3. Multi-threaded without GIL (python -X gil=0)

import aiohttp
import asyncio
from bs4 import BeautifulSoup
from queue import Queue, Empty
from concurrent.futures import ThreadPoolExecutor
from time import perf_counter
from argparse import ArgumentParser

BASE_URL = "https://news.ycombinator.com/news?p={}"
ITEM_URL = "https://news.ycombinator.com/item?id={}"


async def fetch(session: aiohttp.ClientSession, url: str) -> str:
    """Fetch a single page from the web.

    This is an async function that waits for the network response.
    In traditional Python, the GIL is released during this I/O wait,
    allowing other threads to run.
    """
    async with session.get(url, timeout=100) as response:
        return await response.text()


def parse_stories(html: str) -> list[dict]:
    """Extract story information from a Hacker News page.

    This parsing happens on the CPU and is affected by the GIL.
    With free-threaded Python, multiple threads can parse simultaneously.
    """
    soup = BeautifulSoup(html, "html.parser")
    stories = []

    for item in soup.select(".athing"):
        title_tag = item.select_one(".titleline > a")
        story_id = item.get("id")

        if title_tag and story_id:
            title = title_tag.text.strip()
            link = title_tag["href"].strip()
            stories.append({"id": story_id, "title": title, "link": link})

    return stories


def parse_comments(html: str) -> list[dict]:
    """Extract comments from a Hacker News story page.

    Like parse_stories, this CPU-bound parsing benefits from
    true parallelism in free-threaded Python.
    """
    soup = BeautifulSoup(html, "html.parser")
    comments = []

    for row in soup.select("tr.comtr"):
        user_tag = row.select_one(".hnuser")
        comment_tag = row.select_one(".commtext")

        if user_tag and comment_tag:
            user = user_tag.text.strip()
            text = comment_tag.get_text(separator=" ", strip=True)
            comments.append({"user": user, "text": text})

    return comments


async def fetch_story_with_comments(
    session: aiohttp.ClientSession, story: dict
) -> dict:
    """Fetch a story's comment page and add comments to the story dict.

    This demonstrates the callback nature of web scraping:
    - We fetch a page (the main story list)
    - That page has links to other pages (individual stories)
    - We follow those links and fetch more data
    """
    comment_html = await fetch(session, ITEM_URL.format(story["id"]))
    story["comments"] = parse_comments(comment_html)
    return story


async def worker(queue: Queue, all_stories: list) -> None:
    """Worker coroutine that processes pages from a shared queue.

    Each worker:
    1. Gets a page URL from the queue
    2. Fetches the page
    3. Parses the stories on that page
    4. For each story, creates a task to fetch its comments
    5. Adds all stories to the shared list

    The TaskGroup ensures all comment fetches complete before moving on.
    """
    async with aiohttp.ClientSession() as session:
        while True:
            async with asyncio.TaskGroup() as tg:
                try:
                    page = queue.get(block=False)
                except Empty:
                    break
                html = await fetch(session, page)
                stories = parse_stories(html)
                if not stories:
                    break
                # Create concurrent tasks to fetch all story comments
                for story in stories:
                    tg.create_task(fetch_story_with_comments(session, story))
            all_stories.extend(stories)


def main(multithreaded: bool) -> None:
    """Main orchestration function.

    When multithreaded=False:
        Runs a single asyncio event loop in the main thread.
        Fast due to async I/O, but limited to one core.

    When multithreaded=True:
        Creates multiple threads, each running its own asyncio event loop.

        With GIL (default Python):
            Gets some parallelism during I/O waits, but CPU work is serialized.
            Performance improvement is moderate.

        Without GIL (python -X gil=0):
            True parallelism! All CPU cores can work simultaneously on both
            I/O and CPU-bound work. Maximum performance.
    """
    queue = Queue()
    all_stories = []

    # Add 100 pages to scrape
    for page in range(1, 101):
        queue.put(BASE_URL.format(page))

    start_time = perf_counter()

    if multithreaded:
        print("Using multithreading for fetching stories...")
        workers: int = 8  # Number of CPU cores to use
        with ThreadPoolExecutor(max_workers=workers) as executor:
            # Each thread runs its own asyncio event loop
            for _ in range(workers):
                executor.submit(lambda: asyncio.run(worker(queue, all_stories)))
    else:
        print("Using single thread for fetching stories...")
        asyncio.run(worker(queue, all_stories))

    end_time = perf_counter()
    elapsed = end_time - start_time

    # Display results
    print(f"\n{'='*60}")
    print(f"Total stories scraped: {len(all_stories)}")
    print(f"Time elapsed: {elapsed:.2f} seconds")
    print(f"Scraping speed: {len(all_stories) / elapsed:.0f} stories/sec")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    parser = ArgumentParser(description="Scrape Hacker News stories and comments.")
    parser.add_argument(
        "--multithreaded",
        action="store_true",
        default=False,
        help="Use multithreading for fetching stories.",
    )
    args = parser.parse_args()
    main(args.multithreaded)
