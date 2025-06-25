# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python web scraping application that collects data from two pharmaceutical wholesaler websites (Parmed and Blupax) and uploads the results to Google Drive. The scrapers run concurrently and use a combination of HTTP requests and browser automation.

## Commands

### Running the Application
```bash
python -m src.main
```

### Running Individual Scrapers
```bash
# Run Parmed scraper only
python -m src.scrapers.parmed_scraper

# Run Blupax scraper only  
python -m src.scrapers.blupax_scraper
```

### Installing Dependencies
```bash
pip install -r requirements.txt
```

### Running Tests
```bash
python -m unittest tests/test_main.py
```

### Docker Commands
```bash
# Build image
docker build -t wholesaler-tracking .

# Run container
docker run --env-file .env wholesaler-tracking
```

## Architecture

### Core Components
- **BaseScraper** (`src/scrapers/base.py`): Abstract base class providing common functionality for all scrapers including Google Drive upload
- **ParmedScraper** (`src/scrapers/parmed_scraper.py`): Scrapes Cardinal Health API using browser automation to capture access tokens
- **BlupaxScraper** (`src/scrapers/blupax_scraper.py`): Scrapes Blupax website by extracting JSON from preloaded page data
- **Main orchestrator** (`src/main.py`): Runs both scrapers concurrently using asyncio

### Key Dependencies
- **browser-use**: AI-powered browser automation for Parmed login
- **playwright**: Browser automation engine
- **requests**: HTTP client for API calls
- **google-api-python-client**: Google Drive API integration
- **pandas**: Data processing and CSV generation

### Environment Configuration
The application requires a `.env` file with credentials for:
- Proxy settings (OX_*)
- OpenAI API key for browser automation
- Parmed login credentials  
- Blupax session ID
- Google Drive configuration

### Data Flow
1. Main script initializes both scrapers
2. ParmedScraper uses browser automation to login and capture API access token
3. BlupaxScraper extracts data from page source using regex
4. Both scrapers process data and upload CSV files to Google Drive
5. Results are saved with timestamp-based filenames

### Scraper Pattern
All scrapers inherit from BaseScraper and implement:
- `get_data()`: Async method to fetch raw data
- `_save_to_csv()`: Inherited method for Google Drive upload
- `run()`: Orchestrates data fetching and saving

The scrapers use different data extraction strategies - Parmed requires API authentication while Blupax extracts embedded JSON data from HTML.