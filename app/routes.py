from flask import current_app, render_template, jsonify, request
from app.models import Location, db, import_geojson_files
import os

def index():
    return render_template('landing.html')

def map_view():
    return render_template('index.html')

def init_data():
    """Initialize database with GeoJSON data from /app/data files"""
    try:
        # Check for secret token to prevent abuse
        token = request.args.get('token')
        expected_token = os.getenv('INIT_DATA_TOKEN', 'default_secret_token_change_me')
        
        if not token or token != expected_token:
            return jsonify({
                'error': 'Unauthorized',
                'message': 'Valid token required. Set INIT_DATA_TOKEN environment variable.'
            }), 401
        
        # Check if data already exists to prevent re-initialization
        existing_count = Location.query.count()
        if existing_count > 0:
            return jsonify({
                'message': f'Database already contains {existing_count} locations',
                'warning': 'Data already exists. Use token with force=true to reinitialize.',
                'existing_count': existing_count
            }), 200
        
        # Import GeoJSON files
        total_imported = import_geojson_files(current_app)
        
        if total_imported > 0:
            return jsonify({
                'success': True,
                'message': f'Successfully imported {total_imported} locations from GeoJSON files',
                'imported_count': total_imported
            }), 200
        else:
            return jsonify({
                'warning': 'No new locations imported',
                'message': 'All locations may already exist or files may be empty',
                'imported_count': 0
            }), 200
            
    except Exception as e:
        print(f"Error in init_data route: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500

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