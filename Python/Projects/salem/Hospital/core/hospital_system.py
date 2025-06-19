import json
import random
from model import Patient, Billing, Department, Staff
from prettytable import PrettyTable

"""
Main class for managing the hospital system, including patients, rooms, departments, and staff.
Attributes:
    patients (list): List of Patient objects in the hospital.
    rooms (dict): Mapping of room numbers to patient names.
    departments (dict): Mapping of department names to Department objects.
    db_file (str): Path to the database file for saving/loading data.
"""

class HospitalSystem:
    def __init__(self, db_file="hospital_database.json"):
        self.patients = []
        self.rooms = {}
        self.departments = {}
        self.db_file = db_file
        self.load_data()

    def generate_patient_number(self):
        """
        Generate a unique patient number based on existing patients and database records.
        Returns:
            str: The next available patient number as a string.
        """
        numbers = set()
        numbers.update(int(p.patient_number) for p in self.patients if str(p.patient_number).isdigit())
        try:
            with open(self.db_file, "r") as f:
                data = json.load(f)
                for p in data.get('patients', []):
                    num = p.get('patient_number')
                    if num and str(num).isdigit():
                        numbers.add(int(num))
        except Exception:
            pass
        if numbers:
            return str(max(numbers) + 1)
        else:
            return '1001'

    def add_patient(self, name, age, condition, room_number=None):
        """
        Add a new patient to the hospital system.
        Args:
            name (str): Name of the patient.
            age (int): Age of the patient.
            condition (str): Medical condition of the patient.
            room_number (int, optional): Room number to assign. Defaults to None.

        Returns:
            Patient or None: The created Patient object, or None if duplicate found.
        """
        # Prevent duplicate by name or patient_number
        for p in self.patients:
            if p.name == name:
                print(f"Patient with name '{name}' already exists.")
                return None
        patient_number = self.generate_patient_number()
        for p in self.patients:
            if str(p.patient_number) == str(patient_number):
                print(f"Patient number '{patient_number}' already exists.")
                return None
        patient = Patient(name, age, condition, patient_number, room_number=room_number)
        self.patients.append(patient)
        if room_number:
            self.rooms[room_number] = name
        print(f"Patient '{name}' added with number {patient_number}.")
        self.save_data()
        return patient

    def assign_room(self, patient, room_number):
        """
        Assign a room to a patient.
        Args:
            patient (Patient): The patient to assign the room to.
            room_number (int): The room number to assign.
        """
        patient.room_number = room_number
        self.rooms[room_number] = patient.name
        print(f"Assigned room {room_number} to {patient.name}.")
        self.save_data()

    def generate_bill(self, patient, amount, description):
        """
        Generate a bill for a patient.
        Args:
            patient (Patient): The patient to bill.
            amount (float): The amount to bill.
            description (str): Description of the bill.
        """
        bill = Billing(amount, description)
        patient.add_bill(bill)
        print(f"Bill generated for {patient.name}: {amount} - {description}")
        self.save_data()

    def view_bills(self, patient):
        """
        Display all bills for a patient in a table format.
        Args:
            patient (Patient): The patient whose bills to view.
        """
        table = PrettyTable()
        table.field_names = ["Description", "Amount", "Paid"]
        for bill in patient.billing:
            table.add_row([bill.description, bill.amount, "Yes" if bill.paid else "No"])
        print(table)

    def add_department(self, name):
        """
        Add a new department to the hospital.
        Args:
            name (str): Name of the department.
        """
        if name not in self.departments:
            self.departments[name] = Department(name)
            print(f"Department '{name}' added.")
            self.save_data()
        else:
            print(f"Department '{name}' already exists.")

    def add_staff_to_department(self, dept_name, staff_name, staff_age, staff_position):
        """
        Add a staff member to a department, creating the department if it does not exist.
        Args:
            dept_name (str): Name of the department.
            staff_name (str): Name of the staff member.
            staff_age (int): Age of the staff member.
            staff_position (str): Position/job title of the staff member.
        """
        if dept_name not in self.departments:
            print(f"Department '{dept_name}' does not exist. Creating it.")
            self.add_department(dept_name)
        staff = Staff(staff_name, staff_age, staff_position)
        self.departments[dept_name].add_staff(staff)
        self.save_data()

    def view_department_staff(self, dept_name):
        """
        View all staff members in a department.
        Args:
            dept_name (str): Name of the department.
        """
        if dept_name in self.departments:
            staff_list = self.departments[dept_name].staff
            if staff_list:
                for s in staff_list:
                    print(s.view_info())
            else:
                print(f"No staff in department '{dept_name}'.")
        else:
            print(f"Department '{dept_name}' does not exist.")

    def view_rooms(self):
        """
        Get a dictionary of all rooms and their assigned patients.
        Returns:
            dict: Mapping of room numbers to patient names.
        """
        return self.rooms

    def save_data(self):
        """
        Save all hospital data (patients, departments, staff) to the database file.
        """
        data = {
            'patients': [p.to_dict() for p in self.patients],
            'departments': {
                name: {
                    'patients': [getattr(p, 'name', str(p)) for p in dept.patients],
                    'staff': [
                        {'name': s.name, 'age': s.age, 'position': s.position}
                        for s in dept.staff
                    ]
                } for name, dept in self.departments.items()
            }
        }
        with open(self.db_file, "w") as f:
            json.dump(data, f, indent=2)
        print("Data saved.")

    def load_data(self):
        """
        Load hospital data (patients, departments, staff) from the database file.
        """
        try:
            with open(self.db_file, "r") as f:
                data = json.load(f)
                loaded_patients = [Patient.from_dict(p) for p in data.get('patients', [])]
                # Deduplicate by patient_number
                seen = set()
                self.patients = []
                for p in loaded_patients:
                    if p.patient_number not in seen:
                        self.patients.append(p)
                        seen.add(p.patient_number)
                self.rooms = {p.room_number: p.name for p in self.patients if p.room_number}
                self.departments = {}
                for name, dept in data.get('departments', {}).items():
                    department = Department(name)
                    for s in dept.get('staff', []):
                        staff = Staff(s['name'], s['age'], s['position'])
                        department.add_staff(staff)
                    self.departments[name] = department
        except (FileNotFoundError, json.JSONDecodeError):
            self.patients = []
            self.rooms = {}
            self.departments = {}

    def edit_patient(self, patient):
        """
        Edit the details of an existing patient.
        Args:
            patient (Patient): The patient to edit.
        """
        print(f"Editing patient: {patient.name} (Number: {patient.patient_number})")
        new_name = input(f"New name (leave blank to keep '{patient.name}'): ") or patient.name
        new_age = input(f"New age (leave blank to keep '{patient.age}'): ") or patient.age
        new_condition = input(f"New condition (leave blank to keep '{patient.condition}'): ") or patient.condition
        new_status = input(f"New status (normal/surgery/emergency, leave blank to keep '{patient.status}'): ") or patient.status
        patient.name = new_name
        patient.age = int(new_age)
        patient.condition = new_condition
        patient.status = new_status
        print("Patient updated.")
        self.save_data()

    def remove_patient(self, patient):
        if patient in self.patients:
            self.patients.remove(patient)
            print(f"Patient '{patient.name}' (Number: {patient.patient_number}) removed.")
            self.save_data()
        else:
            print("Patient not found.")

    def edit_staff_in_department(self, dept_name, staff_name):
        if dept_name not in self.departments:
            print(f"Department '{dept_name}' does not exist.")
            return
        staff_list = self.departments[dept_name].staff
        staff = next((s for s in staff_list if s.name == staff_name), None)
        if not staff:
            print("Staff not found.")
            return
        print(f"Editing staff: {staff.name}")
        new_name = input(f"New name (leave blank to keep '{staff.name}'): ") or staff.name
        new_age = input(f"New age (leave blank to keep '{staff.age}'): ") or staff.age
        new_position = input(f"New position (leave blank to keep '{staff.position}'): ") or staff.position
        staff.name = new_name
        staff.age = int(new_age)
        staff.position = new_position
        print("Staff updated.")
        self.save_data()

    def remove_staff_from_department(self, dept_name, staff_name):
        if dept_name not in self.departments:
            print(f"Department '{dept_name}' does not exist.")
            return
        staff_list = self.departments[dept_name].staff
        staff = next((s for s in staff_list if s.name == staff_name), None)
        if staff:
            staff_list.remove(staff)
            print(f"Staff '{staff_name}' removed from department '{dept_name}'.")
            self.save_data()
        else:
            print("Staff not found.")

    def update_patient_status(self, name):
        patient = next((p for p in self.patients if p.name == name), None)
        if patient:
            new_status = input(f"Enter new status for {name} (normal/surgery/emergency): ")
            if new_status in ['normal', 'surgery', 'emergency']:
                patient.status = new_status
                print(f"Status updated to {new_status}.")
                self.save_data()
            else:
                print("Invalid status.")
        else:
            print("Patient not found.")

    def mark_bill_paid(self, patient):
        if not patient.billing:
            print("No bills to mark as paid.")
            return
        table = PrettyTable()
        table.field_names = ["Index", "Description", "Amount", "Paid"]
        for idx, bill in enumerate(patient.billing):
            table.add_row([idx, bill.description, bill.amount, "Yes" if bill.paid else "No"])
        print(table)
        try:
            bill_idx = int(input("Enter the index of the bill to mark as paid: "))
            if 0 <= bill_idx < len(patient.billing):
                patient.billing[bill_idx].mark_paid()
                print("Bill marked as paid.")
                self.save_data()
            else:
                print("Invalid index.")
        except ValueError:
            print("Invalid input.")

    def find_patient(self, identifier):
        # identifier can be name or patient_number (as str or int)
        for p in self.patients:
            if p.name == identifier or str(p.patient_number) == str(identifier):
                return p
        return None

    def add_procedure_to_patient(self, patient):
        date = input("Enter procedure date (YYYY-MM-DD): ")
        description = input("Enter procedure description: ")
        patient.add_procedure(date, description)
        print("Procedure added.")
        self.save_data()

    def view_patient_procedures(self, patient):
        procedures = patient.view_procedures()
        if not procedures:
            print("No procedures recorded.")
            return
        table = PrettyTable()
        table.field_names = ["Date", "Description"]
        for proc in procedures:
            table.add_row([proc['date'], proc['description']])
        print(table)

    def generate_bills_from_procedures(self, patient):
        unbilled = [(i, proc) for i, proc in enumerate(patient.procedures) if not proc.get('billed', False)]
        if not unbilled:
            print("No unbilled procedures found.")
            return
        for idx, proc in unbilled:
            print(f"Procedure: {proc['description']} on {proc['date']}")
            try:
                amount = float(input("Enter bill amount for this procedure: "))
            except ValueError:
                print("Invalid amount. Skipping.")
                continue
            desc = f"Procedure: {proc['description']} on {proc['date']}"
            bill = Billing(amount, desc)
            patient.add_bill(bill)
            patient.mark_procedure_billed(idx)
            print("Bill generated and procedure marked as billed.")
        self.save_data()

    def main_menu(self):
        while True:
            print("\n" + "="*50)
            print("Capital Hospital - Patient Management System")
            print("="*50)
            print("1. View Patients")
            print("2. View Rooms")
            print("3. Add Patient")
            print("4. Assign Room")
            print("5. Generate Bill")
            print("6. View Patient Bills")
            print("7. Mark Bill as Paid")
            print("8. Add Department")
            print("9. Add Staff to Department")
            print("10. View Department Staff")
            print("11. Edit Patient")
            print("12. Remove Patient")
            print("13. Edit Staff in Department")
            print("14. Remove Staff from Department")
            print("15. Update Patient Status")
            print("16. Add Procedure to Patient")
            print("17. View Patient Procedures")
            print("18. Generate Bills from Procedures")
            print("19. Save Data")
            print("20. Exit")
            print("-"*50)
            choice = input("Select option (1-20): ")
            if choice == '1':
                for p in self.patients:
                    print(f"Number: {p.patient_number}, Name: {p.name}, Age: {p.age}, Condition: {p.condition}, Room: {p.room_number}, Bills: {len(p.billing)}, Status: {p.status}")
            elif choice == '2':
                for room, name in self.rooms.items():
                    print(f"Room {room}: {name}")
            elif choice == '3':
                name = input("Patient name: ")
                age = int(input("Age: "))
                condition = input("Condition: ")
                room = input("Room number (optional): ")
                room = int(room) if room else None
                self.add_patient(name, age, condition, room)
            elif choice == '4':
                identifier = input("Patient name or number to assign room: ")
                room = int(input("Room number: "))
                patient = self.find_patient(identifier)
                if patient:
                    self.assign_room(patient, room)
                else:
                    print("Patient not found.")
            elif choice == '5':
                identifier = input("Patient name or number for billing: ")
                patient = self.find_patient(identifier)
                if patient:
                    amount = float(input("Bill amount: "))
                    desc = input("Description: ")
                    self.generate_bill(patient, amount, desc)
                else:
                    print("Patient not found.")
            elif choice == '6':
                identifier = input("Patient name or number to view bills: ")
                patient = self.find_patient(identifier)
                if patient:
                    self.view_bills(patient)
                else:
                    print("Patient not found.")
            elif choice == '7':
                identifier = input("Patient name or number to mark bill as paid: ")
                patient = self.find_patient(identifier)
                if patient:
                    self.mark_bill_paid(patient)
                else:
                    print("Patient not found.")
            elif choice == '8':
                dept_name = input("Department name: ")
                self.add_department(dept_name)
            elif choice == '9':
                dept_name = input("Department name: ")
                staff_name = input("Staff name: ")
                staff_age = int(input("Staff age: "))
                staff_position = input("Staff position: ")
                self.add_staff_to_department(dept_name, staff_name, staff_age, staff_position)
            elif choice == '10':
                dept_name = input("Department name: ")
                self.view_department_staff(dept_name)
            elif choice == '11':
                identifier = input("Patient name or number to edit: ")
                patient = self.find_patient(identifier)
                if patient:
                    self.edit_patient(patient)
                else:
                    print("Patient not found.")
            elif choice == '12':
                identifier = input("Patient name or number to remove: ")
                patient = self.find_patient(identifier)
                if patient:
                    if patient.status == 'normal':
                        self.remove_patient(patient)
                    else:
                        print("Patient status is not normal.")
                else:
                    print("Patient not found.")
            elif choice == '13':
                dept_name = input("Department name: ")
                staff_name = input("Staff name to edit: ")
                self.edit_staff_in_department(dept_name, staff_name)
            elif choice == '14':
                dept_name = input("Department name: ")
                staff_name = input("Staff name to remove: ")
                self.remove_staff_from_department(dept_name, staff_name)
            elif choice == '15':
                identifier = input("Patient name or number to update status: ")
                patient = self.find_patient(identifier)
                if patient:
                    self.update_patient_status(patient.name)
                else:
                    print("Patient not found.")
            elif choice == '16':
                identifier = input("Patient name or number to add procedure: ")
                patient = self.find_patient(identifier)
                if patient:
                    self.add_procedure_to_patient(patient)
                else:
                    print("Patient not found.")
            elif choice == '17':
                identifier = input("Patient name or number to view procedures: ")
                patient = self.find_patient(identifier)
                if patient:
                    self.view_patient_procedures(patient)
                else:
                    print("Patient not found.")
            elif choice == '18':
                identifier = input("Patient name or number to generate bills from procedures: ")
                patient = self.find_patient(identifier)
                if patient:
                    self.generate_bills_from_procedures(patient)
                else:
                    print("Patient not found.")
            elif choice == '19':
                self.save_data()
            elif choice == '20':
                save = input("Save data before exit? (y/n): ")
                if save.lower() in ['y', 'yes']:
                    self.save_data()
                print("Goodbye!")
                break
            else:
                print("Invalid choice.")
