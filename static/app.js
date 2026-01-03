let allListings = [];
let allListingsByDay = {};
let currentView = 'day'; // 'movie' or 'day'

// Helper function to create Letterboxd search URL
function getLetterboxdUrl(title) {
    // Clean the title and create a search URL
    const cleanTitle = encodeURIComponent(title.trim());
    return `https://letterboxd.com/search/films/${cleanTitle}/`;
}

// Load listings on page load
document.addEventListener('DOMContentLoaded', () => {
    // Initialize current time filter
    let currentTimeFilter = 'all';
    
    loadListings();
    
    // Add filter listeners for cinema checkboxes
    const cinemaCheckboxes = document.querySelectorAll('input[name="cinema"]');
    const allCinemasCheckbox = document.getElementById('allCinemasCheckbox');
    const parentCheckboxes = document.querySelectorAll('.parent-checkbox input[type="checkbox"]');
    
    // Handle individual cinema checkbox changes
    cinemaCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', () => {
            filterListings();
            updateDropdownLabel();
            updateParentCheckbox(checkbox);
            updateAllCinemasCheckbox();
        });
    });
    
    // Handle parent checkbox changes (West, Centraal, Oost)
    parentCheckboxes.forEach(parentCheckbox => {
        parentCheckbox.addEventListener('change', () => {
            const childValues = parentCheckbox.dataset.children.split(',');
            const isChecked = parentCheckbox.checked;
            
            cinemaCheckboxes.forEach(checkbox => {
                if (childValues.includes(checkbox.value)) {
                    checkbox.checked = isChecked;
                }
            });
            
            filterListings();
            updateDropdownLabel();
            updateAllCinemasCheckbox();
        });
        
        // Initialize parent checkbox state
        updateParentCheckboxState(parentCheckbox);
    });
    
    // Handle All Cinemas checkbox
    allCinemasCheckbox.addEventListener('change', () => {
        const isChecked = allCinemasCheckbox.checked;
        cinemaCheckboxes.forEach(checkbox => {
            checkbox.checked = isChecked;
        });
        parentCheckboxes.forEach(parentCheckbox => {
            updateParentCheckboxState(parentCheckbox);
        });
        filterListings();
        updateDropdownLabel();
    });
    
    // Function to update parent checkbox based on its children
    function updateParentCheckbox(childCheckbox) {
        const parentId = childCheckbox.dataset.parent;
        if (parentId) {
            const parentCheckbox = document.getElementById(parentId);
            updateParentCheckboxState(parentCheckbox);
        }
    }
    
    // Function to update parent checkbox state (checked/unchecked/indeterminate)
    function updateParentCheckboxState(parentCheckbox) {
        const childValues = parentCheckbox.dataset.children.split(',');
        const childCheckboxes = Array.from(cinemaCheckboxes).filter(cb => 
            childValues.includes(cb.value)
        );
        
        const checkedCount = childCheckboxes.filter(cb => cb.checked).length;
        
        if (checkedCount === 0) {
            parentCheckbox.checked = false;
            parentCheckbox.indeterminate = false;
        } else if (checkedCount === childCheckboxes.length) {
            parentCheckbox.checked = true;
            parentCheckbox.indeterminate = false;
        } else {
            parentCheckbox.checked = false;
            parentCheckbox.indeterminate = true;
        }
    }
    
    // Function to update All Cinemas checkbox state based on individual checkboxes
    function updateAllCinemasCheckbox() {
        const allChecked = Array.from(cinemaCheckboxes).every(cb => cb.checked);
        const noneChecked = Array.from(cinemaCheckboxes).every(cb => !cb.checked);
        
        if (allChecked) {
            allCinemasCheckbox.checked = true;
            allCinemasCheckbox.indeterminate = false;
        } else if (noneChecked) {
            allCinemasCheckbox.checked = false;
            allCinemasCheckbox.indeterminate = false;
        } else {
            allCinemasCheckbox.checked = false;
            allCinemasCheckbox.indeterminate = true;
        }
    }
    
    // Cinema dropdown toggle functionality
    const cinemaDropdownToggle = document.getElementById('cinemaDropdownToggle');
    const cinemaDropdownMenu = document.getElementById('cinemaDropdownMenu');
    
    cinemaDropdownToggle.addEventListener('click', (e) => {
        e.stopPropagation();
        cinemaDropdownMenu.classList.toggle('show');
        timeDropdownMenu.classList.remove('show');
    });
    
    // Time filter dropdown toggle functionality
    const timeDropdownToggle = document.getElementById('timeDropdownToggle');
    const timeDropdownMenu = document.getElementById('timeDropdownMenu');
    
    timeDropdownToggle.addEventListener('click', (e) => {
        e.stopPropagation();
        timeDropdownMenu.classList.toggle('show');
        cinemaDropdownMenu.classList.remove('show');
    });
    
    // Time filter option selection
    document.querySelectorAll('.time-option').forEach(option => {
        option.addEventListener('click', () => {
            currentTimeFilter = option.dataset.value;
            document.getElementById('timeDropdownLabel').textContent = option.textContent;
            timeDropdownMenu.classList.remove('show');
            filterListings();
        });
    });
    
    // Close dropdowns when clicking outside
    document.addEventListener('click', (e) => {
        if (!e.target.closest('.cinema-filter-dropdown')) {
            cinemaDropdownMenu.classList.remove('show');
        }
        if (!e.target.closest('.time-filter-dropdown')) {
            timeDropdownMenu.classList.remove('show');
        }
    });
    
    // Prevent cinema dropdown from closing when clicking inside
    cinemaDropdownMenu.addEventListener('click', (e) => {
        e.stopPropagation();
    });
    
    // Initialize label
    updateDropdownLabel();
    
    // Store getter function for time filter
    window.getCurrentTimeFilter = () => currentTimeFilter;
});

