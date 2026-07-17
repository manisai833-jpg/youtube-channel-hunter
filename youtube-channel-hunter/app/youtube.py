from googleapiclient.discovery import build
from app.config import YOUTUBE_API_KEY
from dotenv import load_dotenv
import os

load_dotenv()

youtube = build(
    "youtube",
    "v3",
    developerKey=YOUTUBE_API_KEY
)