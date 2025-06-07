from config.db import engine, Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel

# region pydantic
class Usuario(Base) :
    __tablename__ = "usuarios"

    id = Column("id", Integer, primary_key =True)
    username = Column("username", String(50), unique=True)
    password = Column("pasword", String(50))

    def __init__(self, username, password) :
        self.username = username
        self.password = password

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)

session = Session()

class InputUsuario(BaseModel) :
    id: int
    username: str
    password: str

# endregion

# region userdetails

class UserDetail(Base):
   __tablename__ = "userdetails"
   id = Column("id", Integer, primary_key=True)
   dni = Column("dni", Integer)
   firstName = Column("firstName", String)
   lastName = Column("lastName", String)
   type = Column("type", String)
   email = Column("email", String(80), nullable=False, unique=True)

   def __init__(self, dni, firstName, lastName, type, email):
       self.dni = dni
       self.firstName = firstName
       self.lastName = lastName
       self.type = type
       self.email = email

class InputUserDetail(BaseModel):
    dni: int
    firstName: str
    lastName: str
    type: str
    email: str

# endregion   




