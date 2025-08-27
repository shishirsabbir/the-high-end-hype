# imports
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.model import Base


# defining engine
DB_URL = "sqlite:///output/shoeDB.db"
engine = create_engine(DB_URL)

# creating a session using sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# create all tables
Base.metadata.create_all(bind=engine)
