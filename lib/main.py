import sqlalchemy
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String,VARCHAR, Date, ForeignKey,Time
from faker import Faker
import random


Base = declarative_base()

#class patient and its attribute
class Patient(Base):
    __tablename__ = 'patients'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age= Column(String)
    contact_info = Column(VARCHAR)
    address= Column(String)
    appointments = relationship("Appointment", back_populates="patient")

    def __init__(self, id, name, age, contact_info, address, appointments):
        self.name=name
        self.age=age
        self.contact_info=contact_info
        self.address=address
        self.appointments=appointments

    def __rep__(self):
        return f"{self.name}"

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

    def __init__(self, id, appointment_date, appointment_time, status, patient_id, doctor_id):
        self.appointment_date=appointment_date
        self.appointment_time=appointment_time
        self.status=status
        self.patient_id= patient_id
        self.doctor_id=doctor_id
    
#class patient and its attribute
class Doctor(Base):
     #Doctor table and some of its attribute
     __tablename__ = 'doctors'
     id= Column(Integer, primary_key=True)
     name= Column(String)
     specialization= Column(String)
     contact_info= Column(String)
     appointments = relationship("Appointment", back_populates="doctor")

     def __init__(self, id, name, specialization, contact_info, appointments):
         self.name=name
         self.specialization=specialization
         self.contact_info=contact_info
         self.appointments=appointments

# Connect to the database
engine = sqlalchemy.create_engine('sqlite:///linda_mama_care.db')
Session = sessionmaker(bind=engine)
session = Session()
# Create the tables
Base.metadata.create_all(engine)


#generate random data using faker to populate the appointments
fake = Faker()

patient1 = Patient(
    id=1,
    name=fake.name(),
    age=str(random.randint(18, 65)),
    contact_info=fake.phone_number(),
    address=fake.address(),
    appointments=[]
)


session.add(patient1)
session.commit()

#generate random data
# patient1= Patient(1,'Ann doe',25,'07987373','Kibera','postnatal')

# session.add(patient1)
# session.commit()




