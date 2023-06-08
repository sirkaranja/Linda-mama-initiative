from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from getpass import getpass
from main import Appointment, Doctor, Patient, User
from tabulate import tabulate
from datetime import datetime
from datetime import time

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
#selection to either login as a doctor or patient
    choice = input("Please enter your choice:")

    if choice == "1":
        login_as_doctor()
    elif choice == "2":
        login_as_patient()
#option 3 is to exit the program        
    elif choice == "3":
        print("Goodbye!")
    else:
        print("Invalid choice. Please try again")

#enter details to log in as doctor
def login_as_doctor():
    username = input("Enter your username:")
    password = getpass("Enter your password:")
#validates the inputs from user and compares with the one stored in database
    doctor = session.query(User).filter(User.username == username, User.password == password, User.role == "doctor").first()
    if doctor:
        print(f"Logged in as Doctor: {doctor.username}")
        doctor_menu(doctor)
    else:
        print("Invalid username or password")
        

#after logging in as a doctor
def doctor_menu(doctor):
    print(f"Welcome, Dr. {doctor.username}!")
    print("1. View Patients")
    print("2. View Appointments")
    print("3. Add a Patient")
    print("4. Delete a Patient")
    print("5. Get Report")
    print("6. Update Appointment Status")
    print("7. Logout")
#after logging as doctor there are several options made avaibale to them
    choice = input("Please enter your choice:")

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
        update_appointment_status()
    elif choice == "7":
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
        print(tabulate(patient_data, headers=headers, tablefmt="double_grid"))
    else:
        print("No patients found.")

# Doctor can view the list of appointments with the help of tabulate
def read_appointments():
    appointments = session.query(Appointment).all()
    if appointments:
        appointment_data = [] #initialized an empty list to append details from the db
        for appointment in appointments:
            appointment_data.append([appointment.id, appointment.appointment_date, appointment.appointment_time, appointment.status])
#initialized headers and use tabulate to present the output nicely
        headers = ["Appointment ID", "Date", "Time", "Status"]
        print(tabulate(appointment_data, headers=headers, tablefmt="double_grid"))
    else:
        print("No appointments found.")


#function to add doctors via the command line.
def add_patient():
    #request for user inputs
    name = input("Enter patient's name: ")
    age = input("Enter patient's age: ")
    contact_info = input("Enter patient's contact information: ")
    address = input("Enter patient's address: ")
#create an instance from user inputs and store them in database
    patient = Patient(name=name, age=age, contact_info=contact_info, address=address, appointments=None)
    session.add(patient)
    session.commit()
    print("Patient added successfully.")
    
#function to delete patient record by id
def delete_patient():
    patient_id = input("Enter the patient ID to delete: ")
#first() finds the id and stops from there
    patient = session.query(Patient).filter(Patient.id == patient_id).first()
    if patient:
        session.delete(patient)
        session.commit()
        print("Patient deleted successfully.")
    else:
        print("Patient not found.")

   
#generate report based on the status of the appointment that are scheduled.
def get_report():
#get all appointments that status is schedulled.
    scheduled_appointments = session.query(Appointment).filter(Appointment.status == "Scheduled").all()
    num_appointments = len(scheduled_appointments)

    print("Appointment Report")
    #shows the number of entries with status scheduled
    print(f"Total number of appointments with status 'Scheduled': {num_appointments}")

    if scheduled_appointments:
        appointment_data = []
        for appointment in scheduled_appointments:
            appointment_data.append([appointment.id, appointment.appointment_type, appointment.appointment_date, appointment.appointment_time, appointment.status])
#initialized headers and use tabulate to present the output nicely
        headers = ["Appointment ID", "Type", "Date", "Time", "Status"]
        print(tabulate(appointment_data, headers=headers, tablefmt="double_grid"))
    else:
        print("No appointments found.")

   #update appointment based on status either scheduled or cancelled
def update_appointment_status():
    appointment_id = input("Enter the appointment ID to update: ")
    new_status = input("Enter the new status (Scheduled/Cancelled): ")
#checks for appointments that hace schedule or cancelled as their status
    appointment = session.query(Appointment).filter(Appointment.id == appointment_id).first()
    if appointment:
        if new_status == "Scheduled" or new_status == "Cancelled":
            appointment.status = new_status
            session.commit()
            print("Appointment status updated successfully.")
        else:
            print("Invalid status. Please enter 'Completed' or 'Cancelled'.")
    else:
        print("Appointment not found.")

 #function  to log in as patient
def login_as_patient():
    #request for user inputs
    username = input("Enter your username:")
    password = getpass("Enter your password:")
#validation to check if input matches the one in the database
    patient = session.query(User).filter(User.username == username, User.password == password, User.role == "patient").first()
    #if user exit prints out the login message with their name
    if patient:
        print(f"Logged in as Patient: {patient.username}")
        patient_menu(patient)
    else:
        print("Invalid username or password")
        login_menu()
#user interface for patient once logged in
def patient_menu(patient):
    print(f"Welcome, {patient.username}!")
    print("1. View Details")
    print("2. Book Appointment")
    print("3. View Appointments")
    print("4. Logout")
#patients choose option are limited to 3 
    choice = input("Please enter your choice: ")

    if choice == "1":
        view_details(patient) #views personal details like name
    elif choice == "2":
        book_appointment(patient) #can book an appointment
    elif choice == "3":
        view_appointments(patient) #views the appointment booked 
    elif choice == "4":
        print("Logging out. Goodbye!") #exit the program
    else:
        print("Invalid choice. Please try again")
        patient_menu(patient)

#function to view personal details of the patient like id, name
def view_details(patient):
    print(f"Patient ID: {patient.id}")
    print(f"Username: {patient.username}")
    print(f"Role: {patient.role}")

#fucntion for patient to book an appointment
def book_appointment(patient):
    appointment_type = input("Enter the appointment type (e.g., Postnatal, Prenatal): ")
    appointment_date = input("Enter the appointment date (YYYY-MM-DD): ")
    appointment_time = input("Enter the appointment time (HH:MM AM/PM): ")

    # Convert appointment_date to a Python date object
    appointment_date = datetime.strptime(appointment_date, "%Y-%m-%d").date()

    # Convert appointment_time to a Python time object
    appointment_time = datetime.strptime(appointment_time, "%I:%M %p").time()

    # Get the doctor ID
    doctor_id = input("Enter the doctor ID for the appointment: ")
#creates and instance from the user input and store them in the database by mapping them to respective attributes
    appointment = Appointment(
        appointment_type=appointment_type,
        appointment_date=appointment_date,
        appointment_time=appointment_time,
        patient_id=patient.id,
        doctor_id=doctor_id,
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
        print(tabulate(appointment_data, headers=headers, tablefmt="double_grid"))
    else:
        print("No appointments found.")

    patient_menu(patient)


login_menu()




    



