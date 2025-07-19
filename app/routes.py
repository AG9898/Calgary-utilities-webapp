from flask import current_app, render_template, jsonify
from app.models import Location, db

def index():
    return render_template('landing.html')

def map_view():
    return render_template('index.html')

def geojson():
    """Return all locations as GeoJSON FeatureCollection"""
    try:
        # Query all locations from the database
        locations = Location.query.all()
        
        # Create GeoJSON FeatureCollection
        geojson_data = {
            "type": "FeatureCollection",
            "features": []
        }
        
        # Convert each location to a GeoJSON Feature
        for location in locations:
            # Ensure coordinates are valid numbers
            if location.longitude is None or location.latitude is None:
                continue
            
            # Derive amenity value from category and description
            amenity = "unknown"
            if location.category == 'restaurant':
                amenity = 'restaurant'
            elif location.category == 'utility':
                amenity = 'fuel'
            elif location.category == 'service':
                description_lower = (location.description or "").lower()
                if 'library' in description_lower:
                    amenity = 'library'
                elif 'hospital' in description_lower:
                    amenity = 'hospital'
                else:
                    amenity = 'unknown'
                
            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [float(location.longitude), float(location.latitude)]
                },
                "properties": {
                    "name": location.name or "Unknown Location",
                    "category": location.category or "unknown",
                    "description": location.description or "",
                    "amenity": amenity
                }
            }
            geojson_data["features"].append(feature)
        
        # Add CORS headers to allow fetch requests
        response = jsonify(geojson_data)
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Content-Type', 'application/json')
        
        return response
        
    except Exception as e:
        print(f"Error in geojson route: {str(e)}")
        error_response = jsonify({"error": str(e), "type": "FeatureCollection", "features": []})
        error_response.headers.add('Access-Control-Allow-Origin', '*')
        return error_response, 500 