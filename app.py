from flask import Flask, jsonify, render_template
from scrapers.filmladder_scraper import FilmladderScraper
import os
import json
from datetime import datetime, timedelta

app = Flask(__name__)

CACHE_FILE = 'cache/listings_cache.json'
CACHE_DURATION = timedelta(days=1)  # Cache for 1 day

def get_cached_listings():
    """Get listings from cache if valid, otherwise scrape fresh data"""
    # Create cache directory if it doesn't exist
    os.makedirs('cache', exist_ok=True)
    
    # Check if cache file exists and is recent
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
                cache_time = datetime.fromisoformat(cache_data['cached_at'])
                
                # Check if cache is still valid (less than 1 day old)
                if datetime.now() - cache_time < CACHE_DURATION:
                    print(f"Using cached data from {cache_time}")
                    return cache_data['listings']
                else:
                    print("Cache expired, scraping fresh data...")
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            print(f"Cache file corrupted: {e}")
    
    # Cache is invalid or doesn't exist - scrape fresh data
    print("Scraping fresh data from filmladder.nl...")
    scraper = FilmladderScraper()
    listings = scraper.scrape_all()
    
    # Save to cache
    cache_data = {
        'cached_at': datetime.now().isoformat(),
        'listings': listings
    }
    
    try:
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(cache_data, f, ensure_ascii=False, indent=2)
        print(f"Cached {len(listings)} listings")
    except IOError as e:
        print(f"Failed to write cache: {e}")
    
    return listings

@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')

@app.route('/api/listings')
def get_listings():
    """API endpoint to get all cinema listings"""
    try:
        listings = get_cached_listings()
        
        return jsonify({
            'success': True,
            'data': listings,
            'count': len(listings)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/cinema/<cinema_name>')
def get_cinema_listings(cinema_name):
    """API endpoint to get listings for a specific cinema"""
    try:
        scraper = FilmladderScraper()
        
        if cinema_name == 'lab111':
            listings = scraper.scrape_lab111()
        else:
            return jsonify({
                'success': False,
                'error': 'Cinema not found'
            }), 404
        
        return jsonify({
            'success': True,
            'cinema': cinema_name,
            'data': listings,
            'count': len(listings)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/listings/by-day')
def get_listings_by_day():
    """API endpoint to get listings grouped by day"""
    try:
        listings = get_cached_listings()
        
        # Group showtimes by day
        by_day = {}
        for listing in listings:
            for showtime in listing.get('showtimes', []):
                # Split into day and time
                parts = showtime.split(' ', 1)
                if len(parts) == 2:
                    day, time = parts
                else:
                    day = 'unknown'
                    time = showtime
                
                if day not in by_day:
                    by_day[day] = []
                
                by_day[day].append({
                    'title': listing['title'],
                    'time': time,
                    'rating': listing.get('rating', ''),
                    'cinema': listing['cinema'],
                    'link': listing.get('link', ''),
                    'image': listing.get('image', '')
                })
        
        # Sort movies within each day by time
        for day in by_day:
            by_day[day].sort(key=lambda x: x['time'])
        
        return jsonify({
            'success': True,
            'data': by_day,
            'days': list(by_day.keys())
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=True, host='0.0.0.0', port=port)
