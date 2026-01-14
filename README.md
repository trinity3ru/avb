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

- Python 3.11+
- SQLite (bundled with Python)
- Docker (optional, recommended)

## Installation

### Option 1: Docker (Recommended)

#### Development

```bash
# Copy environment template
cp .env.example .env

# Build and run with docker-compose
docker-compose up --build

# The API will be available at: http://127.0.0.1:8000
```

#### Production

```bash
# Copy and configure environment
cp .env.example .env
# Edit .env with production settings

# Build and run production version
docker-compose -f docker-compose.prod.yml up -d --build
```

### Option 2: Local Setup

#### 1. Clone the repository

```bash
git clone <repository-url>
cd AVB
```

#### 2. Create virtual environment

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Linux/macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

#### 3. Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 4. Configure environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env if needed
```

#### 5. Run database migrations

```bash
# Initialize database with Alembic
alembic upgrade head
```

## Running the Application

### Development mode (local)

```bash
# From project root
cd app
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

### Using Python directly

```bash
cd app
python -m uvicorn main:app --host 127.0.0.1 --port 8000
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

- Database file: `urls.db` (or configured path in `.env`)
- Schema management via **Alembic migrations**

### Database Schema

**Table: `urls`**
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key (auto-increment) |
| url | VARCHAR(255) | Original URL |
| short_id | VARCHAR(255) | Unique short identifier (indexed) |

### Alembic Migrations

```bash
# Create a new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# Show current revision
alembic current

# Show migration history
alembic history
```

## Configuration

Configuration is managed via **environment variables** (`.env` file):

```bash
# Server Configuration
SERVER_HOST=127.0.0.1
SERVER_PORT=8000

# Database Configuration
DATABASE_URL=sqlite+aiosqlite:///urls.db
```

See [.env.example](.env.example) for all available options.

## Technical Stack

- **FastAPI** `0.115.6` - Modern async web framework
- **Uvicorn** `0.34.0` - ASGI server
- **SQLAlchemy** `2.0.36` - Async ORM
- **aiosqlite** `0.20.0` - Async SQLite driver
- **Alembic** `1.14.0` - Database migrations
- **Pydantic** `2.10.4` - Data validation
- **httpx** `0.28.1` - Async HTTP client
- **Ruff** `0.8.5` - Code formatter and linter
- **Docker** - Containerization

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
- ✅ Database migrations with Alembic
- ✅ Docker containerization
- ✅ Environment-based configuration
- ✅ Code quality with Ruff
- ✅ Error handling with proper HTTP status codes

### Code Quality

```bash
# Check code with ruff
ruff check app/

# Auto-fix issues
ruff check --fix app/

# Format code
ruff format app/
```

### Docker Commands

```bash
# Development
docker-compose up --build          # Build and start
docker-compose down                # Stop containers
docker-compose logs -f app         # View logs

# Production
docker-compose -f docker-compose.prod.yml up -d --build
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml logs -f app

# Database migrations in Docker
docker-compose exec app alembic upgrade head
docker-compose exec app alembic revision --autogenerate -m "migration name"
```

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
