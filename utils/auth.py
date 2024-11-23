# utils/auth.py
from functools import wraps
from flask import session, redirect, url_for
from .data_handler import load_data

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def authenticate(username, password):
    users = load_data('users.json')
    user = next((user for user in users if user['username'] == username and user['password'] == password), None)
    return user
