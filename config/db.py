from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("postgresql://postgres:123456789@localhost:5432/escuela", echo=True)
Base = declarative_base()
