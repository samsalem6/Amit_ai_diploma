"""
Class representing a department in the hospital.
Attributes:
    name (str): The name of the department.
    patients (list): List of patients in the department.
    staff (list): List of staff members in the department.
"""
class Department:
    def __init__(self, name):
        self.name = name
        self.patients = []
        self.staff = []

    def add_patient(self, patient):
        """
        Add a patient to the department.
        Args:
            patient: The patient object to add.
        """
        self.patients.append(patient)
        print(f"Patient '{patient.name}' added to {self.name} department.")

    def add_staff(self, staff_member):
        """
        Add a staff member to the department.
        Args:
            staff_member: The staff member object to add.
        """
        self.staff.append(staff_member)
        print(f"Staff '{staff_member.name}' added to {self.name} department.")