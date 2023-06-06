import sqlalchemy
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String,VARCHAR, Date, ForeignKey,Time


Base = declarative_base()

#class patient and its attribute
class Patient(Base):
    __tablename__ = 'patients'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age= Column(String)
    gender= Column(String)
    contact_info = Column(VARCHAR)
    address= Column(String)
    appointments = relationship("Appointment", back_populates="patient")

    def __init__(self, id, name, age, gender, contact_info, address, appointments):
        self.name=name
        self.age=age
        self.gender=gender
        self.contact_info=contact_info
        self.address=address
        self.appointments=appointments
    
    


#class appointment and its attribute
class Appointment(Base):
    #appointment table and some of its attribute
    __tablename__ = 'appointments'
    id = Column(Integer, primary_key= True)
    appointment_date= Column(Date)
    appointment_time= Column(Time)
    status= Column(String)
    patient_id= Column(Integer, ForeignKey('patients.id'))
    doctor_id= Column(Integer, ForeignKey('doctors.id'))
    
    patient= relationship("Patient", back_populates="appointments")
    doctor= relationship("Doctor", back_populates="appointments")
    
#class patient and its attribute
class Doctor(Base):
     #Doctor table and some of its attribute
     __tablename__ = 'doctors'
     id= Column(Integer, primary_key=True)
     name= Column(String)
     specialization= Column(String)
     contact_info= Column(String)
     appointments = relationship("Appointment", back_populates="doctor")


# Connect to the database
engine = sqlalchemy.create_engine('sqlite:///linda_mama_care.db')
Session = sessionmaker(bind=engine)
session = Session()
# Create the tables
Base.metadata.create_all(engine)


#generate random data using faker
