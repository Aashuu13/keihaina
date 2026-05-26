from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import re

users_db = {}

class User(UserMixin):
    def __init__(self, id, username, email, password_hash):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash

    def get_id(self):
        return str(self.id)

    @staticmethod
    def create(password):
        return generate_password_hash(password, method='pbkdf2:sha256:600000')

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def get(user_id):
        for user in users_db.values():
            if str(user.id) == str(user_id):
                return user
        return None

    @staticmethod
    def get_by_username(username):
        return users_db.get(username)