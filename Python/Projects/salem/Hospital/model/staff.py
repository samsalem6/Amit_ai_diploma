from .person import Person

"""
Class for hospital staff, inheriting from Person.
Attributes:
    name (str): The name of the staff member.
    age (int): The age of the staff member.
    position (str): The position/job title of the staff member.
"""
class Staff(Person):
    def __init__(self, name, age, phone_number, date_of_birth, gender, email, address, identifier, position):
        super().__init__(name, age, phone_number, date_of_birth, gender, email, address, identifier)
        self.position = position

    def view_info(self):
        """
        View staff information.
        Returns:
            str: String with the staff member's name, age, and position and other information.
        """
        return f"Staff Name: {self.name}, Age: {self.age}, Position: {self.position}, Phone Number: {self.phone_number}, Date of Birth: {self.date_of_birth}, Gender: {self.gender}, Email: {self.email}, Address: {self.address}, Identifier: {self.identifier}"

class Doctor(Staff):
    def __init__(self, name, age, phone_number, date_of_birth, gender, email, address, identifier, specialty):
        super().__init__(name, age, phone_number, date_of_birth, gender, email, address, identifier, position='Doctor')
        self.specialty = specialty
        self.patients = []

    def add_patient(self, patient):
        self.patients.append(patient)
        print(f"Patient '{patient.name}' assigned to Doctor {self.name}.")

    def view_patients(self):
        return self.patients

class Nurse(Staff):
    def __init__(self, name, age, phone_number, date_of_birth, gender, email, address, identifier, department=None):
        super().__init__(name, age, phone_number, date_of_birth, gender, email, address, identifier, position='Nurse')
        self.department = department