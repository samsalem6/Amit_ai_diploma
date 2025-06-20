import json
import random
from model import Patient, Billing, Department, Staff
from model.staff import Doctor, Nurse
from prettytable import PrettyTable
import datetime

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

    def add_patient(self, name, age, condition, phone_number, date_of_birth, gender, email, address, identifier, patient_next_of_kin, room_number=None, insurance=None):
        """
        Add a new patient to the hospital system.
        Args:
            name (str): Name of the patient.
            age (int): Age of the patient.
            condition (str): Medical condition of the patient.
            phone_number (str): Phone number of the patient.
            date_of_birth (str): Date of birth of the patient.
            gender (str): Gender of the patient.
            email (str): Email of the patient.
            address (str): Address of the patient.
            identifier (str): Identifier of the patient.
            patient_next_of_kin (dict): Next of kin of the patient.
            room_number (int, optional): Room number to assign. Defaults to None.
            insurance (dict, optional): Insurance info for the patient.
        Returns:
            Patient or None: The created Patient object, or None if duplicate found.
        """
        # Prevent duplicate by identifier or patient_number
        for p in self.patients:
            if p.identifier == identifier:
                print(f"Patient with identifier '{identifier}' already exists.")
                return None
        patient_number = self.generate_patient_number()
        for p in self.patients:
            if str(p.patient_number) == str(patient_number):
                print(f"Patient number '{patient_number}' already exists.")
                return None
        register_date = datetime.datetime.now().strftime('%Y-%m-%d')
        patient = Patient(name, age, condition, patient_number, phone_number, date_of_birth, gender, email, address, identifier, patient_next_of_kin, room_number=room_number, register_date=register_date, insurance=insurance)
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
        Generate a bill for a patient, applying insurance discount if available.
        Args:
            patient (Patient): The patient to bill.
            amount (float): The amount to bill.
            description (str): Description of the bill.
        """
        insurance_coverage = 0
        if hasattr(patient, 'insurance') and patient.insurance.get('coverage_percent', 0) > 0:
            insurance_coverage = patient.insurance['coverage_percent']
            discounted_amount = Billing(amount, description).get_discounted_amount(insurance_coverage)
            bill = Billing(discounted_amount, f"{description} (after {insurance_coverage}% insurance discount)")
            print(f"Bill generated for {patient.name}: {amount} - {description}\nInsurance applied: {insurance_coverage}%\nAmount after insurance: {discounted_amount}")
        else:
            bill = Billing(amount, description)
            print(f"Bill generated for {patient.name}: {amount} - {description}")
        patient.add_bill(bill)
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

    def add_staff_to_department(self, dept_name, staff_name, staff_age, staff_position, staff_phone_number, staff_date_of_birth, staff_gender, staff_email, staff_address, staff_identifier, specialty=None):
        """
        Add a staff member to a department, creating the department if it does not exist.
        Args:
            dept_name (str): Name of the department.
            staff_name (str): Name of the staff member.
            staff_age (int): Age of the staff member.
            staff_phone_number (str): Phone number of the staff member.
            staff_date_of_birth (str): Date of birth of the staff member.
            staff_gender (str): Gender of the staff member.
            staff_email (str): Email of the staff member.
            staff_address (str): Address of the staff member.
            staff_identifier (str): Identifier of the staff member.
            staff_position (str): Position/job title of the staff member.
            specialty (str, optional): Specialty for doctors.
        """
        if dept_name not in self.departments:
            print(f"Department '{dept_name}' does not exist. Creating it.")
            self.add_department(dept_name)
        if staff_position.lower() == 'doctor':
            doctor = Doctor(staff_name, staff_age, staff_phone_number, staff_date_of_birth, staff_gender, staff_email, staff_address, staff_identifier, specialty or "General")
            self.departments[dept_name].add_doctor(doctor)
        elif staff_position.lower() == 'nurse':
            nurse = Nurse(staff_name, staff_age, staff_phone_number, staff_date_of_birth, staff_gender, staff_email, staff_address, staff_identifier, dept_name)
            self.departments[dept_name].add_nurse(nurse)
        else:
            staff = Staff(staff_name, staff_age, staff_phone_number, staff_date_of_birth, staff_gender, staff_email, staff_address, staff_identifier, staff_position)
            self.departments[dept_name].add_staff(staff)
        self.save_data()

    def assign_patient_to_doctor_in_department(self, dept_name, doctor_name, patient):
        """
        Assign a patient to a doctor in a department.
        Args:
            dept_name (str): Name of the department.
            doctor_name (str): Name of the doctor.
            patient (Patient): Patient object to assign.
        """
        if dept_name in self.departments:
            doctor = next((d for d in self.departments[dept_name].doctors if d.name == doctor_name), None)
            if doctor:
                self.departments[dept_name].assign_patient_to_doctor(patient, doctor)
                self.save_data()
            else:
                print(f"Doctor '{doctor_name}' not found in department '{dept_name}'.")
        else:
            print(f"Department '{dept_name}' does not exist.")

    def view_department_staff(self, dept_name):
        """
        View all staff members in a department, showing doctors and nurses separately.
        Args:
            dept_name (str): Name of the department.
        """
        if dept_name in self.departments:
            dept = self.departments[dept_name]
            if dept.doctors:
                print(f"Doctors in {dept_name}:")
                for d in dept.doctors:
                    print(d.view_info())
            else:
                print(f"No doctors in department '{dept_name}'.")
            if dept.nurses:
                print(f"Nurses in {dept_name}:")
                for n in dept.nurses:
                    print(n.view_info())
            else:
                print(f"No nurses in department '{dept_name}'.")
            other_staff = [s for s in dept.staff if s.position.lower() not in ['doctor', 'nurse']]
            if other_staff:
                print(f"Other staff in {dept_name}:")
                for s in other_staff:
                    print(s.view_info())
        else:
            print(f"Department '{dept_name}' does not exist.")

    def view_doctor_patients(self, dept_name, doctor_name):
        """
        View all patients assigned to a doctor in a department.
        Args:
            dept_name (str): Name of the department.
            doctor_name (str): Name of the doctor.
        """
        if dept_name in self.departments:
            doctor = next((d for d in self.departments[dept_name].doctors if d.name == doctor_name), None)
            if doctor:
                if doctor.patients:
                    print(f"Patients of Dr. {doctor.name}:")
                    for p in doctor.patients:
                        print(f"{p.name} (Number: {p.patient_number})")
                else:
                    print(f"No patients assigned to Dr. {doctor.name}.")
            else:
                print(f"Doctor '{doctor_name}' not found in department '{dept_name}'.")
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
                        {'name': s.name, 'age': s.age, 'position': s.position, 'phone_number': s.phone_number, 'date_of_birth': s.date_of_birth, 'gender': s.gender, 'email': s.email, 'address': s.address, 'identifier': s.identifier }
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
                        staff = Staff(s['name'], s['age'], s['position'], s['phone_number'], s['date_of_birth'], s['gender'], s['email'], s['address'], s['identifier'])
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
        new_phone_number = input(f"New phone number (leave blank to keep '{patient.phone_number}'): ") or patient.phone_number
        new_date_of_birth = input(f"New date of birth (leave blank to keep '{patient.date_of_birth}'): ") or patient.date_of_birth
        new_gender = input(f"New gender (leave blank to keep '{patient.gender}'): ") or patient.gender
        new_email = input(f"New email (leave blank to keep '{patient.email}'): ") or patient.email
        new_address = input(f"New address (leave blank to keep '{patient.address}'): ") or patient.address
        new_identifier = input(f"New identifier (leave blank to keep '{patient.identifier}'): ") or patient.identifier
        new_condition = input(f"New condition (leave blank to keep '{patient.condition}'): ") or patient.condition
        new_status = input(f"New status (normal/surgery/emergency/death, leave blank to keep '{patient.status}'): ") or patient.status
        # Next of kin logic
        has_kin = input("Is there a next of kin? (yes/no, leave blank to keep current): ").strip().lower()
        if has_kin in ['no', 'n']:
            new_patient_next_of_kin = None
        elif has_kin in ['yes', 'y']:
            kin = patient.patient_next_of_kin if isinstance(patient.patient_next_of_kin, dict) else {'name': '', 'number': '', 'email': '', 'relation': ''}
            kin_name = input(f"Next of kin name (leave blank to keep '{kin.get('name','')}'): ") or kin.get('name','')
            kin_number = input(f"Next of kin number (leave blank to keep '{kin.get('number','')}'): ") or kin.get('number','')
            kin_email = input(f"Next of kin email (leave blank to keep '{kin.get('email','')}'): ") or kin.get('email','')
            kin_relation = input(f"Relation to patient (leave blank to keep '{kin.get('relation','')}'): ") or kin.get('relation','')
            new_patient_next_of_kin = {'name': kin_name, 'number': kin_number, 'email': kin_email, 'relation': kin_relation}
        else:
            new_patient_next_of_kin = patient.patient_next_of_kin
        new_date_of_death = patient.date_of_death
        if new_status == 'death':
            new_date_of_death = input(f"Date of death (YYYY-MM-DD, leave blank to keep '{patient.date_of_death}'): ") or patient.date_of_death
        else:
            new_date_of_death = None
        new_register_date = input(f"Register date (YYYY-MM-DD, leave blank to keep '{getattr(patient, 'register_date', None)}'): ") or getattr(patient, 'register_date', None)
        new_discharge_date = input(f"Discharge date (YYYY-MM-DD, leave blank to keep '{getattr(patient, 'discharge_date', None)}'): ") or getattr(patient, 'discharge_date', None)
        # Insurance info
        has_insurance = input("Does the patient have insurance? (yes/no, leave blank to keep current): ").strip().lower()
        if has_insurance in ['no', 'n']:
            new_insurance = {'provider': '', 'policy_number': '', 'coverage_percent': 0}
        elif has_insurance in ['yes', 'y']:
            ins = patient.insurance if isinstance(patient.insurance, dict) else {'provider': '', 'policy_number': '', 'coverage_percent': 0}
            provider = input(f"Insurance provider (leave blank to keep '{ins.get('provider','')}'): ") or ins.get('provider','')
            policy_number = input(f"Policy number (leave blank to keep '{ins.get('policy_number','')}'): ") or ins.get('policy_number','')
            try:
                coverage_percent = float(input(f"Coverage percent (0-100, leave blank to keep '{ins.get('coverage_percent',0)}'): ") or ins.get('coverage_percent',0))
            except ValueError:
                coverage_percent = ins.get('coverage_percent',0)
            new_insurance = {'provider': provider, 'policy_number': policy_number, 'coverage_percent': coverage_percent}
        else:
            new_insurance = patient.insurance
        patient.name = new_name
        patient.age = int(new_age)
        patient.phone_number = new_phone_number
        patient.date_of_birth = new_date_of_birth
        patient.gender = new_gender
        patient.email = new_email
        patient.address = new_address
        patient.identifier = new_identifier
        patient.condition = new_condition
        patient.status = new_status
        patient.patient_next_of_kin = new_patient_next_of_kin
        patient.date_of_death = new_date_of_death
        patient.register_date = new_register_date
        patient.discharge_date = new_discharge_date
        patient.insurance = new_insurance
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
        new_phone_number = input(f"New phone number (leave blank to keep '{staff.phone_number}'): ") or staff.phone_number
        new_date_of_birth = input(f"New date of birth (leave blank to keep '{staff.date_of_birth}'): ") or staff.date_of_birth
        new_gender = input(f"New gender (leave blank to keep '{staff.gender}'): ") or staff.gender
        new_email = input(f"New email (leave blank to keep '{staff.email}'): ") or staff.email
        new_address = input(f"New address (leave blank to keep '{staff.address}'): ") or staff.address
        new_identifier = input(f"New identifier (leave blank to keep '{staff.identifier}'): ") or staff.identifier
        staff.name = new_name
        staff.age = int(new_age)
        staff.position = new_position
        staff.phone_number = new_phone_number
        staff.date_of_birth = new_date_of_birth
        staff.gender = new_gender
        staff.email = new_email
        staff.address = new_address
        staff.identifier = new_identifier
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
            new_status = input(f"Enter new status for {name} (normal/surgery/emergency/death): ")
            if new_status in ['normal', 'surgery', 'emergency', 'death']:
                patient.status = new_status
                if new_status == 'death':
                    patient.date_of_death = input("Enter date of death (YYYY-MM-DD): ")
                else:
                    patient.date_of_death = None
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
            print("21. Assign Patient to Doctor")
            print("22. View Doctor's Patients")
            print("-"*50)
            choice = input("Select option (1-22): ")
            if choice == '1':
                for p in self.patients:
                    details = f"Number: {p.patient_number}, Name: {p.name}, Age: {p.age}, Condition: {p.condition}, Identifier: {p.identifier}, Phone Number: {p.phone_number}, Date of Birth: {p.date_of_birth}, Gender: {p.gender}, Email: {p.email}, Address: {p.address}, Room: {p.room_number}, Bills: {len(p.billing)}, Status: {p.status}"
                    if getattr(p, 'register_date', None):
                        details += f", Register Date: {p.register_date}"
                    if getattr(p, 'discharge_date', None):
                        details += f", Discharge Date: {p.discharge_date}"
                    if isinstance(p.patient_next_of_kin, dict):
                        kin = p.patient_next_of_kin
                        details += f", Next of Kin: {kin.get('name','')} ({kin.get('relation','')}), Number: {kin.get('number','')}, Email: {kin.get('email','')}"
                    if p.status == 'death' and p.date_of_death:
                        details += f", Date of Death: {p.date_of_death}"
                    print(details)
            elif choice == '2':
                for room, name in self.rooms.items():
                    print(f"Room {room}: {name}")
            elif choice == '3':
                name = input("Patient name: ")
                age = int(input("Age: "))
                condition = input("Condition: ")
                phone_number = input("Phone number: ")
                date_of_birth = input("Date of birth: ")
                gender = input("Gender: ")
                email = input("Email: ")
                address = input("Address: ")
                identifier = input("Patient identifier: ")
                room = input("Room number (optional): ")
                room = int(room) if room else None
                # Next of kin logic
                has_kin = input("Is there a next of kin? (yes/no): ").strip().lower()
                if has_kin in ['yes', 'y']:
                    kin_name = input("Next of kin name: ")
                    kin_number = input("Next of kin number: ")
                    kin_email = input("Next of kin email: ")
                    kin_relation = input("Relation to patient: ")
                    patient_next_of_kin = {'name': kin_name, 'number': kin_number, 'email': kin_email, 'relation': kin_relation}
                else:
                    patient_next_of_kin = None
                # Insurance info
                has_insurance = input("Does the patient have insurance? (yes/no): ").strip().lower()
                if has_insurance in ['yes', 'y']:
                    provider = input("Insurance provider: ")
                    policy_number = input("Policy number: ")
                    try:
                        coverage_percent = float(input("Coverage percent (0-100): "))
                    except ValueError:
                        coverage_percent = 0
                    insurance = {'provider': provider, 'policy_number': policy_number, 'coverage_percent': coverage_percent}
                else:
                    insurance = {'provider': '', 'policy_number': '', 'coverage_percent': 0}
                self.add_patient(name, age, condition, phone_number, date_of_birth, gender, email, address, identifier, patient_next_of_kin, room, insurance)
            elif choice == '4':
                identifier = input("Patient name or number to assign room: ")
                room = int(input("Room number: "))
                patient = self.find_patient(identifier)
                if patient:
                    if patient.status == 'death':
                        print("Cannot assign room: patient is deceased.")
                    else:
                        self.assign_room(patient, room)
                else:
                    print("Patient not found.")
            elif choice == '5':
                identifier = input("Patient name or number for billing: ")
                patient = self.find_patient(identifier)
                if patient:
                    if patient.status == 'death':
                        print("Cannot generate bill: patient is deceased.")
                    else:
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
                staff_phone_number = input("Staff phone number: ")
                staff_date_of_birth = input("Staff date of birth: ")
                staff_gender = input("Staff gender: ")
                staff_email = input("Staff email: ")
                staff_address = input("Staff address: ")
                staff_identifier = input("Staff identifier: ")
                specialty = input("Specialty (leave blank for general): ") or None
                self.add_staff_to_department(dept_name, staff_name, staff_age, staff_position, staff_phone_number, staff_date_of_birth, staff_gender, staff_email, staff_address, staff_identifier, specialty)
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
                    elif patient.status == 'death':
                        print("Cannot remove patient: patient is deceased. Record is kept for history.")
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
            elif choice == '21':
                dept_name = input("Department name: ")
                doctor_name = input("Doctor's name: ")
                patient_identifier = input("Patient name or number to assign: ")
                patient = self.find_patient(patient_identifier)
                if patient:
                    self.assign_patient_to_doctor_in_department(dept_name, doctor_name, patient)
                else:
                    print("Patient not found.")
            elif choice == '22':
                dept_name = input("Department name: ")
                doctor_name = input("Doctor's name: ")
                self.view_doctor_patients(dept_name, doctor_name)
            else:
                print("Invalid choice.")
