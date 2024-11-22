# app.py
from flask import Flask, render_template, request, redirect, url_for, session
from utils import data_handler, auth
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key

# Routes
@app.route('/')
def home():
    return redirect(url_for('search'))

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        filters = {
            'location': request.form.get('location'),
            'date': request.form.get('date'),
            'time': request.form.get('time'),
        }
        parking_spots = data_handler.get_parking_spots(filters)
    else:
        parking_spots = data_handler.get_all_parking_spots()
    return render_template('search.html', parking_spots=parking_spots)

@app.route('/bookings')
@auth.login_required
def bookings():
    user_id = session.get('user_id')
    user_bookings = data_handler.get_user_bookings(user_id)
    return render_template('bookings.html', bookings=user_bookings)

@app.route('/favorites')
@auth.login_required
def favorites():
    user_id = session.get('user_id')
    favorite_spots = data_handler.get_user_favorites(user_id)
    return render_template('favorites.html', favorites=favorite_spots)

@app.route('/account', methods=['GET', 'POST'])
@auth.login_required
def account():
    user_id = session.get('user_id')
    if request.method == 'POST':
        # Update user information
        pass
    user_info = data_handler.get_user_info(user_id)
    return render_template('account.html', user=user_info)

@app.route('/information')
def information():
    return render_template('information.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = auth.authenticate(request.form['username'], request.form['password'])
        if user:
            session['user_id'] = user['id']
            return redirect(url_for('search'))
        else:
            error = 'Invalid credentials'
            return render_template('login.html', error=error)
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('search'))

if __name__ == '__main__':
    app.run(debug=True)
