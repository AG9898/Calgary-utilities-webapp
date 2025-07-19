# Utilities & Services Locator

A Flask web application for locating restaurants, utilities, and services on a Leaflet map centered on Calgary, Alberta.

## Features

- **Interactive Leaflet Map**: Centered on Calgary with OpenStreetMap tiles
- **Location Categories**: Restaurants, utilities, and services with color-coded markers
- **Filtering System**: Sidebar filters with SVG icons for each category
- **GeoJSON API**: RESTful endpoint serving location data
- **PostgreSQL Database**: Production-ready with SQLAlchemy ORM
- **Docker Support**: Containerized deployment ready
- **Render Deployment**: Optimized for Render platform

## Project Structure

```
project-root/
│
├── app/
│   ├── static/
│   │   ├── css/
│   │   │   └── main.css
│   │   └── js/
│   │       └── main.js
│   ├── templates/
│   │   ├── landing.html
│   │   └── index.html
│   ├── data/
│   │   ├── restaurants.geojson
│   │   ├── gas.geojson
│   │   ├── library.geojson
│   │   └── hospital.geojson
│   ├── __init__.py
│   ├── routes.py
│   └── models.py
│
├── run.py
├── requirements.txt
├── Dockerfile
├── runtime.txt
└── init_production_db.py
```

## Setup

### Local Development

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up PostgreSQL database (local):
   ```bash
   # Create database and user as needed
   # Update DATABASE_URL in app/__init__.py if different
   ```

3. Run the application:
   ```bash
   python run.py
   ```

4. Open your browser and navigate to `http://localhost:5000`

### Production Deployment (Render)

1. **Environment Variables**: Set these in your Render dashboard:
   - `DATABASE_URL`: Your PostgreSQL connection string
   - `INIT_DATA_TOKEN`: Secret token for database initialization

2. **Deploy**: Connect your GitHub repository to Render

3. **Initialize Database**: After deployment, populate with real data:
   ```bash
   # Option 1: Use the helper script
   python init_production_db.py
   
   # Option 2: Manual HTTP request
   curl "https://your-app.onrender.com/init-data?token=YOUR_SECRET_TOKEN"
   ```

## Database Initialization

### Production Database Setup

The `/init-data` endpoint allows you to populate your production database with the GeoJSON files:

**Security Features:**
- Requires `INIT_DATA_TOKEN` environment variable
- Prevents re-initialization if data already exists
- Comprehensive error handling

**Usage:**
```bash
# Set environment variables
export PRODUCTION_URL="https://your-app.onrender.com"
export INIT_DATA_TOKEN="your_secret_token"

# Run initialization
python init_production_db.py
```

**Manual Initialization:**
```
GET /init-data?token=YOUR_SECRET_TOKEN
```

**Response Examples:**
```json
// Success
{
  "success": true,
  "message": "Successfully imported 1500 locations from GeoJSON files",
  "imported_count": 1500
}

// Already initialized
{
  "message": "Database already contains 1500 locations",
  "warning": "Data already exists. Use token with force=true to reinitialize.",
  "existing_count": 1500
}
```

## API Endpoints

- `GET /`: Landing page
- `GET /map`: Interactive map page
- `GET /geojson`: GeoJSON data for all locations
- `GET /init-data?token=TOKEN`: Initialize database with GeoJSON files

## Map Features

- **Marker Colors**:
  - 🔴 Red: Restaurants
  - 🔵 Blue: Utilities (gas stations)
  - 🟢 Green: Library services
  - 🟣 Purple: Hospital services
  - 🟠 Orange: Other services

- **Filtering**: Click sidebar buttons to show/hide categories
- **Popups**: Click markers for location details
- **Responsive**: Works on desktop and mobile devices

## Development

The application uses:
- **Flask 3.0.0**: Web framework with application factory pattern
- **SQLAlchemy**: Database ORM with PostgreSQL
- **Leaflet.js**: Interactive mapping library
- **Docker**: Containerization for deployment
- **Render**: Cloud deployment platform

## File Descriptions

- `run.py`: Application entry point with database initialization
- `app/__init__.py`: Flask application factory
- `app/routes.py`: Route definitions and API endpoints
- `app/models.py`: Database models and data import functions
- `app/static/js/main.js`: Leaflet map initialization and interaction
- `app/static/css/main.css`: Map and UI styling
- `Dockerfile`: Container configuration for deployment
- `init_production_db.py`: Helper script for production database setup 