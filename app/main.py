from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from app.youtube import search_channel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://youtube-channel-hunter.onrender.com",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(request, "index.html")


@app.get("/search")
def search(
    channel: str,
    min_subs: int = 0,
    max_subs: int = 999999999999,
    sort: str = "subscribers_desc",
    limit: int = 25
):
    return search_channel(
        channel,
        min_subs,
        max_subs,
        sort,
        limit
    )