function updateDropdownLabel() {
    const selectedCinemas = Array.from(document.querySelectorAll('input[name="cinema"]:checked'))
        .map(cb => cb.value.replace(' Amsterdam', ''));
    const label = document.getElementById('cinemaDropdownLabel');
    
    if (selectedCinemas.length === 0) {
        label.textContent = 'Select Cinemas';
    } else if (selectedCinemas.length === 1) {
        label.textContent = selectedCinemas[0];
    } else {
        label.textContent = `${selectedCinemas.length} Cinemas`;
    }
}

async function loadListings() {
    const loadingEl = document.getElementById('loading');
    const errorEl = document.getElementById('error');
    const listingsEl = document.getElementById('listings');
    
    // Show loading state
    loadingEl.style.display = 'block';
    errorEl.style.display = 'none';
    listingsEl.innerHTML = '';
    
    try {
        // Load both views
        const [movieResponse, dayResponse] = await Promise.all([
            fetch('/api/listings'),
            fetch('/api/listings/by-day')
        ]);
        
        const movieResult = await movieResponse.json();
        const dayResult = await dayResponse.json();
        
        if (movieResult.success && dayResult.success) {
            allListings = movieResult.data;
            allListingsByDay = dayResult.data;
            
            // Apply filters instead of displaying directly
            filterListings();
        } else {
            throw new Error(movieResult.error || dayResult.error || 'Failed to load listings');
        }
    } catch (error) {
        console.error('Error loading listings:', error);
        errorEl.textContent = `Error: ${error.message}`;
        errorEl.style.display = 'block';
    } finally {
        loadingEl.style.display = 'none';
    }
}

function switchView(view) {
    currentView = view;
    
    // Update button states
    document.getElementById('byMovieBtn').classList.toggle('active', view === 'movie');
    document.getElementById('byDayBtn').classList.toggle('active', view === 'day');
    
    // Display the appropriate view with current filters
    filterListings();
}

