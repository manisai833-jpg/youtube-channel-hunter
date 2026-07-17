# youtube-channel-hunter

## Project Overview
This project, **youtube-channel-hunter**, is designed to interact with the YouTube Data API. It allows users to manage and retrieve information about YouTube channels using the provided API key.

## Project Structure
```
youtube-channel-hunter
├── app
│   ├── __init__.py
│   ├── config.py
│   └── youtube.py
├── .env
├── .gitignore
├── requirements.txt
├── README.md
└── .venv
```

## Environment Setup

### .env File
The project uses a `.env` file to store sensitive information such as API keys. This file should not be tracked by version control to protect sensitive data.

- **YOUTUBE_API_KEY**: This is the API key required to authenticate requests to the YouTube Data API. Replace `YOUR_API_KEY` in the `.env` file with your actual API key.

### Virtual Environment
A virtual environment is created in the `.venv` directory. This environment contains all the dependencies required for the project, ensuring that the global Python installation remains unaffected.

## Installation Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/manisai833-jpg/youtube-channel-hunter.git
   cd youtube-channel-hunter
   ```

2. **Rename the Virtual Environment**
   If the virtual environment was mistakenly created as `.env`, rename it to `.venv`:
   ```bash
   mv .env .venv
   ```

3. **Create the .env File**
   Create a new `.env` file in the project root:
   ```bash
   touch .env
   ```

4. **Add Your API Key**
   Open the `.env` file and add the following line:
   ```
   YOUTUBE_API_KEY=YOUR_API_KEY
   ```

5. **Install Dependencies**
   Make sure you have `python-dotenv` and `google-api-python-client` in your `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
To run the application, ensure that the virtual environment is activated and the `.env` file is correctly configured with your API key. The application can then be executed to interact with the YouTube Data API.

## Git Ignore
The following files and directories are ignored in the `.gitignore` file to prevent sensitive information and unnecessary files from being tracked:
```
.env
.venv/
__pycache__/
*.pyc
```

## Conclusion
This project provides a structured approach to interacting with the YouTube Data API while ensuring sensitive information is securely managed. Follow the setup instructions carefully to get started.