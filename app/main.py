from typing import Literal

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from app.youtube import search_channel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],

    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(request, "index.html")


@app.get("/search")
def search(
    channel: str = Query(default=..., min_length=1, max_length=100),
    min_subs: int = Query(default=0, ge=0),
    max_subs: int = Query(default=999999999999, ge=0),
    sort: Literal[
        "subscribers_desc",
        "subscribers_asc",
        "views_desc",
        "views_asc",
    ] = "subscribers_desc",
    limit: int = Query(default=25, ge=1, le=50),
    country: str | None = Query(default=None, pattern=r"^[A-Za-z]{2}$"),
):
    if min_subs > max_subs:
        raise HTTPException(
            status_code=422,
            detail="min_subs must be less than or equal to max_subs",
        )

    return search_channel(
        channel,
        min_subs,
        max_subs,
        sort,
        limit,
        country
    )