function displayListingsByDay(byDayData) {
    const listingsEl = document.getElementById('listings');
    listingsEl.className = ''; // Remove grid class
    
    if (Object.keys(byDayData).length === 0) {
        listingsEl.innerHTML = '<div class="empty-state">No listings available at the moment.</div>';
        return;
    }
    
    // Define day order
    const dayOrder = ['vandaag', 'morgen', 'maandag', 'dinsdag', 'woensdag', 'donderdag', 'vrijdag', 'zaterdag', 'zondag'];
    const sortedDays = Object.keys(byDayData).sort((a, b) => {
        const aIndex = dayOrder.indexOf(a);
        const bIndex = dayOrder.indexOf(b);
        if (aIndex === -1 && bIndex === -1) return a.localeCompare(b);
        if (aIndex === -1) return 1;
        if (bIndex === -1) return -1;
        return aIndex - bIndex;
    });
    
    listingsEl.innerHTML = sortedDays.map(day => {
        const movies = byDayData[day];
        
        // Group movies by title and cinema
        const groupedMovies = {};
        movies.forEach(movie => {
            const key = `${movie.title}|||${movie.cinema}`;
            if (!groupedMovies[key]) {
                groupedMovies[key] = {
                    title: movie.title,
                    cinema: movie.cinema,
                    link: movie.link,
                    image: movie.image,
                    times: []
                };
            }
            groupedMovies[key].times.push(movie.time);
        });
        
        // Sort times and create HTML for each grouped movie
        const moviesHTML = Object.values(groupedMovies).map(movie => {
            // Sort times chronologically
            const sortedTimes = movie.times.sort((a, b) => {
                const timeA = extractTime(a) || 0;
                const timeB = extractTime(b) || 0;
                return timeA - timeB;
            });
            
            const firstTime = sortedTimes[0];
            const additionalTimes = sortedTimes.slice(1);
            
            const alsoShowingHTML = additionalTimes.length > 0
                ? `<div class="also-showing">ꕤ Also showing: ${additionalTimes.join(', ')}</div>`
                : '';
            
            const posterHTML = movie.image
                ? `<div class="day-listing-poster"><img src="${movie.image}" alt="${movie.title} poster" onerror="this.parentElement.style.display='none'"></div>`
                : '<div class="day-listing-poster-placeholder"></div>';
            
            return `
                <div class="day-listing-item">
                    ${posterHTML}
                    <div class="day-listing-time">${firstTime}</div>
                    <div class="day-listing-info">
                        <div class="day-listing-title">${movie.title}</div>
                        <div class="day-listing-cinema">${movie.cinema}</div>
                        ${alsoShowingHTML}
                    </div>
                    <div class="day-listing-links">
                        ${movie.link ? `<a href="${movie.link}" target="_blank" rel="noopener noreferrer" class="day-listing-link">Tickets & Times ➭</a>` : ''}
                        <a href="${getLetterboxdUrl(movie.title)}" target="_blank" rel="noopener noreferrer" class="day-listing-link letterboxd-link">Letterboxd ➭</a>
                    </div>
                </div>
            `;
        }).join('');
        
        const isToday = day === 'vandaag';
        const toggleIcon = isToday ? '▼' : '▶';
        const collapsedClass = isToday ? '' : 'collapsed';
        
        return `
            <div class="day-section">
                <h2 class="day-header" onclick="toggleDay(this)">
                    <span class="toggle-icon">${toggleIcon}</span> ${day}
                </h2>
                <div class="day-listings ${collapsedClass}">
                    ${moviesHTML}
                </div>
            </div>
        `;
    }).join('');
}

function toggleDay(header) {
    const listingsDiv = header.nextElementSibling;
    const icon = header.querySelector('.toggle-icon');
    
    listingsDiv.classList.toggle('collapsed');
    
    if (listingsDiv.classList.contains('collapsed')) {
        icon.textContent = '▶';
    } else {
        icon.textContent = '▼';
    }
}

function toggleShowtimes(toggleElement) {
    const showtimesContainer = toggleElement.parentElement;
    const hiddenSpan = showtimesContainer.querySelector('.showtimes-hidden');
    
    if (hiddenSpan.style.display === 'none') {
        hiddenSpan.style.display = 'contents';
        toggleElement.textContent = 'show less';
    } else {
        hiddenSpan.style.display = 'none';
        toggleElement.textContent = 'show more...';
    }
}

