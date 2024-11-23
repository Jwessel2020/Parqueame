# app.py
from flask import Flask, render_template, request, redirect, url_for, session, flash
from utils import data_handler, auth
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key

# Home Route
@app.route('/')
def home():
    return redirect(url_for('search'))

# Search Route
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

# Reserve Parking Spot
@app.route('/reserve/<int:spot_id>', methods=['GET', 'POST'])
@auth.login_required
def reserve(spot_id):
    if request.method == 'POST':
        user_id = session.get('user_id')
        date = request.form.get('date')
        time = request.form.get('time')
        duration = request.form.get('duration')
        data_handler.create_booking(user_id, spot_id, date, time, duration)
        flash('Reservation successful!')
        return redirect(url_for('bookings'))
    parking_spot = data_handler.get_parking_spot_by_id(spot_id)
    return render_template('reserve.html', parking_spot=parking_spot)

# Bookings Route
@app.route('/bookings')
@auth.login_required
def bookings():
    user_id = session.get('user_id')
    user_bookings = data_handler.get_user_bookings(user_id)
    return render_template('bookings.html', bookings=user_bookings)

# Favorites Route
@app.route('/favorites')
@auth.login_required
def favorites():
    user_id = session.get('user_id')
    favorite_spots = data_handler.get_user_favorites(user_id)
    return render_template('favorites.html', favorites=favorite_spots)

# Add to Favorites
@app.route('/add_favorite/<int:spot_id>')
@auth.login_required
def add_favorite(spot_id):
    user_id = session.get('user_id')
    data_handler.add_favorite(user_id, spot_id)
    flash('Added to favorites!')
    return redirect(url_for('favorites'))

# Remove from Favorites
@app.route('/remove_favorite/<int:spot_id>')
@auth.login_required
def remove_favorite(spot_id):
    user_id = session.get('user_id')
    data_handler.remove_favorite(user_id, spot_id)
    flash('Removed from favorites!')
    return redirect(url_for('favorites'))

# Account Route
@app.route('/account', methods=['GET', 'POST'])
@auth.login_required
def account():
    user_id = session.get('user_id')
    if request.method == 'POST':
        # Update user information
        updated_info = {
            'name': request.form.get('name'),
            'email': request.form.get('email'),
            'phone': request.form.get('phone'),
        }
        data_handler.update_user_info(user_id, updated_info)
        flash('Account information updated!')
        return redirect(url_for('account'))
    user_info = data_handler.get_user_info(user_id)
    return render_template('account.html', user=user_info)

# Information Route
@app.route('/information')
def information():
    return render_template('information.html')

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = auth.authenticate(request.form['username'], request.form['password'])
        if user:
            session['user_id'] = user['id']
            flash('Login successful!')
            return redirect(url_for('search'))
        else:
            error = 'Invalid credentials'
            return render_template('login.html', error=error)
    return render_template('login.html')

# Logout Route
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.')
    return redirect(url_for('search'))

if __name__ == '__main__':
    app.run(debug=True)
