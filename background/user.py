# background/user.py
import hashlib
from background.file_manager import FileManager

class User:
    def __init__(self, ID, username, password, role, full_name="", phone="", active=True):
        self.id = ID
        self.username = username
        self.password = password  
        self.role = role
        self.full_name = full_name
        self.phone = phone
        self.active = active

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.username,
            "password": self.password,
            "role": self.role,
            "full_name": self.full_name,
            "phone": self.phone,
            "active": self.active
        }
    @staticmethod
    def hash_password(plain_text):
        return hashlib.sha256(plain_text.encode("utf-8")).hexdigest()
    @staticmethod
    def load_user():
        return FileManager.load_data("users")
    @staticmethod
    def save_user(user_list):
        return FileManager.save_data("users", user_list)
    @staticmethod
    def authenticate(users, username, password):
        if not username or not password:
            return "Please fill username and password"
        hashed_input = User.hash_password(password)
        for user in users:
            if user.get("name") == username:
                if not user.get("active", True):
                    return "Account is inactive"
                stored_password = user.get("password")
                if stored_password == hashed_input or user.get("password")==password:
                    return True
                else:
                    return "Sorry invalid Password"
        return "Sorry invalid username"
