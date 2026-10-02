from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .config import get_settings
from .database import init_db
from .routes import auth,pages,planners
@asynccontextmanager
async def lifespan(app):
    init_db();yield
s=get_settings()
app=FastAPI(title=s.app_name,version="1.0.0",lifespan=lifespan)
app.add_middleware(CORSMiddleware,allow_origins=s.cors_origin_list,allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
app.mount("/static",StaticFiles(directory="app/static"),name="static")
app.include_router(pages.router);app.include_router(auth.router);app.include_router(planners.router)
if __name__=="__main__":
    import uvicorn;uvicorn.run("app.main:app",host="127.0.0.1",port=8000,reload=True)
