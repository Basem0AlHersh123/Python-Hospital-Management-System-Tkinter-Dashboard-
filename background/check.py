import re
class Check:
    def __init__(self,*args):
        self.list=[self.arg for self.arg in args ]
    @staticmethod
    def check_box(*args):
        for arg in args:
            if arg!='':
                continue
            elif arg=="":
                return False
        return True
    @staticmethod
    def is_valid_username(username,data):
        if bool(username) and len(username)>3 :
            for user in data:
                if username in user.values():
                    return "Username found. Please use another one"
            return False
        return "Username must be at least 3 characters"
    @staticmethod
    def is_valid_password(password):
        return bool(re.match(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}$", password))
    @staticmethod
    def is_valid_phone(phone):
        return bool(re.match(r'^\d{9}$', phone))
    @staticmethod
    def is_valid_email(email):
        return bool(re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email))
    @staticmethod
    def is_valid_date(dt_txt):
        from datetime import datetime
        if not dt_txt:
                return "Missing"
        try:
            datetime.fromisoformat(dt_txt.replace(" ", "T"))
        except Exception:
            return "Bad format"
        return True