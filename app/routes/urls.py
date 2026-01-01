from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import RedirectResponse
from pydantic import HttpUrl
import httpx

from services.url_service import save_url, get_url
from schemas import ShortenRequest

from database import SessionDep

router = APIRouter(prefix="", tags=["url"])


@router.post("/", status_code=201)
async def shorten_url(data: ShortenRequest, session: SessionDep):
    short_id = await save_url(data.url, session)
    return {"short_id": short_id}


@router.get("/async-fetch")
async def async_fetch(url: HttpUrl = Query(...)):
    """Test endpoint for async fetch
    Make get request to url and return status code and body"""
    async with httpx.AsyncClient(timeout=5.0) as client:
        r = await client.get(str(url))
    return {"status_code": r.status_code, "body": r.text}


@router.get("/{short_url}", status_code=307)
async def get_original(short_url: str, session: SessionDep):
    origin_url = await get_url(short_url, session)
    if origin_url is None:
        raise HTTPException(status_code=404, detail="URL not found")
    else:
        return RedirectResponse(origin_url)
