from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Realm(Base):
    __tablename__ = "realms"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True, nullable=False)  # Realm name
    realm_type = Column(String(50), nullable=False)  # PVP, PVE, RPVE, etc.
    ip_address = Column(String(255), nullable=False)  # Server IP address
    port = Column(Integer, nullable=False)  # Port for the realm server
    is_online = Column(Boolean, default=False)  # Status of the realm
    max_players = Column(Integer, default=1000)  # Max allowed players
    current_players = Column(Integer, default=0)  # Current number of players
    created_at = Column(DateTime, default=datetime.utcnow)  # Creation timestamp
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Last update timestamp

    def __repr__(self):
        return f"<Realm(name='{self.name}', type='{self.realm_type}', online={self.is_online})>"
