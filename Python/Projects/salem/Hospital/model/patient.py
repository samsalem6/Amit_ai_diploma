from .person import Person
from .billing import Billing

"""
Represents a patient in the hospital.
Attributes:
    name (str): The name of the patient.
    age (int): The age of the patient.
    condition (str): The medical condition of the patient.
    patient_number (str/int): Unique identifier for the patient.
    room_number (str/int, optional): The room number assigned to the patient.
    procedures (list): List of procedures for the patient, each with a 'billed' flag.
    billing (list): List of Billing objects associated with the patient.
    status (str): The current status of the patient.
"""

class Patient(Person):
    def __init__(self, name, age, condition, patient_number, room_number=None, procedures=None, billing=None, status='normal'):
        super().__init__(name, age)
        self.condition = condition
        self.patient_number = patient_number
        self.room_number = room_number
        # Ensure all procedures have a 'billed' flag
        if procedures is not None:
            self.procedures = [
                {**proc, 'billed': proc.get('billed', False)} for proc in procedures
            ]
        else:
            self.procedures = []
        self.billing = billing if billing is not None else []
        self.status = status

    def add_bill(self, bill):
        """
        Add a billing record to the patient.
        Args:
            bill (Billing): The billing record to add.
        """
        self.billing.append(bill)

    def add_procedure(self, date, description):
        """
        Add a medical procedure to the patient.
        Args:
            date (str): The date of the procedure.
            description (str): Description of the procedure.
        """
        self.procedures.append({'date': date, 'description': description, 'billed': False})

    def mark_procedure_billed(self, index):
        """
        Mark a procedure as billed by its index.
        Args:
            index (int): The index of the procedure to mark as billed.
        """
        if 0 <= index < len(self.procedures):
            self.procedures[index]['billed'] = True

    def view_procedures(self):
        """
        View all procedures for the patient.
        Returns:
            list: List of procedures.
        """
        return self.procedures

    def update_status(self, new_status):
        """
        Update the status of the patient.
        Args:
            new_status (str): The new status to set.
        """
        self.status = new_status

    def to_dict(self):
        """
        Convert the Patient object to a dictionary.
        Returns:
            dict: A dictionary representation of the patient.
        """
        return {
            'name': self.name,
            'age': self.age,
            'condition': self.condition,
            'patient_number': self.patient_number,
            'room_number': self.room_number,
            'procedures': self.procedures,
            'billing': [b.to_dict() for b in self.billing],
            'status': self.status
        }

    @staticmethod
    def from_dict(data):
        """
        Create a Patient object from a dictionary.
        Args:
            data (dict): A dictionary with patient data.
        Returns:
            Patient: A Patient object created from the dictionary data.
        """
        billing = [Billing.from_dict(b) for b in data.get('billing', [])]
        return Patient(
            data['name'],
            data['age'],
            data['condition'],
            data['patient_number'],
            room_number=data.get('room_number'),
            procedures=data.get('procedures', []),
            billing=billing,
            status=data.get('status', 'normal')
        )