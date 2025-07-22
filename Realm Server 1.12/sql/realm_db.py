from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models.realm_models import Base  # Import models from realm_models

def run(config):
    """
    Generate the Realm Database schema using SQLAlchemy.

    Args:
        config (dict): MySQL connection configuration.
    """
    try:
        # Build the database URL
        DATABASE_URL = f"mysql+pymysql://{config['user']}:{config['password']}@{config['host']}/realm_db"

        # Create the engine
        engine = create_engine(DATABASE_URL)

        # Create the database schema
        Base.metadata.create_all(engine)
        print("Realm database and tables created successfully.")

    except Exception as e:
        print(f"Error during Realm Database generation: {e}")
