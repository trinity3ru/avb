# AVB - FastAPI URL Shortener (training)

A small FastAPI service:

- `POST /` - stores the original URL and returns a `short_id`
- `GET /{short_id}` - redirects (307) to the original URL
- `GET /async-fetch?url=...` - performs an async HTTP GET to the given URL and returns the data

## Requirements

- Python 3.11+
- (optional) Postman or curl

## Local run (Windows / PowerShell)

1) Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -U pip
```

2) Install dependencies:

```powershell
pip install fastapi uvicorn[standard] python-dotenv httpx
```

3) Start the server:

```powershell
uvicorn main:app --host 127.0.0.1 --port 8080 --reload
```

After startup the service is available at `http://127.0.0.1:8080`.

## Database

On startup the app creates a SQLite file `urls.db` in the project root and a `urls` table.

## Testing endpoints

### 1) Shorten a URL - `POST /`

**curl:**

```bash
curl -i -X POST "http://127.0.0.1:8080/" \
  -H "Content-Type: application/json" \
  -d "{\"original_url\": \"https://example.com\"}"
```

**PowerShell:**

```powershell
Invoke-RestMethod -Method Post `
  -Uri "http://127.0.0.1:8080/" `
  -ContentType "application/json" `
  -Body '{"original_url":"https://example.com"}'
```

Expected: HTTP `201` and JSON like:

```json
{"short_id":"Ab12Cd","original_url":"https://example.com"}
```

### 2) Follow a short link - `GET /{short_id}`

Open in a browser:

- `http://127.0.0.1:8080/<short_id>`

Or check the `Location` header:

```bash
curl -i "http://127.0.0.1:8080/<short_id>"
```

Expected: HTTP `307` and `Location: https://example.com`.

### 3) Async outbound request - `GET /async-fetch?url=...`

This endpoint performs an outbound HTTP GET to the provided URL and returns:

- `status_code` - response code from the external service
- `body` - response body as text

**curl:**

```bash
curl -s "http://127.0.0.1:8080/async-fetch?url=https%3A%2F%2Fexample.com"
```

**PowerShell:**

```powershell
Invoke-RestMethod -Method Get -Uri "http://127.0.0.1:8080/async-fetch?url=https%3A%2F%2Fexample.com"
```

Note: the `url` parameter is validated as `HttpUrl`, so it must include a scheme like `http://` or `https://`.

## Postman (quick)

1) `POST http://127.0.0.1:8080/`
   - Body -> raw -> JSON
   - `{ "original_url": "https://example.com" }`

2) `GET http://127.0.0.1:8080/<short_id>`

3) `GET http://127.0.0.1:8080/async-fetch`
   - Params:
     - key: `url`
     - value: `https://example.com`

## Note about SERVER_HOST / SERVER_PORT

In the current `main.py`, `SERVER_HOST` / `SERVER_PORT` are read from `.env`, but they are not used for the actual startup.
The effective host/port are set via `uvicorn` CLI arguments.
