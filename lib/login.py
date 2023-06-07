from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from getpass import getpass
from main import User

#connect to db
engine = create_engine('sqlite:///linda_mama_care.db')
Session = sessionmaker(bind=engine)
session = Session()

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
    username= input("Enter your username:")
    password = getpass("Enter your password:")

    doctor = session.query(User).filter(User.username == username, User.password == password, User.role == "doctor").first()
    if doctor:
        print (f"logged in as Doctor: {doctor}")
    
    else:
        print("invalid username or password")
        login_menu()

def login_as_patient():
    username = input("Enter your username:")
    password = getpass("enter your password:")

    patient = session.query(User).filter(User.username ==username, User.password == password, User.role == "patient").first()
    if patient:
        print(f"Logged in as Patient: {patient}")
    
    else:
        print("Invalid username or password")
        login_menu()

login_menu()