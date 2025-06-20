"""
Represents a billing record for a patient.
Attributes:
    amount (float): The amount to be billed.
    description (str): Description of the billing item.
    paid (bool): Status indicating if the bill has been paid.
"""
class Billing:
    def __init__(self, amount, description, paid=False):
        self.amount = amount
        self.description = description
        self.paid = paid

    def mark_paid(self):
        """
        Mark the billing record as paid.
        """
        self.paid = True

    def to_dict(self):
        """
        Convert the Billing object to a dictionary.

        Returns:
            dict: A dictionary representation of the billing record.
        """
        return {
            'amount': self.amount,
            'description': self.description,
            'paid': self.paid
        }

    @staticmethod
    def from_dict(data):
        """
        Create a Billing object from a dictionary.

        Args:
            data (dict): A dictionary with keys 'amount', 'description', and optionally 'paid'.

        Returns:
            Billing: A Billing object created from the dictionary data.
        """
        return Billing(data['amount'], data['description'], data.get('paid', False))

    def get_discounted_amount(self, insurance_coverage_percent=0):
        """
        Calculate the amount after applying insurance discount.
        Args:
            insurance_coverage_percent (float): The percent of the bill covered by insurance (0-100).
        Returns:
            float: The discounted amount to be paid by the patient.
        """
        discount = (insurance_coverage_percent / 100) * self.amount
        return self.amount - discount 