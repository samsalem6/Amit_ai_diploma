class Person:
    """Represents a generic person with a name and age."""
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age
    
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
        return f"Name: {self.name}, Age: {self.age}"