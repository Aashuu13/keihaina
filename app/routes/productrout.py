from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

product_bp = Blueprint('product', __name__)

@product_bp.route('/')
def index():
    """Root URL"""
    if current_user.is_authenticated:
        return redirect(url_for('product.product'))
    else:
        return redirect(url_for('auth.login'))

@product_bp.route('/product')
@login_required
def product():
    """Protected Product Page"""
    return render_template('product.html', user=current_user)