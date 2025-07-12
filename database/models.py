from sqlalchemy import Column, Integer, String, DateTime
from database.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    password = Column("password_hash", String, nullable=False)
    point = Column(Integer, default=0)

class WasteDetectionLog(Base):
    __tablename__ = "waste_detection_log" 

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, nullable=False)
    waste_type = Column(String, nullable=False)
    qr_code = Column(String, nullable=True)
    username = Column(String, nullable=True)
    point = Column(Integer, default=0)