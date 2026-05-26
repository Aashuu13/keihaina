from flask import flash, redirect, url_for, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models.user import User, users_db


def register_user(username, email, password):
    """Register new user"""
    if username in users_db:
        return False, "Username already exists!"
    
    user = User(
        id=len(users_db) + 1,
        username=username,
        email=email,
        password_hash=User.create(password)
    )
    users_db[username] = user
    return True, "Registration successful!"


def login_user_controller(username, password, remember=False):
    """Login user"""
    user = User.get_by_username(username)
    if user and user.verify_password(password):
        login_user(user, remember=remember)
        return True, "Login successful!"
    return False, "Invalid username or password!"


def logout_user_controller():
    """Logout user"""
    logout_user()
    return "Logged out successfully!"