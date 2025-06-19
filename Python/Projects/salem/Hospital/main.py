from core.hospital_system import HospitalSystem
from auth.login import Login

def main():
    print("Welcome to the Hospital Management System")
    username = input("Username: ")
    password = input("Password: ")
    login = Login(username, password)
    result = login.login()
    print(result)
    if result.startswith("Login successful"):
        system = HospitalSystem()
        system.main_menu()
    else:
        print("Exiting system.")

if __name__ == "__main__":
    main()