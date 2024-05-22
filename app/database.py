from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
# initialize db
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
# initialize session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# base model class
Base = declarative_base()
