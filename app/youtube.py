from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from fastapi.responses import JSONResponse
from app.config import YOUTUBE_API_KEY
from datetime import datetime, timezone
import re

youtube = build(
    "youtube",
    "v3",
    developerKey=YOUTUBE_API_KEY
)


def search_channel(
    channel_name,
    min_subs=0,
    max_subs=999999999999,
    sort="subscribers_desc",
    limit=100
):
    try:
        results = []
        next_page_token = None

        while len(results) < limit:
            search_request = youtube.search().list(
                q=channel_name,
                type="channel",
                part="snippet",
                maxResults=min(50, limit - len(results)),
                pageToken=next_page_token
            )

            search_response = search_request.execute()

            if not search_response.get("items"):
                break

            for item in search_response["items"]:
                channel_id = item["snippet"]["channelId"]

                channel_request = youtube.channels().list(
                    part="snippet,statistics",
                    id=channel_id
                )

                channel_response = channel_request.execute()

                if not channel_response["items"]:
                    continue

                channel = channel_response["items"][0]

                subscribers = int(
                    channel["statistics"].get("subscriberCount", 0)
                )

                if subscribers < min_subs or subscribers > max_subs:
                    continue

                latest_video_title = None
                latest_video_published_at = None

                latest_video_request = youtube.search().list(
                    part="snippet",
                    channelId=channel_id,
                    order="date",
                    type="video",
                    maxResults=1
                )
                latest_video_response = latest_video_request.execute()

                if latest_video_response.get("items"):
                    latest_video = latest_video_response["items"][0]
                    latest_video_title = latest_video["snippet"]["title"]
                    latest_video_published_at = latest_video["snippet"]["publishedAt"]

                if latest_video_published_at:
                    published_dt = datetime.fromisoformat(
                        latest_video_published_at.replace("Z", "+00:00")
                    )
                    now_utc = datetime.now(timezone.utc)
                    days_since_last_upload = (now_utc - published_dt).days

                    if days_since_last_upload <= 7:
                        activity_status = "Very Active"
                    elif days_since_last_upload <= 30:
                        activity_status = "Active"
                    elif days_since_last_upload <= 90:
                        activity_status = "Slow"
                    else:
                        activity_status = "Inactive"
                else:
                    days_since_last_upload = None
                    activity_status = "Unknown"

                description_text = channel["snippet"]["description"]
                urls = re.findall(r"https?://[^\s,]+", description_text)
                contact_links = {}

                for url in urls:
                    url = url.rstrip(".,;:!?)]\"")
                    url_lower = url.lower()

                    if "instagram.com" in url_lower:
                        contact_links.setdefault("instagram", url)
                    elif "twitter.com" in url_lower or "x.com" in url_lower:
                        contact_links.setdefault("twitter", url)
                    elif "facebook.com" in url_lower or "fb.com" in url_lower:
                        contact_links.setdefault("facebook", url)
                    elif "discord.gg" in url_lower or "discord.com" in url_lower:
                        contact_links.setdefault("discord", url)
                    elif "linktr.ee" in url_lower:
                        contact_links.setdefault("linktree", url)
                    elif "beacons.ai" in url_lower:
                        contact_links.setdefault("beacons", url)
                    else:
                        if "website" not in contact_links:
                            contact_links["website"] = url
                        else:
                            contact_links.setdefault("other", []).append(url)

                if contact_links and "other" not in contact_links:
                    contact_links.setdefault("other", [])

                email_match = re.search(
                    r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
                    description_text
                )
                business_email = email_match.group(0) if email_match else None

                lead_score = 0
                score_breakdown = {}

                if days_since_last_upload is not None:
                    if days_since_last_upload <= 7:
                        lead_score += 30
                        score_breakdown["recent_upload"] = {
                            "points": 30,
                            "reason": f"Uploaded {days_since_last_upload} days ago"
                        }
                    elif days_since_last_upload <= 30:
                        lead_score += 20
                        score_breakdown["recent_upload"] = {
                            "points": 20,
                            "reason": f"Uploaded {days_since_last_upload} days ago"
                        }
                    else:
                        score_breakdown["recent_upload"] = {
                            "points": 0,
                            "reason": f"Last upload {days_since_last_upload} days ago"
                        }
                else:
                    score_breakdown["recent_upload"] = {
                        "points": 0,
                        "reason": "No recent upload found"
                    }

                if contact_links:
                    lead_score += 15
                    score_breakdown["contact_links"] = {
                        "points": 15,
                        "reason": "Contact links found"
                    }
                else:
                    score_breakdown["contact_links"] = {
                        "points": 0,
                        "reason": "No contact links found"
                    }

                if business_email:
                    lead_score += 25
                    score_breakdown["business_email"] = {
                        "points": 25,
                        "reason": "Business email found"
                    }
                else:
                    score_breakdown["business_email"] = {
                        "points": 0,
                        "reason": "No business email found"
                    }

                if min_subs <= subscribers <= max_subs:
                    lead_score += 20
                    score_breakdown["subscriber_match"] = {
                        "points": 20,
                        "reason": "Subscriber count matches the requested range"
                    }
                else:
                    score_breakdown["subscriber_match"] = {
                        "points": 0,
                        "reason": "Subscriber count does not match the requested range"
                    }

                if int(channel["statistics"].get("videoCount", 0)) > 100:
                    lead_score += 10
                    score_breakdown["video_count"] = {
                        "points": 10,
                        "reason": "More than 100 videos"
                    }
                else:
                    score_breakdown["video_count"] = {
                        "points": 0,
                        "reason": "100 or fewer videos"
                    }

                lead_score = min(lead_score, 100)

                if lead_score >= 90:
                    lead_rating = "Excellent"
                    recommendation = "Excellent prospect. Contact this creator."
                elif lead_score >= 75:
                    lead_rating = "Good"
                    recommendation = "Good prospect. Check the About page."
                elif lead_score >= 60:
                    lead_rating = "Average"
                    recommendation = "Average prospect. Contact only if the niche fits."
                elif lead_score >= 40:
                    lead_rating = "Low Priority"
                    recommendation = "Low priority prospect. Consider later."
                else:
                    lead_rating = "Skip"
                    recommendation = "Skip for now. Channel is inactive."

                results.append({
                    "channel_name": channel["snippet"]["title"],
                    "description": channel["snippet"]["description"][:200],
                    "channel_id": channel_id,
                    "channel_url": f"https://www.youtube.com/channel/{channel_id}",
                    "thumbnail": channel["snippet"]["thumbnails"]["high"]["url"],
                    "published_at": channel["snippet"]["publishedAt"],
                    "subscribers": subscribers,
                    "views": int(channel["statistics"].get("viewCount", 0)),
                    "videos": int(channel["statistics"].get("videoCount", 0)),
                    "latest_video_title": latest_video_title,
                    "latest_video_published_at": latest_video_published_at,
                    "days_since_last_upload": days_since_last_upload,
                    "activity_status": activity_status,
                    "contact_links": contact_links,
                    "business_email": business_email,
                    "lead_score": lead_score,
                    "lead_rating": lead_rating,
                    "score_breakdown": score_breakdown,
                    "recommendation": recommendation
                })

            next_page_token = search_response.get("nextPageToken")

            if not next_page_token:
                break

        if not results:
            return {"success": False, "error": "Channel not found"}

        if sort == "subscribers_desc":
            results.sort(key=lambda x: x["subscribers"], reverse=True)
        elif sort == "subscribers_asc":
            results.sort(key=lambda x: x["subscribers"])
        elif sort == "views_desc":
            results.sort(key=lambda x: x["views"], reverse=True)
        elif sort == "views_asc":
            results.sort(key=lambda x: x["views"])

        return {
            "total_results": len(results),
            "returned_results": len(results),
            "channels": results
        }

    except HttpError as e:
        status_code = getattr(e, "status_code", None)

        if status_code == 429:
            return JSONResponse(
                status_code=429,
                content={
                    "success": False,
                    "error": "YouTube API quota exceeded. Please try again later or use another API key."
                }
            )

        if status_code == 403:
            return JSONResponse(
                status_code=403,
                content={
                    "success": False,
                    "error": "Invalid YouTube API key or access forbidden. Please verify your API key."
                }
            )

        return JSONResponse(
            status_code=status_code or 502,
            content={
                "success": False,
                "error": f"YouTube API request failed with status {status_code or 'unknown'}. Please try again later."
            }
        )

    except OSError:
        return JSONResponse(
            status_code=503,
            content={
                "success": False,
                "error": "Network error contacting YouTube API. Please check your connection and try again later."
            }
        )

    except Exception:
        return JSONResponse(
            status_code=503,
            content={
                "success": False,
                "error": "Unexpected error occurred while processing the request. Please try again later."
            }
        )
