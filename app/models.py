from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Location(db.Model):
    __tablename__ = 'locations'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # 'restaurant', 'utility', or 'service'
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)
    
    def __repr__(self):
        return f'<Location {self.name} ({self.category})>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'description': self.description
        }

def insert_sample_data(app):
    """Insert sample data into the Location table"""
    with app.app_context():
        # Check if data already exists to avoid duplicates
        if Location.query.first() is not None:
            print("Sample data already exists. Skipping insertion.")
            return
        
        # Sample locations
        sample_locations = [
            Location(
                name="Tim Hortons",
                category="restaurant",
                latitude=51.045,
                longitude=-114.0719,
                description="Coffee and donuts."
            ),
            Location(
                name="Calgary Public Library",
                category="service",
                latitude=51.0453,
                longitude=-114.0581,
                description="Downtown library."
            ),
            Location(
                name="Petro-Canada",
                category="utility",
                latitude=51.046,
                longitude=-114.0730,
                description="Gas station."
            )
        ]
        
        # Insert the sample data
        for location in sample_locations:
            db.session.add(location)
        
        db.session.commit()
        print("Sample data inserted successfully!")
        print(f"Added {len(sample_locations)} locations to the database.")

def import_geojson_files(app):
    """Import locations from GeoJSON files into the database"""
    import json
    import os
    
    # Define file to category mapping
    file_category_mapping = {
        'restaurants.geojson': 'restaurant',
        'gas.geojson': 'utility',
        'library.geojson': 'service',
        'hospital.geojson': 'service'
    }
    
    with app.app_context():
        data_dir = os.path.join(app.root_path, 'data')
        total_imported = 0
        
        for filename, category in file_category_mapping.items():
            file_path = os.path.join(data_dir, filename)
            
            if not os.path.exists(file_path):
                print(f"Warning: File {filename} not found at {file_path}")
                continue
            
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    geojson_data = json.load(file)
                
                imported_count = 0
                
                # Process each feature in the GeoJSON
                for feature in geojson_data.get('features', []):
                    # Check if feature has required properties
                    properties = feature.get('properties', {})
                    name = properties.get('name')
                    
                    # Skip features without a valid name
                    if not name or not name.strip():
                        continue
                    
                    # Get coordinates from geometry
                    geometry = feature.get('geometry', {})
                    if geometry.get('type') != 'Point':
                        continue
                    
                    coordinates = geometry.get('coordinates', [])
                    if len(coordinates) != 2:
                        continue
                    
                    longitude, latitude = coordinates
                    
                    # Validate coordinates
                    if not isinstance(longitude, (int, float)) or not isinstance(latitude, (int, float)):
                        continue
                    
                    # Check if location already exists (by name and coordinates)
                    existing = Location.query.filter_by(
                        name=name,
                        latitude=latitude,
                        longitude=longitude
                    ).first()
                    
                    if existing:
                        continue  # Skip if already exists
                    
                    # Create new location
                    location = Location(
                        name=name,
                        category=category,
                        latitude=latitude,
                        longitude=longitude,
                        description=""  # Empty string as requested
                    )
                    
                    db.session.add(location)
                    imported_count += 1
                
                # Commit the batch for this file
                db.session.commit()
                total_imported += imported_count
                print(f"Imported {imported_count} locations from {filename}")
                
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON in {filename}: {e}")
            except Exception as e:
                print(f"Error processing {filename}: {e}")
                db.session.rollback()
        
        print(f"Total locations imported: {total_imported}")
        return total_imported

def delete_sample_data(app):
    """Delete sample data from the Location table"""
    sample_names = ['Tim Hortons', 'Calgary Public Library', 'Petro-Canada']
    
    with app.app_context():
        deleted_count = 0
        
        for name in sample_names:
            # Find and delete locations with matching names
            locations = Location.query.filter_by(name=name).all()
            for location in locations:
                db.session.delete(location)
                deleted_count += 1
        
        if deleted_count > 0:
            db.session.commit()
            print(f"Deleted {deleted_count} sample locations from the database.")
        else:
            print("No sample data found to delete.")
        
        return deleted_count 