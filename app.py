# app.py

from flask import Flask, render_template, request, redirect, url_for, session, flash
from utils import data_handler, auth
from models.user import User
from models.parking_spot import ParkingSpot
from models.booking import Booking
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Existing routes...


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
            'start_datetime': request.form.get('start_datetime'),
            'end_datetime': request.form.get('end_datetime'),
        }
        parking_spots = data_handler.get_parking_spots(filters)
    else:
        parking_spots = data_handler.get_all_parking_spots()

    # Get user's favorites if logged in
    user_favorites = []
    if 'user_id' in session:
        user = data_handler.get_user_by_id(session.get('user_id'))
        user_favorites = user.favorites
    else:
        user = None

    return render_template('search.html', parking_spots=parking_spots, user=user, user_favorites=user_favorites)

# app.py

@app.route('/add_vehicle', methods=['GET', 'POST'])
@auth.login_required
def add_vehicle():
    user = data_handler.get_user_by_id(session.get('user_id'))
    if request.method == 'POST':
        make = request.form.get('make')
        model = request.form.get('model')
        license_plate = request.form.get('license_plate')
        vehicle_id = data_handler.get_next_vehicle_id(user)
        vehicle = {
            'id': vehicle_id,
            'make': make,
            'model': model,
            'license_plate': license_plate
        }
        user.add_vehicle(vehicle)
        data_handler.update_user(user)
        flash('Vehicle added successfully!')
        return redirect(url_for('account'))
    return render_template('add_vehicle.html')

# app.py

@app.route('/remove_vehicle/<int:vehicle_id>', methods=['POST'])
@auth.login_required
def remove_vehicle(vehicle_id):
    user = data_handler.get_user_by_id(session.get('user_id'))
    user.remove_vehicle(vehicle_id)
    data_handler.update_user(user)
    flash('Vehicle removed successfully!')
    return redirect(url_for('account'))


# Reserve Parking Spot
@app.route('/reserve/<int:spot_id>', methods=['GET', 'POST'])
@auth.login_required
def reserve(spot_id):
    parking_spot = data_handler.get_parking_spot_by_id(spot_id)
    if request.method == 'POST':
        user = data_handler.get_user_by_id(session.get('user_id'))
        start_datetime_str = request.form.get('start_datetime')
        end_datetime_str = request.form.get('end_datetime')

        # Convert strings to datetime objects
        start_datetime = datetime.fromisoformat(start_datetime_str)
        end_datetime = datetime.fromisoformat(end_datetime_str)

        # Validate that end time is after start time
        if end_datetime <= start_datetime:
            flash('End time must be after start time.')
            return redirect(url_for('reserve', spot_id=spot_id))

        # Check availability
        bookings = data_handler.load_bookings()
        if not parking_spot.is_available(start_datetime, end_datetime, bookings):
            flash('Parking spot is not available during the selected time.')
            return redirect(url_for('reserve', spot_id=spot_id))

        # Calculate total price
        duration_hours = (end_datetime - start_datetime).total_seconds() / 3600
        total_price = parking_spot.price_per_hour * duration_hours

        booking = Booking(
            id=data_handler.get_next_booking_id(),
            user_id=user.id,
            parking_spot_id=parking_spot.id,
            parking_spot_name=parking_spot.name,
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            total_price=total_price
        )
        data_handler.create_booking(booking)
        flash('Reservation successful!')
        return redirect(url_for('bookings'))

    return render_template('reserve.html', parking_spot=parking_spot)

# Bookings Route
@app.route('/bookings')
@auth.login_required
def bookings():
    user = data_handler.get_user_by_id(session.get('user_id'))
    user_bookings = data_handler.get_user_bookings(user.id)
    return render_template('bookings.html', bookings=user_bookings)

# Favorites Route
@app.route('/favorites')
@auth.login_required
def favorites():
    user = data_handler.get_user_by_id(session.get('user_id'))
    favorite_spots = data_handler.get_user_favorites(user)
    return render_template('favorites.html', favorites=favorite_spots)

# Add to Favorites
@app.route('/add_favorite/<int:spot_id>')
@auth.login_required
def add_favorite(spot_id):
    user = data_handler.get_user_by_id(session.get('user_id'))
    user.add_favorite(spot_id)
    data_handler.update_user(user)
    flash('Added to favorites!')
    return redirect(url_for('favorites'))

# Remove from Favorites
@app.route('/remove_favorite/<int:spot_id>')
@auth.login_required
def remove_favorite(spot_id):
    user = data_handler.get_user_by_id(session.get('user_id'))
    user.remove_favorite(spot_id)
    data_handler.update_user(user)
    flash('Removed from favorites!')
    return redirect(url_for('favorites'))

@app.route('/account', methods=['GET', 'POST'])
@auth.login_required
def account():
    user = data_handler.get_user_by_id(session.get('user_id'))
    if request.method == 'POST':
        # Update user information
        user.update_info(
            name=request.form.get('name'),
            email=request.form.get('email'),
            phone=request.form.get('phone')
        )
        data_handler.update_user(user)
        flash('Account information updated!')
        return redirect(url_for('account'))
    return render_template('account.html', user=user)


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
            session['user_id'] = user.id
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
