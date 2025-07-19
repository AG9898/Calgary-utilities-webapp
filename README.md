# Utilities & Services Locator

A Flask web application for locating restaurants, utilities, and services on a Leaflet map.

## Project Structure

```
project-root/
│
├── app/
│   ├── static/
│   │   ├── css/
│   │   └── js/
│   ├── templates/
│   │   └── index.html
│   ├── data/
│   │   └── (will contain locations.db later)
│   ├── __init__.py
│   ├── routes.py
│   └── models.py
│
├── run.py
└── requirements.txt
```

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   python run.py
   ```

3. Open your browser and navigate to `http://localhost:5000`

## Features

- Flask web application with modular structure
- Ready for Leaflet map integration
- Database models prepared for location data
- Static file organization for CSS and JavaScript

## Development

The app is currently showing a "Hello, World!" message on the homepage. Future development will include:

- Leaflet map integration
- Database models for storing location data
- RESTful API endpoints
- Interactive map features 