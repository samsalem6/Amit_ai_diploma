from .person import Person

"""
Class for hospital staff, inheriting from Person.
Attributes:
    name (str): The name of the staff member.
    age (int): The age of the staff member.
    position (str): The position/job title of the staff member.
"""
class Staff(Person):
    def __init__(self, name, age, position):
        super().__init__(name, age)
        self.position = position

    def view_info(self):
        """
        View staff information.
        Returns:
            str: String with the staff member's name, age, and position.
        """
        return f"Staff Name: {self.name}, Age: {self.age}, Position: {self.position}"