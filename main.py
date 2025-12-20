from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, HttpUrl
import httpx
import uvicorn

from dotenv import load_dotenv
import os

import sqlite3
import string
import random

DB_NAME = "urls.db"
def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS urls (id INTEGER PRIMARY KEY AUTOINCREMENT, short_id TEXT UNIQUE NOT NULL, original_url TEXT NOT NULL)")
    conn.commit()
    conn.close()

def generate_short_id(length: int = 8)->str:
    short_id = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    return short_id

def save_url(original_url: str)->str:
    """Save unique short_id into DB and return short_id"""
    while True:
        short_id = generate_short_id()
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM urls WHERE short_id = ?", (short_id,))
            if cursor.fetchone() is None:
                cursor.execute("INSERT INTO urls (short_id, original_url) VALUES (?, ?)", (short_id, original_url))
                conn.commit()
                 
                return short_id
        finally:
            conn.close()        
 
  

def get_url (short_url: str):
        """Get original url from short_id""" 
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT original_url FROM urls WHERE short_id = ?", (short_url,))
            original_url = cursor.fetchone()
            if original_url is None:
                return None
            else:
                return original_url[0]           
             
        finally:
            conn.close()        
    



load_dotenv()

SERVER_HOST = os.getenv("SERVER_HOST", "127.0.0.1")
SERVER_PORT = int(os.getenv("SERVER_PORT", 8080))

class ShortenRequest(BaseModel):
    original_url: str

app = FastAPI(
    title="Shorten Url API",
    description="Test API for shortening URLs",
    version="1.0.2"
)

 


@app.post("/", status_code=201)
def shorten_url(data: ShortenRequest):
    short_id = save_url(data.original_url)
    return {"short_id":short_id, "original_url":data.original_url}
 
@app.get("/async-fetch")
async def async_fetch(url: HttpUrl = Query(...)):
    """Test endpoint for async fetch
    Make get request to url and return status code and body"""
    async with httpx.AsyncClient(timeout=5.0) as client:
        r = await client.get(str(url))
    return {"status_code": r.status_code, "body": r.text}

@app.get("/{short_url}", status_code=307)
def get_original(short_url:str):
    origin_url = get_url(short_url)
    if origin_url is None:
        raise HTTPException(status_code=404, detail="URL not found")
    else:
        return RedirectResponse(origin_url)
    
    
      
# @app.on_event("startup")
# def on_startup():
if __name__ == "__main__":
    uvicorn.run("main:app",host=SERVER_HOST, port=SERVER_PORT)
     

@app.on_event("startup")
def on_startup():
    init_db()