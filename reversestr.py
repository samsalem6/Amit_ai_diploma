"""
A class to reverse the word order in a string

This class takes a string input and provides functionality to reverse
the order of words while maintaining the words themselves intact.

Attributes:
    string (str): The input string to be processed
"""


class ReverseStr2:
    def __init__(self, string):
        self.string = string
    
    def reverse(self):
        """Reverse the order of words in the input string
        
        Algorithm:
        1. Split string into list of words
        2. Reverse the list using slice notation
        3. Join words back together with spaces
        
        Returns:
            str: A new string with the words in reverse order
        """
        lst = self.string.split(" ")
        new_lst = lst[::-1]
        new_str = " ".join(new_lst)
        return new_str