# models/booking.py
from datetime import datetime

class Booking:
    def __init__(self, id, user_id, parking_spot_id, parking_spot_name, start_datetime, end_datetime, total_price, vehicle_id=None, vehicle_info=None):
        self.id = id
        self.user_id = user_id
        self.parking_spot_id = parking_spot_id
        self.parking_spot_name = parking_spot_name
        self.start_datetime = start_datetime  # datetime object
        self.end_datetime = end_datetime      # datetime object
        self.total_price = total_price
        self.vehicle_id = vehicle_id
        self.vehicle_info = vehicle_info

    # Existing methods...

