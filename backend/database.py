from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
engine = create_engine("sqlite:///./backend/flights.db")
SessionLocal = sessionmaker(bind=engine)