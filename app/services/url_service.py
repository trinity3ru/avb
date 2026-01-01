from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

import string
import random

from database import AsyncSession
from models.urls import Url
from schemas import HttpUrl

MAX_ATTEMPTS = 5


def generate_short_id(length: int = 8) -> str:
    short_id = "".join(random.choices(string.ascii_letters + string.digits, k=length))
    return short_id


async def save_url(url: HttpUrl, session: AsyncSession) -> str:
    """Save unique short_id into DB and return short_id"""
    attempts = 0
    while attempts < MAX_ATTEMPTS:
        try:
            short_id = generate_short_id()
            query = select(Url).where(Url.short_id == short_id)
            result = await session.execute(query)
            if result.scalar() is None:
                session.add(Url(short_id=short_id, url=str(url)))
                await session.commit()
                return short_id
        except IntegrityError:
            attempts += 1

    raise RuntimeError("Failed to generate unique short_id")


async def get_url(short_url: str, session: AsyncSession) -> str | None:
    """Get original url from short_id"""
    query = select(Url).where(Url.short_id == short_url)
    result = await session.execute(query)
    url = result.scalar()
    if url is None:
        return None
    else:
        return url.url
