# from sqlalchemy import create_engine, MetaData
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

password = os.getenv("DB_PASSWORT")

DATABASE_URL = f"mysql+pymysql://root:{password}@localhost:3306/Job_Agent"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()

