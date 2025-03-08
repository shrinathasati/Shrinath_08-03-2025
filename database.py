from sqlalchemy import create_engine, Column, String, Integer, Time, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database setup
DATABASE_URL = "sqlite:///./store_monitoring.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database models
class StoreStatus(Base):
    __tablename__ = "store_status"
    store_id = Column(String, primary_key=True)
    timestamp_utc = Column(TIMESTAMP, primary_key=True)
    status = Column(String)

class BusinessHours(Base):
    __tablename__ = "business_hours"
    store_id = Column(String, primary_key=True)
    dayOfWeek = Column(Integer, primary_key=True)
    start_time_local = Column(Time)
    end_time_local = Column(Time)

class StoreTimezone(Base):
    __tablename__ = "store_timezone"
    store_id = Column(String, primary_key=True)
    timezone_str = Column(String)

# Create tables
Base.metadata.create_all(bind=engine)