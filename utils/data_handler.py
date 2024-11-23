# utils/data_handler.py
import json
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')

def load_data(file_name):
    with open(os.path.join(DATA_DIR, file_name), 'r') as f:
        return json.load(f)

def save_data(file_name, data):
    with open(os.path.join(DATA_DIR, file_name), 'w') as f:
        json.dump(data, f, indent=4)

def get_all_parking_spots():
    return load_data('parkingspots.json')

def get_parking_spots(filters):
    spots = get_all_parking_spots()
    # Filter by location
    if filters['location']:
        spots = [spot for spot in spots if filters['location'].lower() in spot['address'].lower()]
    # In this mock version, we don't filter by date and time
    return spots

def get_parking_spot_by_id(spot_id):
    spots = get_all_parking_spots()
    return next((spot for spot in spots if spot['id'] == spot_id), None)

def get_user_bookings(user_id):
    bookings = load_data('bookings.json')
    return [booking for booking in bookings if booking['user_id'] == user_id]

def create_booking(user_id, spot_id, date, time, duration):
    bookings = load_data('bookings.json')
    spots = get_all_parking_spots()
    spot = get_parking_spot_by_id(spot_id)
    total_price = spot['pricePerHour'] * int(duration)
    booking_id = max([b['id'] for b in bookings], default=0) + 1
    new_booking = {
        'id': booking_id,
        'user_id': user_id,
        'parking_spot_id': spot_id,
        'parking_spot_name': spot['name'],
        'date': date,
        'time': time,
        'duration': int(duration),
        'total_price': total_price
    }
    bookings.append(new_booking)
    save_data('bookings.json', bookings)

def get_user_info(user_id):
    users = load_data('users.json')
    return next((user for user in users if user['id'] == user_id), None)

def update_user_info(user_id, updated_info):
    users = load_data('users.json')
    for user in users:
        if user['id'] == user_id:
            user.update(updated_info)
            break
    save_data('users.json', users)

def get_user_favorites(user_id):
    user = get_user_info(user_id)
    favorites = user.get('favorites', [])
    spots = get_all_parking_spots()
    favorite_spots = [spot for spot in spots if spot['id'] in favorites]
    return favorite_spots

def add_favorite(user_id, spot_id):
    users = load_data('users.json')
    for user in users:
        if user['id'] == user_id:
            if 'favorites' not in user:
                user['favorites'] = []
            if spot_id not in user['favorites']:
                user['favorites'].append(spot_id)
            break
    save_data('users.json', users)

def remove_favorite(user_id, spot_id):
    users = load_data('users.json')
    for user in users:
        if user['id'] == user_id and 'favorites' in user:
            if spot_id in user['favorites']:
                user['favorites'].remove(spot_id)
            break
    save_data('users.json', users)
