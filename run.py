from app import create_app
from app.models import db
import os

app = create_app()

def init_database():
    """Initialize database tables and schema"""
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")
        
        # Only insert sample data in development (not production)
        if not os.getenv('DATABASE_URL'):
            print("Development environment detected - skipping sample data insertion")
            print("Use /init-data endpoint with token to populate production database")
        else:
            print("Production environment detected - database ready for /init-data endpoint")

if __name__ == '__main__':
    # Initialize database before running the app
    init_database()
    app.run(host="0.0.0.0", port=5000) 