// Main JavaScript file for the utilities and services locator app

document.addEventListener('DOMContentLoaded', function() {
    let map;
    let locationLayer;
    let allLocations = [];

    // Initialize the Leaflet map
    function initMap() {
        map = L.map('map').setView([51.0447, -114.0719], 12);
        
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(map);
    }

    // Get marker color based on category and amenity
    function getMarkerColor(category, amenity) {
        if (!category) return 'gray';
        
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
                    return 'orange';
                }
            default:
                return 'gray';
        }
    }

    // Create popup content
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
        // Remove existing layer
        if (locationLayer) {
            map.removeLayer(locationLayer);
            locationLayer = null;
        }
        
        // Filter locations based on category
        let filteredLocations;
        if (category === 'all') {
            filteredLocations = allLocations;
            console.log(`Displaying all ${filteredLocations.features.length} locations`);
        } else {
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

    // Fetch and load locations
    function loadLocations() {
        console.log('Fetching locations from /geojson...');
        
        fetch('/geojson')
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                console.log('Received data:', data);
                
                // Validate data structure
                if (!data || !data.features || !Array.isArray(data.features)) {
                    throw new Error('Invalid GeoJSON data structure');
                }
                
                if (data.features.length === 0) {
                    console.log('No locations found in database');
                    allLocations = { type: "FeatureCollection", features: [] };
                    return;
                }
                
                allLocations = data;
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

    // Initialize everything
    initMap();
    initFilterButtons();
    loadLocations();
}); 