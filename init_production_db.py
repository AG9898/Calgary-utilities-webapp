#!/usr/bin/env python3
"""
Script to initialize production database with GeoJSON data.
This script can be run locally to populate the production database on Render.
"""

import requests
import os
import sys

def init_production_db():
    """Initialize production database with GeoJSON data"""
    
    # Get the production URL from environment or user input
    production_url = os.getenv('PRODUCTION_URL')
    if not production_url:
        production_url = input("Enter your production URL (e.g., https://your-app.onrender.com): ").strip()
        if not production_url:
            print("Error: Production URL is required")
            sys.exit(1)
    
    # Get the token from environment or user input
    token = os.getenv('INIT_DATA_TOKEN')
    if not token:
        token = input("Enter your INIT_DATA_TOKEN: ").strip()
        if not token:
            print("Error: INIT_DATA_TOKEN is required")
            sys.exit(1)
    
    # Construct the URL
    init_url = f"{production_url}/init-data?token={token}"
    
    print(f"Initializing database at: {production_url}")
    print("This may take a few minutes depending on the size of your GeoJSON files...")
    
    try:
        # Make the request
        response = requests.get(init_url, timeout=300)  # 5 minute timeout
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Success!")
            print(f"Message: {result.get('message', 'No message')}")
            if 'imported_count' in result:
                print(f"Imported: {result['imported_count']} locations")
            if 'existing_count' in result:
                print(f"Existing: {result['existing_count']} locations")
        elif response.status_code == 401:
            print("❌ Error: Unauthorized")
            print("Check your INIT_DATA_TOKEN environment variable")
        else:
            print(f"❌ Error: HTTP {response.status_code}")
            try:
                error_data = response.json()
                print(f"Error: {error_data.get('error', 'Unknown error')}")
                print(f"Message: {error_data.get('message', 'No message')}")
            except:
                print(f"Response: {response.text}")
                
    except requests.exceptions.Timeout:
        print("❌ Error: Request timed out (5 minutes)")
        print("The GeoJSON files may be very large. Check your Render logs.")
    except requests.exceptions.RequestException as e:
        print(f"❌ Error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == '__main__':
    init_production_db() 