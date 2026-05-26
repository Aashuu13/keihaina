from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import re

from app.controllers.auth import register_user, login_user_controller, logout_user_controller

auth_bp = Blueprint('auth', __name__)

# Strong Password Validator
def strong_password(form, field):
    password = field.data
    if len(password) < 8:
        raise ValidationError('Password must be at least 8 characters.')
    if not re.search(r"[A-Z]", password):
        raise ValidationError('Password must contain at least one uppercase letter.')
    if not re.search(r"[a-z]", password):
        raise ValidationError('Password must contain at least one lowercase letter.')
    if not re.search(r"[0-9]", password):
        raise ValidationError('Password must contain at least one number.')
    if not re.search(r"[@$!%*?&]", password):
        raise ValidationError('Password must contain at least one special character (@$!%*?&).')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
        DataRequired(), Length(min=8), strong_password
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), EqualTo('password', message='Passwords must match')
    ])

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('product.product'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        success, message = register_user(
            form.username.data, 
            form.email.data, 
            form.password.data
        )
        flash(message, 'success' if success else 'danger')
        if success:
            return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('product.product'))
    
    form = LoginForm()
    if form.validate_on_submit():
        success, message = login_user_controller(
            form.username.data, 
            form.password.data, 
            form.remember.data
        )
        flash(message, 'success' if success else 'danger')
        if success:
            return redirect(url_for('product.product'))
    return render_template('login.html', form=form)
@auth_bp.route('/dashboard')
@login_required
def dashboard():
    return "Welcome to your dashboard, {}!".format(current_user.username)
@login_required
def logout():
    message = logout_user_controller()
    flash(message, 'info')
    return redirect(url_for('auth.login'))
    