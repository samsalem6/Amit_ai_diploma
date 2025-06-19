class Login:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def authenticate(self) -> bool:
        # Placeholder for authentication logic
        # In a real application, this would check the credentials against a database
        return self.username == "admin" and self.password == "admin"
    
    def get_user_info(self) -> dict:
        # Placeholder for user information retrieval
        # In a real application, this would fetch user details from a database
        return {
            "username": self.username,
            "role": "admin" if self.username == "admin" else "user"
        }
    def login(self) -> str:
        if self.authenticate():
            user_info = self.get_user_info()
            return f"Login successful! Welcome {user_info['username']} ({user_info['role']})"
        else:
            return "Login failed! Invalid username or password."
        
    