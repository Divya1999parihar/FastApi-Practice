
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

db_url= "postgresql://postgres:postgres@localhost:5432/postgres"
engine = create_engine(db_url)
SessionLocal= sessionmaker(autocommit=False, autoflush=False, bind= engine)