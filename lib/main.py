import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey

Base = declarative_base()

class Patient(Base):
    __tablename__ = 'patients'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    # appointment type
    #vacination type



class Appointment(Base):
    __tablename__ = 'appointments'
    id = Column(Integer, primary_key= True)
    # patient_id
    #vaccine type
    #date


# Connect to the database
engine = sqlalchemy.create_engine('sqlite:///linda_mama_care.db')
Session = sessionmaker(bind=engine)
session = Session()
# Create the tables
Base.metadata.create_all(engine)