function displayListings(listings) {
    const listingsEl = document.getElementById('listings');
    listingsEl.className = 'listings-grid'; // Add grid class back
    
    if (listings.length === 0) {
        listingsEl.innerHTML = '<div class="empty-state">No listings available at the moment.</div>';
        return;
    }
    
    listingsEl.innerHTML = listings.map(listing => createMovieCard(listing)).join('');
}

// Helper function to extract time from showtime string
function extractTime(showtime) {
    // Extract time in format HH:MM from strings like "vandaag 14:30" or "14:30"
    const timeMatch = showtime.match(/(\d{1,2}):(\d{2})/);
    if (timeMatch) {
        const hours = parseInt(timeMatch[1]);
        const minutes = parseInt(timeMatch[2]);
        return hours * 60 + minutes; // Return minutes since midnight
    }
    return null;
}

function matchesTimeFilter(showtime, timeFilter) {
    if (timeFilter === 'all') return true;
    
    const timeMinutes = extractTime(showtime);
    if (timeMinutes === null) return true; // Include if we can't parse the time
    
    switch (timeFilter) {
        case 'morning':
            return timeMinutes < 12 * 60; // Before 12:00
        case 'afternoon':
            return timeMinutes >= 12 * 60 && timeMinutes < 16 * 60; // 12:00 - 15:59
        case 'evening':
            return timeMinutes >= 16 * 60; // 16:00 onwards
        default:
            return true;
    }
}

function filterListings() {
    const selectedCinemas = Array.from(document.querySelectorAll('input[name="cinema"]:checked'))
        .map(cb => cb.value);
    const timeFilter = window.getCurrentTimeFilter ? window.getCurrentTimeFilter() : 'all';
    
    if (currentView === 'movie') {
        // Filter by cinema and time in movie view
        let filtered = allListings.map(listing => {
            // Clone the listing
            let filteredListing = { ...listing };
            
            // Apply time filter to showtimes
            if (timeFilter !== 'all' && listing.showtimes) {
                filteredListing.showtimes = listing.showtimes.filter(showtime => 
                    matchesTimeFilter(showtime, timeFilter)
                );
            }
            
            return filteredListing;
        });
        
        // Remove listings with no showtimes after time filtering
        filtered = filtered.filter(listing => 
            !listing.showtimes || listing.showtimes.length > 0
        );
        
        // Apply cinema filter - only show selected cinemas
        if (selectedCinemas.length > 0) {
            filtered = filtered.filter(listing => selectedCinemas.includes(listing.cinema));
        }
        
        displayListings(filtered);
    } else {
        // Filter by both cinema and time in day view
        let filteredByDay = {};
        
        Object.keys(allListingsByDay).forEach(day => {
            const movies = allListingsByDay[day];
            let filteredMovies = movies;
            
            // Apply cinema filter - only show selected cinemas
            if (selectedCinemas.length > 0) {
                filteredMovies = filteredMovies.filter(movie => selectedCinemas.includes(movie.cinema));
            }
            
            // Apply time filter
            if (timeFilter !== 'all') {
                filteredMovies = filteredMovies.filter(movie => 
                    matchesTimeFilter(movie.time, timeFilter)
                );
            }
            
            if (filteredMovies.length > 0) {
                filteredByDay[day] = filteredMovies;
            }
        });
        
        displayListingsByDay(filteredByDay);
    }
}

function displayListings(listings) {
    const listingsEl = document.getElementById('listings');
    listingsEl.className = 'listings-grid'; // Add grid class
    
    if (listings.length === 0) {
        listingsEl.innerHTML = '<div class="empty-state">No listings available at the moment.</div>';
        return;
    }
    
    // Group movies by title
    const groupedMovies = {};
    listings.forEach(listing => {
        const title = listing.title;
        if (!groupedMovies[title]) {
            groupedMovies[title] = {
                title: listing.title,
                image: listing.image,
                link: listing.link,
                cinemas: []
            };
        }
        groupedMovies[title].cinemas.push({
            name: listing.cinema,
            showtimes: listing.showtimes
        });
    });
    
    // Sort movies alphabetically by title
    const sortedMovies = Object.values(groupedMovies).sort((a, b) => 
        a.title.localeCompare(b.title)
    );
    
    listingsEl.innerHTML = sortedMovies.map(movie => createMovieCard(movie)).join('');
}

