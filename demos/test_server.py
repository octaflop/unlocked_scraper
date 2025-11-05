"""
FastAPI Test Server - Local Web Scraping Target
Generates pages with links to simulate a real website for testing scrapers.

Run: uvicorn demos.test_server:app --reload
Access: http://127.0.0.1:8000
"""

import random
import time
from datetime import datetime
from typing import List, Optional

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI(title="Web Scraping Test Server")

# Set up Jinja2 templates
templates = Jinja2Templates(directory="demos/templates")

# In-memory stats tracking
request_stats = {
    "total_requests": 0,
    "page_views": 0,
    "article_views": 0,
    "start_time": datetime.now()
}


class Article(BaseModel):
    """Article data model"""
    id: int
    title: str
    author: str
    content: str
    tags: List[str]
    views: int = 0


# Generate sample articles
SAMPLE_ARTICLES = [
    Article(
        id=i,
        title=f"Understanding {'Async' if i % 2 == 0 else 'Threading'} in Python: Part {i}",
        author=random.choice(["Alice", "Bob", "Charlie", "Diana", "Eve"]),
        content=f"This is article {i}. " + " ".join(
            [f"Interesting content about topic {j}." for j in range(10)]
        ),
        tags=random.sample(["python", "async", "gil", "performance", "web", "scraping"], k=3)
    )
    for i in range(1, 101)  # 100 articles
]


@app.middleware("http")
async def add_stats_middleware(request: Request, call_next):
    """Track request statistics"""
    request_stats["total_requests"] += 1

    # Simulate realistic server processing time
    time.sleep(random.uniform(0.01, 0.05))

    response = await call_next(request)
    return response


@app.get("/", response_class=HTMLResponse)
async def index(request: Request, page: int = 1):
    """Homepage with paginated article list"""
    request_stats["page_views"] += 1

    articles_per_page = 10
    start_idx = (page - 1) * articles_per_page
    end_idx = start_idx + articles_per_page

    paginated_articles = SAMPLE_ARTICLES[start_idx:end_idx]
    total_pages = (len(SAMPLE_ARTICLES) + articles_per_page - 1) // articles_per_page

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "articles": paginated_articles,
            "page": page,
            "total_pages": total_pages,
            "stats": request_stats
        }
    )


@app.get("/article/{article_id}", response_class=HTMLResponse)
async def article(request: Request, article_id: int):
    """Individual article page"""
    request_stats["article_views"] += 1

    # Find the article
    article = next((a for a in SAMPLE_ARTICLES if a.id == article_id), None)
    if not article:
        return HTMLResponse(content="Article not found", status_code=404)

    # Increment views
    article.views += 1

    # Related articles (3 random articles)
    related = random.sample(
        [a for a in SAMPLE_ARTICLES if a.id != article_id],
        k=min(3, len(SAMPLE_ARTICLES) - 1)
    )

    return templates.TemplateResponse(
        "article.html",
        {
            "request": request,
            "article": article,
            "related": related,
            "stats": request_stats
        }
    )


@app.get("/stats", response_class=HTMLResponse)
async def stats(request: Request):
    """Statistics page"""
    uptime = datetime.now() - request_stats["start_time"]

    # Calculate additional stats
    total_views = sum(a.views for a in SAMPLE_ARTICLES)
    most_viewed = sorted(SAMPLE_ARTICLES, key=lambda x: x.views, reverse=True)[:5]

    return templates.TemplateResponse(
        "stats.html",
        {
            "request": request,
            "stats": request_stats,
            "uptime_seconds": int(uptime.total_seconds()),
            "total_article_views": total_views,
            "most_viewed": most_viewed,
            "total_articles": len(SAMPLE_ARTICLES)
        }
    )


@app.get("/api/stats")
async def api_stats():
    """API endpoint for stats (JSON)"""
    uptime = datetime.now() - request_stats["start_time"]

    return {
        **request_stats,
        "uptime_seconds": int(uptime.total_seconds()),
        "total_articles": len(SAMPLE_ARTICLES),
        "total_article_views": sum(a.views for a in SAMPLE_ARTICLES)
    }


@app.get("/api/articles")
async def api_articles(page: int = 1, limit: int = 10):
    """API endpoint for articles list (JSON)"""
    start_idx = (page - 1) * limit
    end_idx = start_idx + limit

    return {
        "page": page,
        "limit": limit,
        "total": len(SAMPLE_ARTICLES),
        "articles": [a.model_dump() for a in SAMPLE_ARTICLES[start_idx:end_idx]]
    }


if __name__ == "__main__":
    import uvicorn
    print("Starting test server on http://127.0.0.1:8000")
    print("Visit /stats to see server statistics")
    uvicorn.run(app, host="127.0.0.1", port=8000)
