from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sqlalchemy.orm

engine = create_engine('sqlite:///local.db', echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class ModDate(Base):
    __tablename__ = 'modifications'
    control_number = Column(Integer, primary_key=True)
    date_modified = Column(String)


Base.metadata.create_all(engine)
