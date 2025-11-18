# models/user.py
class User:
    def __init__(self, user_id, name=None):
        self.user_id = user_id
        self.name = name or f"User {user_id}"

    def to_dict(self):
        return {"user_id": self.user_id, "name": self.name}
    
    def change_name(self, new_name):
        self.name = new_name

    @staticmethod
    def from_dict(data):
        return User(data["user_id"], data["name"])
