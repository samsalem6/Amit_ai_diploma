from core.hospital_system import HospitalSystem
from auth.login import Login

def main():
    print("Welcome to the Hospital Management System")
    while True:
        username = input("Username: ")
        password = input("Password: ")
        login = Login(username, password)
        result = login.login()
        print(result)
        if result.startswith("Login successful"):
            break
        else:
            print("Invalid username or password. Please try again.\n")
    system = HospitalSystem()
    system.main_menu()

if __name__ == "__main__":
    main()