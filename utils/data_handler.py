# utils/data_handler.py

import json
import os
from models.user import User
from models.parking_spot import ParkingSpot
from models.booking import Booking
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')

def load_data(file_name):
    with open(os.path.join(DATA_DIR, file_name), 'r') as f:
        return json.load(f)

def save_data(file_name, data):
    with open(os.path.join(DATA_DIR, file_name), 'w') as f:
        json.dump(data, f, indent=4)

# **Update the load_users function to include vehicles**
def load_users():
    data = load_data('users.json')
    users = []
    for item in data:
        user = User(
            id=item['id'],
            username=item['username'],
            password=item['password'],
            name=item['name'],
            email=item['email'],
            phone=item['phone'],
            favorites=item.get('favorites', []),
            vehicles=item.get('vehicles', [])  # Load vehicles from user data
        )
        users.append(user)
    return users

# **Add a new function to save users**
def save_users(users):
    data = [user_to_dict(u) for u in users]
    save_data('users.json', data)

# **Update user_to_dict function to include vehicles**
def user_to_dict(user):
    return {
        'id': user.id,
        'username': user.username,
        'password': user.password,
        'name': user.name,
        'email': user.email,
        'phone': user.phone,
        'favorites': user.favorites,
        'vehicles': user.vehicles  # Include vehicles when saving
    }

def get_user_by_id(user_id):
    users = load_users()
    return next((user for user in users if user.id == user_id), None)

# **Update the update_user function to use save_users**
def update_user(user):
    users = load_users()
    for idx, u in enumerate(users):
        if u.id == user.id:
            users[idx] = user
            break
    save_users(users)

def load_parking_spots():
    data = load_data('parkingspots.json')
    spots = []
    for item in data:
        spot = ParkingSpot(
            id=item['id'],
            name=item['name'],
            address=item['address'],
            price_per_hour=item['pricePerHour'],
            available=item.get('available', True)
        )
        spots.append(spot)
    return spots

def get_all_parking_spots():
    return load_parking_spots()

def get_parking_spots(filters):
    spots = load_parking_spots()
    bookings = load_bookings()
    # Filter by location
    if filters['location']:
        spots = [spot for spot in spots if filters['location'].lower() in spot.address.lower()]

    # Filter by availability during the desired time range
    if filters['start_datetime'] and filters['end_datetime']:
        start_datetime = datetime.fromisoformat(filters['start_datetime'])
        end_datetime = datetime.fromisoformat(filters['end_datetime'])
        available_spots = []
        for spot in spots:
            if spot.is_available(start_datetime, end_datetime, bookings):
                available_spots.append(spot)
        spots = available_spots
    return spots

def get_parking_spot_by_id(spot_id):
    spots = load_parking_spots()
    return next((spot for spot in spots if spot.id == spot_id), None)

def get_user_bookings(user_id):
    bookings = load_bookings()
    return [booking for booking in bookings if booking.user_id == user_id]

def get_next_booking_id():
    bookings = load_bookings()
    return max([b.id for b in bookings], default=0) + 1

def create_booking(booking):
    bookings = load_bookings()
    bookings.append(booking)
    # Convert bookings to dicts before saving
    data = [booking_to_dict(b) for b in bookings]
    save_data('bookings.json', data)

# **Update booking_to_dict to include vehicle_info**
def booking_to_dict(booking):
    return {
        'id': booking.id,
        'user_id': booking.user_id,
        'parking_spot_id': booking.parking_spot_id,
        'parking_spot_name': booking.parking_spot_name,
        'start_datetime': booking.start_datetime.isoformat(),
        'end_datetime': booking.end_datetime.isoformat(),
        'total_price': booking.total_price,
        'vehicle_id': booking.vehicle_id,
        'vehicle_info': booking.vehicle_info  # Include vehicle info
    }

# **Update load_bookings to load vehicle_info**
def load_bookings():
    data = load_data('bookings.json')
    bookings = []
    for item in data:
        booking = Booking(
            id=item['id'],
            user_id=item['user_id'],
            parking_spot_id=item['parking_spot_id'],
            parking_spot_name=item['parking_spot_name'],
            start_datetime=datetime.fromisoformat(item['start_datetime']),
            end_datetime=datetime.fromisoformat(item['end_datetime']),
            total_price=item['total_price'],
            vehicle_id=item['vehicle_id'],
            vehicle_info=item['vehicle_info']  # Load vehicle info
        )
        bookings.append(booking)
    return bookings

def get_user_info(user_id):
    return get_user_by_id(user_id)

def get_user_favorites(user):
    spots = load_parking_spots()
    favorite_spots = [spot for spot in spots if spot.id in user.favorites]
    return favorite_spots

# **Add function to generate next vehicle ID**
def get_next_vehicle_id(user):
    vehicle_ids = [v['id'] for v in user.vehicles]
    return max(vehicle_ids, default=0) + 1
