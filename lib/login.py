from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from getpass import getpass
from main import Appointment, Patient, User
from tabulate import tabulate
from datetime import datetime

# Connect to the database
engine = create_engine('sqlite:///linda_mama_care.db')
Session = sessionmaker(bind=engine)
session = Session()

#user interface when the program runs
def login_menu():
    print("Welcome to Linda Mama Care!")
    print("1. Login as Doctor")
    print("2. Login as Patient")
    print("3. Exit")

    choice = input("Please enter your choice:")

    if choice == "1":
        login_as_doctor()
    elif choice == "2":
        login_as_patient()
    elif choice == "3":
        print("Goodbye!")
    else:
        print("Invalid choice. Please try again")


def login_as_doctor():
    username = input("Enter your username:")
    password = getpass("Enter your password:")

    doctor = session.query(User).filter(User.username == username, User.password == password, User.role == "doctor").first()
    if doctor:
        print(f"Logged in as Doctor: {doctor.username}")
        doctor_menu(doctor)
    else:
        print("Invalid username or password")
        login_menu()

#after logging in as a doctor
def doctor_menu(doctor):
    print(f"Welcome, Dr. {doctor.username}!")
    print("1. View Patients")
    print("2. View Appointments")
    print("3. Add a Patient")
    print("4. Delete a Patient")
    print("5. Get Report")
    print("6. Logout")

    choice = input("Please enter your choice:")
  #displaying the patients details
    if choice == "1":
        read_patients()
    elif choice == "2":
        read_appointments()
    elif choice == "3":
        add_patient()
    elif choice == "4":
        delete_patient()
    elif choice == "5":
        get_report()
    elif choice == "6":
        print("Logging out. Goodbye!")
    else:
        print("Invalid choice. Please try again")
        doctor_menu(doctor)

#doctor will be able to view the list of patients with the help of tabulate
def read_patients():
    patients = session.query(Patient).all()
    if patients:
        patient_data = []
        for patient in patients:
            patient_data.append([patient.id, patient.name, patient.age, patient.contact_info, patient.address])

        headers = ["Patient ID", "Name", "Age", "Contact Info", "Address"]
        print(tabulate(patient_data, headers=headers, tablefmt="fancy_grid"))
    else:
        print("No patients found.")

    


# Doctor can view the list of appointments with the help of tabulate
def read_appointments():
    appointments = session.query(Appointment).all()
    if appointments:
        appointment_data = []
        for appointment in appointments:
            appointment_data.append([appointment.id, appointment.appointment_date, appointment.appointment_time, appointment.status])

        headers = ["Appointment ID", "Date", "Time", "Status"]
        print(tabulate(appointment_data, headers=headers, tablefmt="grid"))
    else:
        print("No appointments found.")



def add_patient():
    name = input("Enter patient's name: ")
    age = input("Enter patient's age: ")
    contact_info = input("Enter patient's contact information: ")
    address = input("Enter patient's address: ")

    patient = Patient(name=name, age=age, contact_info=contact_info, address=address, appointments=None)
    session.add(patient)
    session.commit()
    print("Patient added successfully.")

 
  


def delete_patient():
    patient_id = input("Enter the patient ID to delete: ")

    patient = session.query(Patient).filter(Patient.id == patient_id).first()
    if patient:
        session.delete(patient)
        session.commit()
        print("Patient deleted successfully.")
    else:
        print("Patient not found.")

   

def get_report():
    postnatal_appointments = session.query(Appointment).filter(Appointment.appointment_type == "Postnatal", Appointment.status == "Scheduled").all()
    num_patients = len(postnatal_appointments)

    print("Postnatal Appointment Report")
    print(f"Total number of patients with scheduled postnatal appointments: {num_patients}")

   

def login_as_patient():
    username = input("Enter your username:")
    password = getpass("Enter your password:")

    patient = session.query(User).filter(User.username == username, User.password == password, User.role == "patient").first()
    if patient:
        print(f"Logged in as Patient: {patient.username}")
        patient_menu(patient)
    else:
        print("Invalid username or password")
        login_menu()


def patient_menu(patient):
    print(f"Welcome, {patient.username}!")
    print("1. View Details")
    print("2. Book Appointment")
    print("3. View Appointments")
    print("4. Logout")

    choice = input("Please enter your choice: ")

    if choice == "1":
        view_details(patient)
    elif choice == "2":
        book_appointment(patient)
    elif choice == "3":
        view_appointments(patient)
    elif choice == "4":
        print("Logging out. Goodbye!")
    else:
        print("Invalid choice. Please try again")
        patient_menu(patient)


def view_details(patient):
    print(f"Patient ID: {patient.id}")
    print(f"Username: {patient.username}")
    print(f"Role: {patient.role}")

    




def book_appointment(patient):
    appointment_type = input("Enter the appointment type (e.g., Postnatal, Prenatal): ")
    appointment_date = input("Enter the appointment date (YYYY-MM-DD): ")
    appointment_time = input("Enter the appointment time (HH:MM AM/PM): ")

    # Convert appointment_date to a Python date object
    appointment_date = datetime.strptime(appointment_date, "%Y-%m-%d").date()

    appointment = Appointment(
        appointment_type=appointment_type,
        appointment_date=appointment_date,
        appointment_time=appointment_time,
        patient_id=patient.id,
        doctor_id=None,  # Replace None with the appropriate doctor ID
        status="Scheduled"
    )
    session.add(appointment)
    session.commit()
    print("Appointment booked successfully.")

    patient_menu(patient)



    


def view_appointments(patient):
    appointments = session.query(Appointment).filter(Appointment.patient_id == patient.id).all()
    if appointments:
        appointment_data = []
        for appointment in appointments:
            appointment_data.append([appointment.id, appointment.appointment_type, appointment.appointment_date, appointment.appointment_time, appointment.status])

        headers = ["Appointment ID", "Type", "Date", "Time", "Status"]
        print(tabulate(appointment_data, headers=headers, tablefmt="grid"))
    else:
        print("No appointments found.")

    patient_menu(patient)


login_menu()




    



