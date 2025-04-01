from config.db import engine, Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel

class Usuario(Base) :
    __tablename__ = "usuarios"

    id = Column("id", Integer, primary_key =True)
    username = Column("username", String(50), unique=True)
    password = Column("pasword", String(50))

    def __init__(self, id, username, password) :
        self.id = id
        self.username = username
        self.password = password

Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)

session = Session()

class InputUsuario(BaseModel) :
    id: int
    username: str
    password: str