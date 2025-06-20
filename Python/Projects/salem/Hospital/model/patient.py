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
    register_date (str, optional): The date of registration of the patient.
    discharge_date (str, optional): The date of discharge of the patient.
    date_of_death (str, optional): The date of death of the patient.
    insurance (dict): Insurance information for the patient.
"""

class Patient(Person):
    def __init__(self, name, age, condition, patient_number, phone_number, date_of_birth, gender, email, address, identifier, patient_next_of_kin, room_number=None, procedures=None, billing=None, status='normal', register_date=None, discharge_date=None, date_of_death=None, insurance=None):
        super().__init__(name, age, phone_number, date_of_birth, gender, email, address, identifier)
        self.condition = condition
        self.patient_number = patient_number
        # Ensure next_of_kin is a dict with required keys
        if isinstance(patient_next_of_kin, dict):
            self.patient_next_of_kin = {
                'name': patient_next_of_kin.get('name', ''),
                'number': patient_next_of_kin.get('number', ''),
                'email': patient_next_of_kin.get('email', ''),
                'relation': patient_next_of_kin.get('relation', '')
            }
        else:
            self.patient_next_of_kin = {'name': '', 'number': '', 'email': '', 'relation': ''}
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
        self.register_date = register_date
        self.discharge_date = discharge_date
        self.date_of_death = date_of_death
        # Insurance info: dict with provider, policy_number, coverage_percent
        if insurance is not None:
            self.insurance = {
                'provider': insurance.get('provider', ''),
                'policy_number': insurance.get('policy_number', ''),
                'coverage_percent': insurance.get('coverage_percent', 0)
            }
        else:
            self.insurance = {'provider': '', 'policy_number': '', 'coverage_percent': 0}

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
            'patient_next_of_kin': self.patient_next_of_kin,
            'room_number': self.room_number,
            'phone_number': self.phone_number,
            'date_of_birth': self.date_of_birth,
            'gender': self.gender,
            'email': self.email,
            'address': self.address,
            'identifier': self.identifier,
            'procedures': self.procedures,
            'billing': [b.to_dict() for b in self.billing],
            'status': self.status,
            'register_date': self.register_date,
            'discharge_date': self.discharge_date,
            'date_of_death': self.date_of_death,
            'insurance': self.insurance,
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
            data['phone_number'],
            data['date_of_birth'],
            data['gender'],
            data['email'],
            data['address'],
            data['identifier'],
            data.get('patient_next_of_kin', {'name': '', 'number': '', 'email': '', 'relation': ''}),
            room_number=data.get('room_number'),
            procedures=data.get('procedures', []),
            billing=billing,
            status=data.get('status', 'normal'),
            register_date=data.get('register_date'),
            discharge_date=data.get('discharge_date'),
            date_of_death=data.get('date_of_death'),
            insurance=data.get('insurance', {'provider': '', 'policy_number': '', 'coverage_percent': 0})
        )