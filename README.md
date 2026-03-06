# Topic Intelligence System

A FastAPI backend that aggregates RSS feeds across multiple categories, ranks articles by topic relevance, caches results in Redis, and stores matched articles in a database.

## Features

- Topic-based article search from RSS feeds
- Categories: `news`, `tech`, `sports`, `finance`
- Relevance scoring based on title/summary matches
- Redis caching (auto-disables if Redis is unavailable)
- Database persistence with PostgreSQL and automatic SQLite fallback
- Pagination support in API responses

## Project Structure

```text
backend/
  app/
    api/          # FastAPI routes
    core/         # Logger, DB engine/session, Redis client
    models/       # SQLAlchemy models
    schemas/      # Pydantic response models
    scrapers/     # RSS scraper + category feed sources
    services/     # Query orchestration, scoring, caching, persistence
```

## Requirements

- Python 3.10+
- Optional: PostgreSQL
- Optional: Redis

Install dependencies:

```bash
cd backend
pip install -r requirements.txt
```

## Environment Variables

The app works without extra configuration, but supports:

- `DATABASE_URL` (default: `postgresql://postgres:postgres@localhost:5432/news`)
- `REDIS_URL` (preferred Redis connection string)
- `REDIS_HOST` (default: `localhost`)
- `REDIS_PORT` (default: `6379`)

Notes:

- If `DATABASE_URL` is unreachable, the app falls back to local SQLite: `topic_intelligence.db`.
- If Redis is unavailable, caching is disabled and requests still succeed.

## Run Locally

```bash
cd backend
uvicorn app.main:app --reload
```

API will be available at:

- `http://127.0.0.1:8000/`
- Swagger UI: `http://127.0.0.1:8000/docs`

## API Endpoints

### `GET /`

Health/welcome message.

### `GET /search`

Query parameters:

- `topic` (required): search keyword
- `category` (optional): `news` | `tech` | `sports` | `finance` (default: `news`)
- `page` (optional): page number, minimum `1` (default: `1`)
- `size` (optional): page size, `1` to `50` (default: `10`)

Example:

```bash
curl "http://127.0.0.1:8000/search?topic=ai&category=tech&page=1&size=10"
```

Response shape:

```json
{
  "topic": "ai",
  "page": 1,
  "size": 10,
  "total_results": 27,
  "results": [
    {
      "id": "article-guid-or-link",
      "title": "Article title",
      "link": "https://example.com/article",
      "summary": "Article summary",
      "pubDate": "2026-03-06T12:00:00+00:00",
      "score": 3
    }
  ]
}
```

## Scoring Logic

- +2 if the topic appears in article title
- +1 if the topic appears in article summary
- Only articles with score `> 0` are returned
- Results are sorted by score, then publication date (newest first)

## Docker

`backend/Dockerfile` exists but is currently empty. Add container instructions there before using Docker for this project.
