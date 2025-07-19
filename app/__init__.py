from flask import Flask
from app.models import db

def create_app():
    app = Flask(__name__)
    
    # Configure PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user_AG:Aden9898@localhost:5432/utilities_locator'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize SQLAlchemy with the app (only once)
    db.init_app(app)
    
    # Import and register routes
    from app import routes
    app.add_url_rule('/', 'index', routes.index)
    app.add_url_rule('/map', 'map', routes.map_view)
    app.add_url_rule('/geojson', 'geojson', routes.geojson)
    
    return app 