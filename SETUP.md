# Quick Setup Guide

## Docker Setup (Recommended)

```bash
# 1. Copy environment template
cp .env.example .env

# 2. Start the application
docker-compose up --build

# 3. Access the API
# http://127.0.0.1:8000
# Docs: http://127.0.0.1:8000/docs
```

## Local Development Setup

```bash
# 1. Create virtual environment
python -m venv .venv

# 2. Activate virtual environment
# Windows
.\.venv\Scripts\Activate.ps1
# Linux/macOS
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Copy environment template
cp .env.example .env

# 5. Run database migrations
alembic upgrade head

# 6. Start the application
cd app
python -m uvicorn main:app --reload
```

## Common Commands

### Database Migrations
```bash
# Create new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

### Code Quality
```bash
# Format code
ruff format app/

# Check for issues
ruff check app/

# Auto-fix issues
ruff check --fix app/
```

### Docker
```bash
# View logs
docker-compose logs -f app

# Stop containers
docker-compose down

# Rebuild
docker-compose up --build
```

## Troubleshooting

### Port already in use
Change `SERVER_PORT` in `.env` file.

### Database locked
Stop all running instances and delete `urls.db` file, then run `alembic upgrade head` again.

### Module not found errors
Make sure you're in the correct directory and virtual environment is activated.
