import re
from datetime import datetime


class Validation:

    @staticmethod
    def validate_email(email):
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(pattern, email)

    @staticmethod
    def validate_mobile(mobile):
        return (
            len(mobile) == 10
            and mobile.isdigit()
            and mobile[0] in "6789"
        )

    @staticmethod
    def validate_password(password):
        return (
            len(password) >= 8
            and any(c.isupper() for c in password)
            and any(c.islower() for c in password)
            and any(c.isdigit() for c in password)
            and any(not c.isalnum() for c in password)
        )

    @staticmethod
    def email_exists(email, customers):
        return any(
            customer["email"].lower() == email.lower()
            for customer in customers
        )

    @staticmethod
    def mobile_exists(mobile, customers):
        return any(
            customer["mobile"] == mobile
            for customer in customers
        )

    @staticmethod
    def validate_weight(weight):
        try:
            weight = float(weight)
            return weight > 0
        except ValueError:
            return False

    @staticmethod
    def valid_pickup_date(pickup_date):
        try:
            pickup = datetime.strptime(
                pickup_date,
                "%d-%m-%Y"
            )
            today = datetime.today()

            # Allow today or future date
            return pickup.date() >= today.date()

        except ValueError:
            return False

    @staticmethod
    def valid_drop_date(pickup_date, drop_date):
        try:
            pickup = datetime.strptime(
                pickup_date,
                "%d-%m-%Y"
            )
            drop = datetime.strptime(
                drop_date,
                "%d-%m-%Y"
            )

            return drop.date() > pickup.date()

        except ValueError:
            return False

    @staticmethod
    def validate_description(
        description,
        max_length=200
    ):
        return 1 <= len(description) <= max_length

    @staticmethod
    def validate_upi(upi_id):
        return (
            "@" in upi_id
            and len(upi_id.strip()) > 3
        )

    @staticmethod
    def validate_card_number(card_number):
        return (
            len(card_number) == 16
            and card_number.isdigit()
        )

    @staticmethod
    def validate_cvv(cvv):
        return (
            len(cvv) == 3
            and cvv.isdigit()
        )

    @staticmethod
    def validate_expiry(expiry):
        if len(expiry) != 5:
            return False

        if expiry[2] != "/":
            return False

        month, year = expiry.split("/")

        if not month.isdigit() or not year.isdigit():
            return False

        return 1 <= int(month) <= 12

    @staticmethod
    def validate_rating(rating):
        return rating in ["1", "2", "3", "4", "5"]