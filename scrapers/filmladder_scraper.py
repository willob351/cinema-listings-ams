import requests
from bs4 import BeautifulSoup
from datetime import datetime

class FilmladderScraper:
    """Scraper for filmladder.nl cinema listings"""
    
    BASE_URL = 'https://www.filmladder.nl'
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
    
    def scrape_lab111(self):
        """Scrape LAB111 Amsterdam cinema listings"""
        url = f'{self.BASE_URL}/bioscoop/lab111-amsterdam'
        
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            listings = []
            
            # First, build a map of movie titles to their poster images
            poster_map = {}
            all_image_links = soup.find_all('a')
            for link in all_image_links:
                img = link.find('img')
                if img and img.get('src'):
                    # Get the alt text which might contain the movie title
                    alt_text = img.get('alt', '')
                    if alt_text and 'poster' in alt_text.lower():
                        # Extract title from alt text like "Alphaville - poster"
                        title_from_alt = alt_text.replace(' - poster', '').replace('- poster', '').strip()
                        poster_map[title_from_alt.lower()] = img['src']
            
            # Find all h4 elements (movie titles)
            h4_tags = soup.find_all('h4')
            
            for h4 in h4_tags:
                try:
                    # Get all links in the h4
                    links = h4.find_all('a')
                    if len(links) < 2:
                        continue
                    
                    # First link is the title
                    title_link = links[0]
                    title = title_link.get_text(strip=True)
                    link = title_link.get('href', '')
                    
                    # Second link is the rating
                    rating = links[1].get_text(strip=True)
                    
                    # Find poster image from the poster map
                    image_url = poster_map.get(title.lower(), '')
                    
                    # Extract showtimes with days from the next sibling (week-frame div)
                    showtimes = []
                    week_frame = h4.find_next_sibling('div', class_='week-frame')
                    if week_frame:
                        # Find all day divs
                        days = week_frame.find_all('div', class_='day')
                        for day_div in days:
                            # Get the day name
                            day_name_full = day_div.find('span', class_='name full')
                            day_name_short = day_div.find('span', class_='name short')
                            
                            day_label = ''
                            if day_name_full:
                                day_label = day_name_full.get_text(strip=True)
                            elif day_name_short:
                                day_label = day_name_short.get_text(strip=True)
                            
                            # Get showtimes for this day
                            time_links = day_div.find_all('a', href=lambda x: x and 'kaartjes' in x)
                            for time_link in time_links:
                                time_text = time_link.get_text(strip=True)
                                if time_text:
                                    # Combine day and time
                                    if day_label:
                                        showtime = f"{day_label} {time_text}"
                                    else:
                                        showtime = time_text
                                    showtimes.append(showtime)
                    
                    # Only add if we have at least a title
                    if title:
                        listing = {
                            'title': title,
                            'cinema': 'LAB111',
                            'rating': rating,
                            'showtimes': showtimes,
                            'image': image_url,
                            'link': 'https://www.filmladder.nl/bioscoop/lab111-amsterdam',
                            'scraped_at': datetime.now().isoformat()
                        }
                        listings.append(listing)
                
                except Exception as e:
                    print(f"Error parsing movie: {e}")
                    continue
            
            return listings
            
        except requests.RequestException as e:
            print(f"Error fetching LAB111 listings: {e}")
            return []
    
    def scrape_filmhallen(self):
        """Scrape Filmhallen Amsterdam cinema listings"""
        url = f'{self.BASE_URL}/bioscoop/filmhallen-amsterdam'
        
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            listings = []
            
            # First, build a map of movie titles to their poster images
            poster_map = {}
            all_image_links = soup.find_all('a')
            for link in all_image_links:
                img = link.find('img')
                if img and img.get('src'):
                    # Get the alt text which might contain the movie title
                    alt_text = img.get('alt', '')
                    if alt_text and 'poster' in alt_text.lower():
                        # Extract title from alt text like "Alphaville - poster"
                        title_from_alt = alt_text.replace(' - poster', '').replace('- poster', '').strip()
                        poster_map[title_from_alt.lower()] = img['src']
            
            # Find all h4 elements (movie titles)
            h4_tags = soup.find_all('h4')
            
            for h4 in h4_tags:
                try:
                    # Get all links in the h4
                    links = h4.find_all('a')
                    if len(links) < 2:
                        continue
                    
                    # First link is the title
                    title_link = links[0]
                    title = title_link.get_text(strip=True)
                    link = title_link.get('href', '')
                    
                    # Second link is the rating
                    rating = links[1].get_text(strip=True)
                    
                    # Extract showtimes with days from the next sibling (week-frame div)
                    showtimes = []
                    week_frame = h4.find_next_sibling('div', class_='week-frame')
                    if week_frame:
                        # Find all day divs
                        days = week_frame.find_all('div', class_='day')
                        for day_div in days:
                            # Get the day name
                            day_name_full = day_div.find('span', class_='name full')
                            day_name_short = day_div.find('span', class_='name short')
                            
                            day_label = ''
                            if day_name_full:
                                day_label = day_name_full.get_text(strip=True)
                            elif day_name_short:
                                day_label = day_name_short.get_text(strip=True)
                            
                            # Get showtimes for this day
                            time_links = day_div.find_all('a', href=lambda x: x and 'kaartjes' in x)
                            for time_link in time_links:
                                time_text = time_link.get_text(strip=True)
                                if time_text:
                                    # Combine day and time
                                    if day_label:
                                        showtime = f"{day_label} {time_text}"
                                    else:
                                        showtime = time_text
                                    showtimes.append(showtime)
                    
                    # Only add if we have at least a title
                    if title:
                        listing = {
                            'title': title,
                            'cinema': 'Filmhallen',
                            'rating': rating,
                            'showtimes': showtimes,
                            'image': poster_map.get(title.lower(), ''),
                            'link': 'https://www.filmladder.nl/bioscoop/filmhallen-amsterdam',
                            'scraped_at': datetime.now().isoformat()
                        }
                        listings.append(listing)
                
                except Exception as e:
                    print(f"Error parsing movie: {e}")
                    continue
            
            return listings
            
        except requests.RequestException as e:
            print(f"Error fetching Filmhallen listings: {e}")
            return []
    
    def scrape_tuschinski(self):
        """Scrape Pathé Tuschinski Amsterdam cinema listings"""
        url = f'{self.BASE_URL}/bioscoop/pathe-tuschinski-amsterdam'
        
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            listings = []
            
            # First, build a map of movie titles to their poster images
            poster_map = {}
            all_image_links = soup.find_all('a')
            for link in all_image_links:
                img = link.find('img')
                if img and img.get('src'):
                    # Get the alt text which might contain the movie title
                    alt_text = img.get('alt', '')
                    if alt_text and 'poster' in alt_text.lower():
                        # Extract title from alt text like "Alphaville - poster"
                        title_from_alt = alt_text.replace(' - poster', '').replace('- poster', '').strip()
                        poster_map[title_from_alt.lower()] = img['src']
            
            # Find all h4 elements (movie titles)
            h4_tags = soup.find_all('h4')
            
            for h4 in h4_tags:
                try:
                    # Get all links in the h4
                    links = h4.find_all('a')
                    if len(links) < 2:
                        continue
                    
                    # First link is the title
                    title_link = links[0]
                    title = title_link.get_text(strip=True)
                    link = title_link.get('href', '')
                    
                    # Second link is the rating
                    rating = links[1].get_text(strip=True)
                    
                    # Extract showtimes with days from the next sibling (week-frame div)
                    showtimes = []
                    week_frame = h4.find_next_sibling('div', class_='week-frame')
                    if week_frame:
                        # Find all day divs
                        days = week_frame.find_all('div', class_='day')
                        for day_div in days:
                            # Get the day name
                            day_name_full = day_div.find('span', class_='name full')
                            day_name_short = day_div.find('span', class_='name short')
                            
                            day_label = ''
                            if day_name_full:
                                day_label = day_name_full.get_text(strip=True)
                            elif day_name_short:
                                day_label = day_name_short.get_text(strip=True)
                            
                            # Get showtimes for this day
                            time_links = day_div.find_all('a', href=lambda x: x and 'kaartjes' in x)
                            for time_link in time_links:
                                time_text = time_link.get_text(strip=True)
                                if time_text:
                                    # Combine day and time
                                    if day_label:
                                        showtime = f"{day_label} {time_text}"
                                    else:
                                        showtime = time_text
                                    showtimes.append(showtime)
                    
                    # Only add if we have at least a title
                    if title:
                        listing = {
                            'title': title,
                            'cinema': 'Pathé Tuschinski',
                            'rating': rating,
                            'showtimes': showtimes,
                            'image': poster_map.get(title.lower(), ''),
                            'link': 'https://www.filmladder.nl/bioscoop/pathe-tuschinski-amsterdam',
                            'scraped_at': datetime.now().isoformat()
                        }
                        listings.append(listing)
                
                except Exception as e:
                    print(f"Error parsing movie: {e}")
                    continue
            
            return listings
            
        except requests.RequestException as e:
            print(f"Error fetching Tuschinski listings: {e}")
            return []
    
    def scrape_kriterion(self):
        """Scrape Kriterion Amsterdam cinema listings"""
        url = f'{self.BASE_URL}/bioscoop/kriterion-amsterdam'
        
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            listings = []
            
            # First, build a map of movie titles to their poster images
            poster_map = {}
            all_image_links = soup.find_all('a')
            for link in all_image_links:
                img = link.find('img')
                if img and img.get('src'):
                    # Get the alt text which might contain the movie title
                    alt_text = img.get('alt', '')
                    if alt_text and 'poster' in alt_text.lower():
                        # Extract title from alt text like "Alphaville - poster"
                        title_from_alt = alt_text.replace(' - poster', '').replace('- poster', '').strip()
                        poster_map[title_from_alt.lower()] = img['src']
            
            # Find all h4 elements (movie titles)
            h4_tags = soup.find_all('h4')
            
            for h4 in h4_tags:
                try:
                    # Get all links in the h4
                    links = h4.find_all('a')
                    if len(links) < 2:
                        continue
                    
                    # First link is the title
                    title_link = links[0]
                    title = title_link.get_text(strip=True)
                    link = title_link.get('href', '')
                    
                    # Second link is the rating
                    rating = links[1].get_text(strip=True)
                    
                    # Extract showtimes with days from the next sibling (week-frame div)
                    showtimes = []
                    week_frame = h4.find_next_sibling('div', class_='week-frame')
                    if week_frame:
                        # Find all day divs
                        days = week_frame.find_all('div', class_='day')
                        for day_div in days:
                            # Get the day name
                            day_name_full = day_div.find('span', class_='name full')
                            day_name_short = day_div.find('span', class_='name short')
                            
                            day_label = ''
                            if day_name_full:
                                day_label = day_name_full.get_text(strip=True)
                            elif day_name_short:
                                day_label = day_name_short.get_text(strip=True)
                            
                            # Get showtimes for this day
                            time_links = day_div.find_all('a', href=lambda x: x and 'kaartjes' in x)
                            for time_link in time_links:
                                time_text = time_link.get_text(strip=True)
                                if time_text:
                                    # Combine day and time
                                    if day_label:
                                        showtime = f"{day_label} {time_text}"
                                    else:
                                        showtime = time_text
                                    showtimes.append(showtime)
                    
                    # Only add if we have at least a title
                    if title:
                        listing = {
                            'title': title,
                            'cinema': 'Kriterion',
                            'rating': rating,
                            'showtimes': showtimes,
                            'image': poster_map.get(title.lower(), ''),
                            'link': 'https://www.filmladder.nl/bioscoop/kriterion-amsterdam',
                            'scraped_at': datetime.now().isoformat()
                        }
                        listings.append(listing)
                
                except Exception as e:
                    print(f"Error parsing movie: {e}")
                    continue
            
            return listings
            
        except requests.RequestException as e:
            print(f"Error fetching Kriterion listings: {e}")
            return []
    
    def scrape_de_uitkijk(self):
        """Scrape De Uitkijk Amsterdam cinema listings"""
        url = f'{self.BASE_URL}/bioscoop/de-uitkijk-amsterdam'
        
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            listings = []
            
            # First, build a map of movie titles to their poster images
            poster_map = {}
            all_image_links = soup.find_all('a')
            for link in all_image_links:
                img = link.find('img')
                if img and img.get('src'):
                    # Get the alt text which might contain the movie title
                    alt_text = img.get('alt', '')
                    if alt_text and 'poster' in alt_text.lower():
                        # Extract title from alt text like "Alphaville - poster"
                        title_from_alt = alt_text.replace(' - poster', '').replace('- poster', '').strip()
                        poster_map[title_from_alt.lower()] = img['src']
            
            # Find all h4 elements (movie titles)
            h4_tags = soup.find_all('h4')
            
            for h4 in h4_tags:
                try:
                    # Get all links in the h4
                    links = h4.find_all('a')
                    if len(links) < 2:
                        continue
                    
                    # First link is the title
                    title_link = links[0]
                    title = title_link.get_text(strip=True)
                    link = title_link.get('href', '')
                    
                    # Second link is the rating
                    rating = links[1].get_text(strip=True)
                    
                    # Extract showtimes with days from the next sibling (week-frame div)
                    showtimes = []
                    week_frame = h4.find_next_sibling('div', class_='week-frame')
                    if week_frame:
                        # Find all day divs
                        days = week_frame.find_all('div', class_='day')
                        for day_div in days:
                            # Get the day name
                            day_name_full = day_div.find('span', class_='name full')
                            day_name_short = day_div.find('span', class_='name short')
                            
                            day_label = ''
                            if day_name_full:
                                day_label = day_name_full.get_text(strip=True)
                            elif day_name_short:
                                day_label = day_name_short.get_text(strip=True)
                            
                            # Get showtimes for this day
                            time_links = day_div.find_all('a', href=lambda x: x and 'kaartjes' in x)
                            for time_link in time_links:
                                time_text = time_link.get_text(strip=True)
                                if time_text:
                                    # Combine day and time
                                    if day_label:
                                        showtime = f"{day_label} {time_text}"
                                    else:
                                        showtime = time_text
                                    showtimes.append(showtime)
                    
                    # Only add if we have at least a title
                    if title:
                        listing = {
                            'title': title,
                            'cinema': 'De Uitkijk',
                            'rating': rating,
                            'showtimes': showtimes,
                            'image': poster_map.get(title.lower(), ''),
                            'link': 'https://www.filmladder.nl/bioscoop/de-uitkijk-amsterdam',
                            'scraped_at': datetime.now().isoformat()
                        }
                        listings.append(listing)
                
                except Exception as e:
                    print(f"Error parsing movie: {e}")
                    continue
            
            return listings
            
        except requests.RequestException as e:
            print(f"Error fetching De Uitkijk listings: {e}")
            return []
    
    def scrape_studio_k(self):
        """Scrape Studio K Amsterdam cinema listings"""
        url = f'{self.BASE_URL}/bioscoop/studio-k-amsterdam'
        
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            listings = []
            
            # First, build a map of movie titles to their poster images
            poster_map = {}
            all_image_links = soup.find_all('a')
            for link in all_image_links:
                img = link.find('img')
                if img and img.get('src'):
                    # Get the alt text which might contain the movie title
                    alt_text = img.get('alt', '')
                    if alt_text and 'poster' in alt_text.lower():
                        # Extract title from alt text like "Alphaville - poster"
                        title_from_alt = alt_text.replace(' - poster', '').replace('- poster', '').strip()
                        poster_map[title_from_alt.lower()] = img['src']
            
            # Find all h4 elements (movie titles)
            h4_tags = soup.find_all('h4')
            
            for h4 in h4_tags:
                try:
                    # Get all links in the h4
                    links = h4.find_all('a')
                    if len(links) < 2:
                        continue
                    
                    # First link is the title
                    title_link = links[0]
                    title = title_link.get_text(strip=True)
                    link = title_link.get('href', '')
                    
                    # Second link is the rating
                    rating = links[1].get_text(strip=True)
                    
                    # Extract showtimes with days from the next sibling (week-frame div)
                    showtimes = []
                    week_frame = h4.find_next_sibling('div', class_='week-frame')
                    if week_frame:
                        # Find all day divs
                        days = week_frame.find_all('div', class_='day')
                        for day_div in days:
                            # Get the day name
                            day_name_full = day_div.find('span', class_='name full')
                            day_name_short = day_div.find('span', class_='name short')
                            
                            day_label = ''
                            if day_name_full:
                                day_label = day_name_full.get_text(strip=True)
                            elif day_name_short:
                                day_label = day_name_short.get_text(strip=True)
                            
                            # Get showtimes for this day
                            time_links = day_div.find_all('a', href=lambda x: x and 'kaartjes' in x)
                            for time_link in time_links:
                                time_text = time_link.get_text(strip=True)
                                if time_text:
                                    # Combine day and time
                                    if day_label:
                                        showtime = f"{day_label} {time_text}"
                                    else:
                                        showtime = time_text
                                    showtimes.append(showtime)
                    
                    # Only add if we have at least a title
                    if title:
                        listing = {
                            'title': title,
                            'cinema': 'Studio K',
                            'rating': rating,
                            'showtimes': showtimes,
                            'image': poster_map.get(title.lower(), ''),
                            'link': 'https://www.filmladder.nl/bioscoop/studio-k-amsterdam',
                            'scraped_at': datetime.now().isoformat()
                        }
                        listings.append(listing)
                
                except Exception as e:
                    print(f"Error parsing movie: {e}")
                    continue
            
            return listings
            
        except requests.RequestException as e:
            print(f"Error fetching Studio K listings: {e}")
            return []
    
    def scrape_eye(self):
        """Scrape EYE Amsterdam cinema listings"""
        url = f'{self.BASE_URL}/bioscoop/eye-amsterdam'
        
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            listings = []
            
            # First, build a map of movie titles to their poster images
            poster_map = {}
            all_image_links = soup.find_all('a')
            for link in all_image_links:
                img = link.find('img')
                if img and img.get('src'):
                    # Get the alt text which might contain the movie title
                    alt_text = img.get('alt', '')
                    if alt_text and 'poster' in alt_text.lower():
                        # Extract title from alt text like "Alphaville - poster"
                        title_from_alt = alt_text.replace(' - poster', '').replace('- poster', '').strip()
                        poster_map[title_from_alt.lower()] = img['src']
            
            # Find all h4 elements (movie titles)
            h4_tags = soup.find_all('h4')
            
            for h4 in h4_tags:
                try:
                    # Get all links in the h4
                    links = h4.find_all('a')
                    if len(links) < 2:
                        continue
                    
                    # First link is the title
                    title_link = links[0]
                    title = title_link.get_text(strip=True)
                    link = title_link.get('href', '')
                    
                    # Second link is the rating
                    rating = links[1].get_text(strip=True)
                    
                    # Extract showtimes with days from the next sibling (week-frame div)
                    showtimes = []
                    week_frame = h4.find_next_sibling('div', class_='week-frame')
                    if week_frame:
                        # Find all day divs
                        days = week_frame.find_all('div', class_='day')
                        for day_div in days:
                            # Get the day name
                            day_name_full = day_div.find('span', class_='name full')
                            day_name_short = day_div.find('span', class_='name short')
                            
                            day_label = ''
                            if day_name_full:
                                day_label = day_name_full.get_text(strip=True)
                            elif day_name_short:
                                day_label = day_name_short.get_text(strip=True)
                            
                            # Get showtimes for this day
                            time_links = day_div.find_all('a', href=lambda x: x and 'kaartjes' in x)
                            for time_link in time_links:
                                time_text = time_link.get_text(strip=True)
                                if time_text:
                                    # Combine day and time
                                    if day_label:
                                        showtime = f"{day_label} {time_text}"
                                    else:
                                        showtime = time_text
                                    showtimes.append(showtime)
                    
                    # Only add if we have at least a title
                    if title:
                        listing = {
                            'title': title,
                            'cinema': 'EYE',
                            'rating': rating,
                            'showtimes': showtimes,
                            'image': poster_map.get(title.lower(), ''),
                            'link': 'https://www.filmladder.nl/bioscoop/eye-amsterdam',
                            'scraped_at': datetime.now().isoformat()
                        }
                        listings.append(listing)
                
                except Exception as e:
                    print(f"Error parsing movie: {e}")
                    continue
            
            return listings
            
        except requests.RequestException as e:
            print(f"Error fetching EYE listings: {e}")
            return []
    
    def scrape_fc_hyena(self):
        """Scrape FC Hyena Amsterdam cinema listings"""
        url = f'{self.BASE_URL}/bioscoop/fc-hyena-amsterdam'
        
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            listings = []
            
            # First, build a map of movie titles to their poster images
            poster_map = {}
            all_image_links = soup.find_all('a')
            for link in all_image_links:
                img = link.find('img')
                if img and img.get('src'):
                    # Get the alt text which might contain the movie title
                    alt_text = img.get('alt', '')
                    if alt_text and 'poster' in alt_text.lower():
                        # Extract title from alt text like "Alphaville - poster"
                        title_from_alt = alt_text.replace(' - poster', '').replace('- poster', '').strip()
                        poster_map[title_from_alt.lower()] = img['src']
            
            # Find all h4 elements (movie titles)
            h4_tags = soup.find_all('h4')
            
            for h4 in h4_tags:
                try:
                    # Get all links in the h4
                    links = h4.find_all('a')
                    if len(links) < 2:
                        continue
                    
                    # First link is the title
                    title_link = links[0]
                    title = title_link.get_text(strip=True)
                    link = title_link.get('href', '')
                    
                    # Second link is the rating
                    rating = links[1].get_text(strip=True)
                    
                    # Extract showtimes with days from the next sibling (week-frame div)
                    showtimes = []
                    week_frame = h4.find_next_sibling('div', class_='week-frame')
                    if week_frame:
                        # Find all day divs
                        days = week_frame.find_all('div', class_='day')
                        for day_div in days:
                            # Get the day name
                            day_name_full = day_div.find('span', class_='name full')
                            day_name_short = day_div.find('span', class_='name short')
                            
                            day_label = ''
                            if day_name_full:
                                day_label = day_name_full.get_text(strip=True)
                            elif day_name_short:
                                day_label = day_name_short.get_text(strip=True)
                            
                            # Get showtimes for this day
                            time_links = day_div.find_all('a', href=lambda x: x and 'kaartjes' in x)
                            for time_link in time_links:
                                time_text = time_link.get_text(strip=True)
                                if time_text:
                                    # Combine day and time
                                    if day_label:
                                        showtime = f"{day_label} {time_text}"
                                    else:
                                        showtime = time_text
                                    showtimes.append(showtime)
                    
                    # Only add if we have at least a title
                    if title:
                        listing = {
                            'title': title,
                            'cinema': 'FC Hyena',
                            'rating': rating,
                            'showtimes': showtimes,
                            'image': poster_map.get(title.lower(), ''),
                            'link': 'https://www.filmladder.nl/bioscoop/fc-hyena-amsterdam',
                            'scraped_at': datetime.now().isoformat()
                        }
                        listings.append(listing)
                
                except Exception as e:
                    print(f"Error parsing movie: {e}")
                    continue
            
            return listings
            
        except requests.RequestException as e:
            print(f"Error fetching FC Hyena listings: {e}")
            return []
    
    def scrape_all(self):
        """Scrape all supported cinemas"""
        all_listings = []
        all_listings.extend(self.scrape_lab111())
        all_listings.extend(self.scrape_filmhallen())
        all_listings.extend(self.scrape_tuschinski())
        all_listings.extend(self.scrape_kriterion())
        all_listings.extend(self.scrape_de_uitkijk())
        all_listings.extend(self.scrape_studio_k())
        all_listings.extend(self.scrape_eye())
        all_listings.extend(self.scrape_fc_hyena())
        return all_listings
