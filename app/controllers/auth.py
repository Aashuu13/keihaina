from flask import flash, redirect, url_for, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models.user import User, users_db
from flask import session, flash, redirect, url_for, render_template, request
from app.controllers.basecontroller import BaseController
from app.models.user import User


class AuthController(BaseController):
    '''Controller for user authentication'''
    def __init__(self):
        super().__init__()

    def register(self):
        if self.is_logged_in():
            if session.get("user_role") == "admin":
                return redirect(url_for("admin.dashboard"))
            return redirect(url_for("auth.dashboard"))

        if request.method == "POST":
            name, email = self.get_form_data("name", "email")
            password = request.form.get("password", "")

            # Validation
            if not name or not email or not password:
                flash("All fields are required.", "danger")
                return render_template("register.html")

            if len(name) > 100:
                flash("Name must be under 100 characters.", "danger")
                return render_template("register.html")

            if len(password) < 6:
                flash("Password must be at least 6 characters.", "danger")
                return render_template("register.html")

            # Create a new User object and check email
            new_user = User(name=name, email=email, password=password, role="user")

            if new_user.email_exists():
                flash("Email already exists.", "danger")
                return redirect(url_for("auth.register"))

            # Save to database
            new_user.save()
            return self.flash_and_redirect(
                "Registration successful! Please login.", "success", "auth.login"
            )

        return render_template("register.html")
     


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