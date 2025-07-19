#!/usr/bin/env python3
"""
Database initialization script for the Utilities & Services Locator app.
This script creates the PostgreSQL database and all necessary tables.
"""

from app import create_app
from app.models import db, insert_sample_data, import_geojson_files, delete_sample_data

def main():
    """Main function to initialize the database"""
    print("Initializing database for Utilities & Services Locator...")
    
    # Create the Flask app
    app = create_app()
    
    # Create all tables within app context
    with app.app_context():
        db.create_all()
        print("PostgreSQL database initialized successfully!")
        print("Tables created successfully!")
    
    # Delete any existing sample data
    delete_sample_data(app)
    
    # Insert sample data
    insert_sample_data(app)
    
    # Import GeoJSON files
    import_geojson_files(app)
    
    print("Database initialization complete!")

if __name__ == '__main__':
    main() 