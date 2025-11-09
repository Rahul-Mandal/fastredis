from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Base = declarative_base()


DATABASE_URL = 'postgresql://postgres:root@localhost:5432/test1'

engine = create_engine(DATABASE_URL, pool_size =10, max_overflow = 20, pool_timeout = 30,pool_recycle = 1800)

SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

Base = declarative_base()

# //dependency

def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()