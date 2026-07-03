from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# The connection string to our local PostgreSQL database
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:gilsu123@localhost:5432/fitness_app"

# The core engine that handles the communication with PostgreSQL
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# A factory that creates temporary database sessions for each request
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# The base blueprint for all our SQLAlchemy models (tables)
Base = declarative_base()