function createMovieCard(movie) {
    // Handle grouped movie format (with cinemas array) or legacy single listing format
    const isGrouped = movie.cinemas && Array.isArray(movie.cinemas);
    const isMobile = window.innerWidth <= 768;
    const visibleCount = isMobile ? 3 : 4;
    
    let cinemasHTML = '';
    if (isGrouped) {
        cinemasHTML = movie.cinemas.map((cinema, cinemaIndex) => {
            const allShowtimes = cinema.showtimes || [];
            const hasMany = allShowtimes.length > visibleCount;
            const visibleShowtimes = hasMany ? allShowtimes.slice(0, visibleCount) : allShowtimes;
            const hiddenShowtimes = hasMany ? allShowtimes.slice(visibleCount) : [];
            
            const visibleHTML = visibleShowtimes.map(time => `<span class="showtime">${time}</span>`).join('');
            const hiddenHTML = hiddenShowtimes.map(time => `<span class="showtime">${time}</span>`).join('');
            const showMoreHTML = hasMany ? `<span class="showtime-toggle" onclick="toggleShowtimes(this)">show more...</span>` : '';
            
            return `
                <div class="cinema-section">
                    <div class="cinema-name">${cinema.name}</div>
                    <div class="showtimes">
                        ${visibleHTML}
                        <span class="showtimes-hidden" style="display: none;">${hiddenHTML}</span>
                        ${showMoreHTML}
                    </div>
                </div>
            `;
        }).join('');
    } else {
        // Legacy format for single cinema
        const allShowtimes = movie.showtimes || [];
        const hasMany = allShowtimes.length > visibleCount;
        const visibleShowtimes = hasMany ? allShowtimes.slice(0, visibleCount) : allShowtimes;
        const hiddenShowtimes = hasMany ? allShowtimes.slice(visibleCount) : [];
        
        const visibleHTML = visibleShowtimes.map(time => `<span class="showtime">${time}</span>`).join('');
        const hiddenHTML = hiddenShowtimes.map(time => `<span class="showtime">${time}</span>`).join('');
        const showMoreHTML = hasMany ? `<span class="showtime-toggle" onclick="toggleShowtimes(this)">show more...</span>` : '';
        
        cinemasHTML = `
            <div class="cinema-section">
                <div class="cinema-name">${movie.cinema}</div>
                <div class="showtimes">
                    ${visibleHTML}
                    <span class="showtimes-hidden" style="display: none;">${hiddenHTML}</span>
                    ${showMoreHTML}
                </div>
            </div>
        `;
    }
    
    const posterHTML = movie.image
        ? `<div class="movie-poster-container"><img src="${movie.image}" alt="${movie.title} poster" class="movie-poster" onerror="this.parentElement.style.display='none'"></div>`
        : '';
    
    const linkHTML = movie.link
        ? `<a href="${movie.link}" target="_blank" rel="noopener noreferrer" class="movie-link">Tickets & Times ➭</a>`
        : '';
    
    const letterboxdHTML = `<a href="${getLetterboxdUrl(movie.title)}" target="_blank" rel="noopener noreferrer" class="movie-link letterboxd-link">Letterboxd ➭</a>`;
    
    return `
        <div class="movie-card">
            ${posterHTML}
            <div class="movie-content">
                <div class="movie-header">
                    <h3 class="movie-title">${movie.title}</h3>
                    <div class="movie-links">
                        ${linkHTML}
                        ${letterboxdHTML}
                    </div>
                </div>
                ${cinemasHTML}
            </div>
        </div>
    `;
}
