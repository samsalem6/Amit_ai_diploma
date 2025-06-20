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
        self.doctors = []
        self.nurses = []
        self.staff = []  # Optional: keep for backward compatibility
        self.patients = []

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

    def add_doctor(self, doctor):
        self.doctors.append(doctor)
        self.staff.append(doctor)
        print(f"Doctor '{doctor.name}' added to {self.name} department.")

    def add_nurse(self, nurse):
        self.nurses.append(nurse)
        self.staff.append(nurse)
        print(f"Nurse '{nurse.name}' added to {self.name} department.")

    def assign_patient_to_doctor(self, patient, doctor):
        if doctor in self.doctors:
            doctor.add_patient(patient)
            self.patients.append(patient)
            print(f"Patient '{patient.name}' assigned to Doctor '{doctor.name}' in {self.name} department.")
        else:
            print(f"Doctor '{doctor.name}' is not in {self.name} department.")