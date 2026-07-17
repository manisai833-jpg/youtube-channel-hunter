# YouTube Channel Hunter

YouTube Channel Hunter is a FastAPI-powered web application that helps users discover active YouTube creators and identify potential clients using filters, lead scoring, and contact information.

## Features

- Search YouTube channels by keyword
- Filter by minimum and maximum subscribers
- Sort by subscribers, views, newest, and oldest
- Detect recently active creators
- Extract public contact links
- Detect public business email (when available)
- Generate direct YouTube channel links
- Lead Score (0–100)
- Lead Rating (Excellent, Good, Average, Skip)
- Score Breakdown
- AI-friendly JSON API
- Modern responsive web interface
- Graceful error handling for API quota and invalid API keys

## Screenshots

Coming Soon

## Tech Stack

- Python 3
- FastAPI
- Jinja2
- HTML
- CSS
- JavaScript
- YouTube Data API v3

## Installation

1. Clone the repository

```bash
git clone https://github.com/manisai833-jpg/youtube-channel-hunter.git
cd youtube-channel-hunter
```

2. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install requirements

```bash
pip install -r requirements.txt
```

4. Create a `.env` file

```bash
touch .env
```

5. Add your API key to `.env`

```env
YOUTUBE_API_KEY=YOUR_API_KEY
```

6. Run the app

```bash
uvicorn app.main:app --reload
```

7. Open the app in your browser

```text
http://127.0.0.1:8000
```

## API Example

GET `/search?channel=gaming&min_subs=10000&max_subs=500000&limit=5`

## Example Response

```json
{
  "total_results": 5,
  "returned_results": 5,
  "channels": [
    {
      "channel_name": "Gaming Channel Name",
      "subscribers": 120000,
      "lead_score": 82,
      "lead_rating": "Good",
      "channel_url": "https://www.youtube.com/channel/UC123456789"
    }
  ]
}
```

## Error Handling

The API returns friendly JSON messages when external failures occur, instead of crashing.

- API quota exceeded
- Invalid API key
- Network failure

Example error response:

```json
{
  "success": false,
  "error": "YouTube API quota exceeded. Please try again later or use another API key."
}
```

## Project Structure

- `app/` – FastAPI application code and API routes
- `templates/` – Jinja2 frontend templates
- `models.py` – data models and helpers
- `youtube.py` – YouTube API search and enrichment logic
- `config.py` – configuration and API key settings
- `main.py` – FastAPI app initialization and routes

## Future Roadmap

- CSV Export
- Excel Export
- AI Lead Ranking
- Email Verification
- Advanced Filters
- Multi-platform Creator Search
- AI Agent Integration

## License

MIT License
