# Cinema Listings Aggregator

A Python Flask web application that aggregates cinema listings from multiple websites and displays them in a unified interface.

## Features

- Scrapes movie listings from filmladder.nl (LAB111 Amsterdam)
- Clean, modern web interface
- Real-time data fetching
- Filter by cinema
- Responsive design

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Start the Flask server:
```bash
python app.py
```

2. Open your browser and navigate to:
```
http://localhost:5000
```

## Project Structure

```
cinemaApp/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── scrapers/
│   ├── __init__.py
│   └── filmladder_scraper.py  # Filmladder.nl scraper
├── templates/
│   └── index.html             # Main HTML template
└── static/
    ├── style.css              # CSS styles
    └── app.js                 # Frontend JavaScript
```

## API Endpoints

- `GET /` - Main web interface
- `GET /api/listings` - Get all cinema listings (JSON)
- `GET /api/cinema/<cinema_name>` - Get listings for specific cinema

## Adding New Cinemas

To add a new cinema source:

1. Create a new scraper method in `scrapers/filmladder_scraper.py` or create a new scraper file
2. Add the scraper call to the API endpoints in `app.py`
3. Update the cinema filter in `templates/index.html`

## Legal Notice

This application scrapes publicly available data. Please respect the terms of service of the websites being scraped and implement appropriate rate limiting.
