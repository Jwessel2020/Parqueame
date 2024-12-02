# utils/auth.py
from functools import wraps
from flask import session, redirect, url_for
from .data_handler import load_users

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def authenticate(username, password):
    users = load_users()
    user = next((u for u in users if u.username == username), None)
    if user and user.authenticate(password):
        return user
    return Nonet
