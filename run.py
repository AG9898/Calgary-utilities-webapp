from app import create_app
from app.models import db

app = create_app()

def init_database():
    """Initialize database tables and schema"""
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")

if __name__ == '__main__':
    # Initialize database before running the app
    init_database()
    app.run(host="0.0.0.0", port=5000) 