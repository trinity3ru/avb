from fastapi import FastAPI
import uvicorn
from contextlib import asynccontextmanager

import config 
from routes.urls import router as urls_router
from database import engine, Model 

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)
    print("BD is ready") 
    yield
    print ("BD is closed")

app = FastAPI(lifespan=lifespan,
              title="Shorten Url API",
               description="Test API for shortening URLs",
               version="1.0.4")
 
app.include_router(urls_router)  
      
SERVER_HOST = config.SERVER_HOST
SERVER_PORT = config.SERVER_PORT

if __name__ == "__main__":
    uvicorn.run("main:app",host=SERVER_HOST, port=SERVER_PORT)
     

