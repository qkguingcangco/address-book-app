from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import logging

logger = logging.getLogger(__name__)

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# Function to initialize the database engine with retries
def create_db_engine(url, retries=3):
    attempt = 0
    while attempt < retries:
        try:
            logger.debug("Creating database engine")
            engine = create_engine(url, connect_args={"check_same_thread": False})
            logger.info("Database engine created successfully")
            return engine
        except Exception as e:
            logger.error("Error creating database engine: %s", str(e))
            attempt += 1
            if attempt < retries:
                logger.warning(f"Retrying to create database engine ({attempt}/{retries})")
    raise Exception("Failed to create database engine after multiple attempts")

try:
    # Initialize db engine
    engine = create_db_engine(SQLALCHEMY_DATABASE_URL)
except Exception as e:
    logger.critical("Failed to initialize database engine: %s", str(e))
    raise

try:
    # Initialize session
    logger.debug("Creating session local")
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    logger.info("Session local created successfully")
except Exception as e:
    logger.critical("Error creating session local: %s", str(e))
    raise

try:
    # Base model class
    logger.debug("Creating base model class")
    Base = declarative_base()
    logger.info("Base model class created successfully")
except Exception as e:
    logger.critical("Error creating base model class: %s", str(e))
    raise