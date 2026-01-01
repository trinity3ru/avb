# URL Shortener API

A modern asynchronous URL shortener service built with FastAPI and SQLAlchemy.

## Features

- **URL Shortening**: Store long URLs and generate short unique IDs
- **Redirection**: Automatically redirect short IDs to original URLs
- **Async HTTP Client**: Test endpoint for making asynchronous HTTP requests
- **SQLAlchemy ORM**: Async database operations with SQLite
- **Type Safety**: Full type hints with Pydantic v2
- **Clean Architecture**: Organized project structure with separate layers

## API Endpoints

### 1. `POST /` - Shorten URL
Create a short ID for a URL.

**Request:**
```json
{
  "url": "https://example.com"
}
```

**Response (201 Created):**
```json
{
  "short_id": "Ab12Cd34"
}
```

### 2. `GET /{short_id}` - Redirect to Original URL
Redirects to the original URL.

**Example:** `http://127.0.0.1:8000/Ab12Cd34`

**Response:** HTTP 307 redirect to original URL

### 3. `GET /async-fetch?url=<url>` - Async HTTP Fetch
Test endpoint that fetches a URL asynchronously.

**Query Parameter:**
- `url` (required): Valid HTTP/HTTPS URL

**Response:**
```json
{
  "status_code": 200,
  "body": "..."
}
```

## Project Structure

```
app/
├── main.py                 # Application entry point
├── config.py              # Configuration settings
├── database.py            # Database connection and session
├── requirements.txt       # Python dependencies
│
├── models/                # SQLAlchemy models
│   ├── __init__.py
│   └── urls.py           # URL model
│
├── routes/                # API endpoints
│   ├── __init__.py
│   └── urls.py           # URL routes
│
├── schemas/               # Pydantic schemas
│   ├── __init__.py
│   └── url.py            # Request/response schemas
│
└── services/              # Business logic
    ├── __init__.py
    └── url_service.py    # URL shortening logic
```

## Requirements

- Python 3.10+
- SQLite (bundled with Python)

## Installation

### 1. Clone the repository

```bash
cd app
```

### 2. Create virtual environment

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## Running the Application

### Development mode

```bash
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

### Using Python directly

```bash
python main.py
```

The API will be available at: `http://127.0.0.1:8000`

### Interactive API Documentation

- **Swagger UI**: `http://127.0.0.1:8000/docs`
- **ReDoc**: `http://127.0.0.1:8000/redoc`

## Testing Endpoints

### Using cURL

**1. Shorten a URL:**
```bash
curl -X POST "http://127.0.0.1:8000/" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

**2. Redirect to original URL:**
```bash
curl -L "http://127.0.0.1:8000/Ab12Cd34"
```

**3. Test async fetch:**
```bash
curl "http://127.0.0.1:8000/async-fetch?url=https://example.com"
```

### Using PowerShell

**1. Shorten a URL:**
```powershell
Invoke-RestMethod -Method Post `
  -Uri "http://127.0.0.1:8000/" `
  -ContentType "application/json" `
  -Body '{"url":"https://example.com"}'
```

**2. Test redirect:**
```powershell
Invoke-WebRequest -Uri "http://127.0.0.1:8000/Ab12Cd34" -MaximumRedirection 0
```

**3. Test async fetch:**
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/async-fetch?url=https://example.com"
```

### Using HTTPie

```bash
# Shorten URL
http POST http://127.0.0.1:8000/ url=https://example.com

# Get redirect
http GET http://127.0.0.1:8000/Ab12Cd34

# Async fetch
http GET http://127.0.0.1:8000/async-fetch url==https://example.com
```

## Database

The application uses **SQLite** with **async support** via `aiosqlite`.

- Database file: `urls.db` (created automatically on first run)
- Tables are created automatically using SQLAlchemy migrations

### Database Schema

**Table: `urls`**
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key (auto-increment) |
| url | VARCHAR(255) | Original URL |
| short_id | VARCHAR(255) | Unique short identifier (indexed) |

## Configuration

Configuration is stored in `config.py`:

```python
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8000
```

## Technical Stack

- **FastAPI** `0.115.6` - Modern async web framework
- **Uvicorn** `0.34.0` - ASGI server
- **SQLAlchemy** `2.0.36` - Async ORM
- **aiosqlite** `0.20.0` - Async SQLite driver
- **Pydantic** `2.10.4` - Data validation
- **httpx** `0.28.1` - Async HTTP client

## Development

### Code Architecture

The project follows **clean architecture** principles:

1. **Models** (`models/`) - Database entities
2. **Schemas** (`schemas/`) - Data validation and serialization
3. **Services** (`services/`) - Business logic
4. **Routes** (`routes/`) - API endpoints
5. **Database** (`database.py`) - Database connection and session management

### Key Features

- ✅ Full async/await support
- ✅ Type hints everywhere
- ✅ Dependency injection with FastAPI
- ✅ Automatic API documentation
- ✅ Database session management
- ✅ Error handling with proper HTTP status codes

## Error Handling

- **404 Not Found**: Short ID doesn't exist
- **422 Unprocessable Entity**: Invalid request data (e.g., malformed URL)
- **500 Internal Server Error**: Failed to generate unique short ID after maximum attempts

## Notes

- Short IDs are **8 characters** long (alphanumeric: `a-zA-Z0-9`)
- The service attempts to generate a unique ID up to **5 times** before failing
- All database operations are **asynchronous**
- URLs are validated using Pydantic's `HttpUrl` type

## License

This is a training project for learning FastAPI and async Python.

## Author

Training project - FastAPI URL Shortener
