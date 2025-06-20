class Person:
    """Represents a generic person with a name and age."""
    def __init__(self, name: str, age: int, phone_number: str, date_of_birth: str, gender: str, email: str, address: str, identifier: str):
        self.name = name
        self.age = age
        self.phone_number = phone_number
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.email = email
        self.address = address
        self.identifier = identifier
    def __str__(self):
        """
        Return a string representation of the person.
        Returns:
            str: String with the person's name and age.
        """
        return f"Name: {self.name}, Age: {self.age}"
    
    def __repr__(self):
        """
        Return a detailed string representation of the person for debugging.
        Returns:
            str: Detailed string with the person's name and age.
        """
        return f"Person(name={self.name}, age={self.age})"  
    
    def view_info(self):
        """
        View the person's information.
        Returns:
            str: String with the person's name and age.
        """
        return f"Name: {self.name}, Age: {self.age}, Phone Number: {self.phone_number}, Date of Birth: {self.date_of_birth}, Gender: {self.gender}, Email: {self.email}, Address: {self.address}, Identifier: {self.identifier}"