import json


class Database:
    CUSTOMER_FILE = "data/customers.json"

    @staticmethod
    def load_customers():
        try:
            with open(Database.CUSTOMER_FILE, "r") as file:
                return json.load(file)
        except:
            return []

    @staticmethod
    def save_customers(customers):
        with open(Database.CUSTOMER_FILE, "w") as file:
            json.dump(customers, file, indent=4)

    @staticmethod
    def load_bookings():
        try:
            with open("data/bookings.json", "r") as file:
                return json.load(file)
        except:
            return []

    @staticmethod
    def save_bookings(bookings):
        with open("data/bookings.json", "w") as file:
            json.dump(bookings, file, indent=4)

    @staticmethod
    def load_feedback():
        try:
            with open("data/feedback.json", "r") as file:
                return json.load(file)
        except:
            return []

    @staticmethod
    def save_feedback(feedback):
        with open("data/feedback.json", "w") as file:
            json.dump(feedback, file, indent=4)

    @staticmethod
    def load_officers():
        try:
            with open("data/officers.json", "r") as file:
                return json.load(file)
        except:
            return []