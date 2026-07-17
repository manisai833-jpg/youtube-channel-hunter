from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from app.youtube import search_channel

app = FastAPI()

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