from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# Import models so that SQLAlchemy registers them with the metadata
from .models.world_models import Base, Character, Class


def run(config):
    """Generate the World Database schema using SQLAlchemy."""
    try:
        DATABASE_URL = (
            f"mysql+pymysql://{config['user']}:{config['password']}@{config['host']}/world_db"
        )
        engine = create_engine(DATABASE_URL)
        Base.metadata.create_all(engine)
        print("World database and tables created successfully.")
    except Exception as e:
        print(f"Error during World Database generation: {e}")
