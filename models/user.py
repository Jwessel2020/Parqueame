# models/user.py

class User:
    def __init__(self, id, username, password, name, email, phone, favorites=None, vehicles=None):
        self.id = id
        self.username = username
        self.password = password  # Note: In production, use hashed passwords
        self.name = name
        self.email = email
        self.phone = phone
        self.favorites = favorites if favorites else []
        self.vehicles = vehicles if vehicles else []  # List of vehicle dictionaries

    def authenticate(self, password):
        return self.password == password  # In production, use a secure compare function

    def add_favorite(self, parking_spot_id):
        if parking_spot_id not in self.favorites:
            self.favorites.append(parking_spot_id)

    def remove_favorite(self, parking_spot_id):
        if parking_spot_id in self.favorites:
            self.favorites.remove(parking_spot_id)

    def update_info(self, name=None, email=None, phone=None):
        if name:
            self.name = name
        if email:
            self.email = email
        if phone:
            self.phone = phone

    def add_vehicle(self, vehicle):
        self.vehicles.append(vehicle)

    def remove_vehicle(self, vehicle_id):
        self.vehicles = [v for v in self.vehicles if v['id'] != vehicle_id]
