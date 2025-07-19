// Main JavaScript file for the utilities and services locator app

let map;
let locationLayer;
let allLocations = [];

// Initialize the Leaflet map
function initMap() {
    // Initialize map centered on Calgary
    map = L.map('map').setView([51.0447, -114.0719], 12);
    
    // Add OpenStreetMap tile layer
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);
}

// Get marker color based on category and amenity
function getMarkerColor(category, amenity) {
    if (!category) return 'gray'; // default fallback
    
    switch(category) {
        case 'restaurant':
            return 'red';
        case 'utility':
            return 'blue';
        case 'service':
            if (amenity === 'library') {
                return 'green';
            } else if (amenity === 'hospital') {
                return 'purple';
            } else {
                return 'orange'; // default for other services
            }
        default:
            return 'gray'; // default fallback
    }
}

// Create popup content safely
function createPopupContent(feature) {
    const properties = feature.properties || {};
    const name = properties.name || 'Unknown Location';
    const category = properties.category || 'Unknown';
    const description = properties.description || 'No description available';
    
    return `
        <div style="min-width: 200px;">
            <h4 style="margin: 0 0 8px 0; color: #333;">${name}</h4>
            <p style="margin: 4px 0; font-weight: bold; color: #666;">
                Category: <span style="color: #333;">${category}</span>
            </p>
            <p style="margin: 4px 0; color: #555;">
                ${description}
            </p>
        </div>
    `;
}

// Create marker layer from GeoJSON data
function createMarkerLayer(locations) {
    return L.geoJSON(locations, {
        pointToLayer: function(feature, latlng) {
            const properties = feature.properties || {};
            const category = properties.category;
            const amenity = properties.amenity;
            const color = getMarkerColor(category, amenity);
            
            return L.circleMarker(latlng, {
                radius: 8,
                fillColor: color,
                color: 'white',
                weight: 2,
                opacity: 1,
                fillOpacity: 0.8
            });
        },
        onEachFeature: function(feature, layer) {
            const popupContent = createPopupContent(feature);
            layer.bindPopup(popupContent);
        }
    });
}

// Filter locations by category
function filterLocations(category) {
    // Always remove existing layer first
    if (locationLayer) {
        map.removeLayer(locationLayer);
        locationLayer = null;
    }
    
    // Filter locations based on category
    let filteredLocations;
    if (category === 'all') {
        // Show all locations
        filteredLocations = allLocations;
        console.log(`Displaying all ${filteredLocations.features.length} locations`);
    } else {
        // Show only locations for the selected category
        filteredLocations = {
            type: "FeatureCollection",
            features: allLocations.features.filter(feature => {
                const properties = feature.properties || {};
                return properties.category === category;
            })
        };
        console.log(`Displaying ${filteredLocations.features.length} ${category} locations`);
    }
    
    // Create and add new layer
    locationLayer = createMarkerLayer(filteredLocations);
    locationLayer.addTo(map);
}

// Initialize filter buttons
function initFilterButtons() {
    const buttons = document.querySelectorAll('.filter-btn');
    
    buttons.forEach(button => {
        button.addEventListener('click', () => {
            // Update active button styling
            buttons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
            
            // Filter locations
            const category = button.getAttribute('data-category');
            filterLocations(category);
        });
    });
}

// Fetch and display locations
function loadLocations() {
    console.log('Fetching locations from /geojson...');
    
    fetch('/geojson', {
        method: 'GET',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        console.log('Response status:', response.status);
        console.log('Response headers:', response.headers);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log('Received data:', data);
        
        // Validate data structure
        if (!data) {
            throw new Error('No data received');
        }
        
        if (!data.features) {
            throw new Error('Missing features array in GeoJSON');
        }
        
        if (!Array.isArray(data.features)) {
            throw new Error('Features is not an array');
        }
        
        // Check if we have any features
        if (data.features.length === 0) {
            console.log('No locations found in database');
            allLocations = { type: "FeatureCollection", features: [] };
            return;
        }
        
        allLocations = data;
        
        // Don't display markers initially - wait for user to click a filter button
        console.log(`Loaded ${data.features.length} locations (not displayed until filter is selected)`);
    })
    .catch(error => {
        console.error('Error loading locations:', error);
        
        // Display error message on the map
        L.popup()
            .setLatLng([51.0447, -114.0719])
            .setContent(`
                <div style="color: red; text-align: center;">
                    <h4>Error Loading Data</h4>
                    <p>Error: ${error.message}</p>
                    <p>Please check the console for more details.</p>
                </div>
            `)
            .openOn(map);
    });
}

// Initialize everything when the page loads
document.addEventListener('DOMContentLoaded', function() {
    // Initialize the map
    initMap();
    
    // Initialize filter buttons
    initFilterButtons();
    
    // Load locations
    loadLocations();
}); 