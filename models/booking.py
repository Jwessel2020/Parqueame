# models/booking.py
from datetime import datetime

class Booking:
    def __init__(self, id, user_id, parking_spot_id, parking_spot_name, start_datetime, end_datetime, total_price):
        self.id = id
        self.user_id = user_id
        self.parking_spot_id = parking_spot_id
        self.parking_spot_name = parking_spot_name
        self.start_datetime = start_datetime  # datetime object
        self.end_datetime = end_datetime      # datetime object
        self.total_price = total_price

    def overlaps(self, other_start, other_end):
        return self.start_datetime < other_end and other_start < self.end_datetime
