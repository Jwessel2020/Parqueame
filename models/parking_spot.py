# models/parking_spot.py
from datetime import datetime

class ParkingSpot:
    def __init__(self, id, name, address, price_per_hour, available=True):
        self.id = id
        self.name = name
        self.address = address
        self.price_per_hour = price_per_hour
        self.available = available  # This field becomes less relevant with time based availability

    def is_available(self, start_datetime, end_datetime, bookings):
        for booking in bookings:
            if booking.parking_spot_id == self.id and booking.overlaps(start_datetime, end_datetime):
                return False
        return True
