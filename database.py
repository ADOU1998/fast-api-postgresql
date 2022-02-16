from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Configuration de la bd POSTGRESQL
engine=create_engine("postgresql://postgres:1998fabrice@localhost/fastapi", echo=True)

Base=declarative_base()

SessionLocal=sessionmaker(bind=engine)