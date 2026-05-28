from flask import flash, redirect, url_for, request, render_template
from flask_login import login_user, logout_user, current_user

from app.controllers.basecontroller import BaseController
from app.models.user import User, users_db


class AuthController(BaseController):
    """
    Authentication Controller
    """

    def __init__(self):
        super().__init__()

    def register(self):

        if self.is_logged_in():
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

            # Create user
            new_user = User(
                name=name,
                email=email,
                password=password,
                role="user"
            )

            if new_user.email_exists():
                flash("Email already exists.", "danger")
                return redirect(url_for("auth.register"))

            new_user.save()

            flash("Registration successful! Please login.", "success")
            return redirect(url_for("auth.login"))

        return render_template("register.html")

    def dashboard(self):
        return "Welcome to your dashboard, {}!".format(current_user.name)


def login_user_controller(username, password, remember=False):
    

    user = User.get_by_username(username)

    if user and user.verify_password(password):
        login_user(user, remember=remember)
        return True, "Login successful!"

    return False, "Invalid username or password!"
def register_user(username, email, password):

    # Check if username/email exists
    existing_user = User.get_by_username(username)

    if existing_user:
        return False, "Username already exists!"

    # Create new user
    new_user = User(
        name=username,
        email=email,
        password=password,
        role="user"
    )

    # Save user
    new_user.save()

    return True, "Registration successful!"


def logout_user_controller():

    logout_user()
    return "Logged out successfully!"