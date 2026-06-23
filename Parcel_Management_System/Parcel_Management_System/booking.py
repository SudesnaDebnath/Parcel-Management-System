from database import Database
from validation import Validation
from datetime import datetime


class Booking:

    def book_parcel(self, customer_id):
        bookings = Database.load_bookings()

        print("===== Parcel Booking =====")

        while True:
            receiver_name = input("Enter Receiver Name: ")
            if receiver_name:
                break
            print("Receiver Name cannot be blank!")

        while True:
            receiver_mobile = input("Enter Receiver Mobile: ")

            if not Validation.validate_mobile(receiver_mobile):
                print("Receiver Mobile is not valid!")
                continue

            break

        while True:
            try:
                weight = float(input("Enter Receiver Weight (kg): "))

                if Validation.validate_weight(weight):
                    break

                print("Weight cannot be negative!")

            except ValueError:
                print("Enter a valid weight!")

        overload_charge = 0

        if weight > 20:
            overload_charge = (weight - 20) * 10

            print("Parcel exceeds the allowed weight limit of 20 kg.")
            print(
                f"Extra Charge: Rs. {overload_charge} "
                "(Charge Rate: Rs. 10 per kg)"
            )

        while True:
            pickup_location = input("Enter Pickup Location: ")

            if pickup_location:
                break

            print("Pickup Location cannot be blank!")

        while True:
            drop_location = input("Enter Drop Location: ")

            if drop_location:
                break

            print("Drop Location cannot be blank!")

        if pickup_location.strip().lower() == drop_location.strip().lower():
            print("Pickup and Drop Location cannot be the same!")
            return

        print("\nDelivery Type")
        print("1. Standard")
        print("2. Express")
        print("3. Same Day")

        while True:
            delivery_choice = input("Enter Delivery Type: ")

            if delivery_choice == "1":
                delivery_type = "Standard"
                break

            elif delivery_choice == "2":
                delivery_type = "Express"
                break

            elif delivery_choice == "3":
                delivery_type = "Same Day"
                break

            print("Invalid Delivery Type!")

        print("\nPacking Preference")
        print("1. Basic")
        print("2. Premium")

        while True:
            packing_choice = input("Enter Packing Type: ")

            if packing_choice == "1":
                packing_type = "Basic"
                break

            elif packing_choice == "2":
                packing_type = "Premium"
                break

            print("Invalid Packing Type!")

        while True:
            pickup_date = input(
                "Enter Pickup Date (DD-MM-YYYY): "
            )

            if Validation.valid_pickup_date(pickup_date):
                break

            print(
                "Pickup date must be today or a future date!"
            )

        while True:
            drop_date = input(
                "Enter Drop Date (DD-MM-YYYY): "
            )

            if Validation.valid_drop_date(
                pickup_date,
                drop_date
            ):
                break

            print(
                "Drop date must be after pickup date!"
            )

        booking_id = "B" + str(
            1000 + len(bookings) + 1
        )

        base_amount = 100

        if delivery_type == "Express":
            base_amount += 50

        elif delivery_type == "Same Day":
            base_amount += 100

        if packing_type == "Premium":
            base_amount += 30

        total_amount = base_amount + overload_charge

        booking = {
            "booking_id": booking_id,
            "customer_id": customer_id,
            "receiver_name": receiver_name,
            "receiver_mobile": receiver_mobile,
            "pickup_location": pickup_location,
            "drop_location": drop_location,
            "weight": weight,
            "delivery_type": delivery_type,
            "packing_type": packing_type,
            "pickup_date": pickup_date,
            "drop_date": drop_date,
            "booking_time": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "amount": total_amount,
            "overload_charge": overload_charge,
            "payment_status": "Pending",
            "payment_method": "",
            "status": "Booked"
        }

        if isinstance(bookings, dict):
            bookings = [bookings]

        bookings.append(booking)

        Database.save_bookings(bookings)

        print("\nParcel Booking Complete")
        print("Booking ID:", booking_id)
        print("Total Amount: Rs.", total_amount)
        print("Booking Status:", booking["status"])

        # ----------------------------------------------------
def pay_parcel(self, customer_id):
    bookings = Database.load_bookings()

    found = False

    print("\n===== Pay Parcel =====")

    for booking in bookings:
        if (
            booking["customer_id"] == customer_id
            and booking["payment_status"] == "Pending"
        ):
            found = True

            print("\nBooking Id:", booking["booking_id"])
            print("Amount: Rs.", booking["amount"])

    if not found:
        print("No Pending Payments Found!")
        return

    booking_id = input("\nEnter Booking ID: ")

    selected_booking = None

    for booking in bookings:
        if (
            booking["booking_id"] == booking_id
            and booking["customer_id"] == customer_id
        ):
            selected_booking = booking
            break

    if selected_booking is None:
        print("Booking ID Not Found!")
        return

    print("\nAmount: Rs.", selected_booking["amount"])

    print("\n===== Select Payment Method =====")
    print("1. UPI")
    print("2. Credit Card")
    print("3. Debit Card")
    print("4. Net Banking")
    print("5. Wallet")

    paymethod_choice = input("Enter Payment Method: ")

    if paymethod_choice == "1":

        while True:
            upi_id = input("Enter UPI ID: ")

            if Validation.validate_upi(upi_id):
                break

            print("Invalid UPI ID!")

        payment_method = "UPI"

    elif paymethod_choice == "2":

        while True:
            card_number = input("Enter Card Number: ")

            if Validation.validate_card_number(card_number):
                break

            print("Card Number must be 16 digits!")

        while True:
            expiry = input("Enter Expiry Date (MM/YY): ")

            if Validation.validate_expiry(expiry):
                break

            print("Invalid Expiry Date!")

        while True:
            cvv = input("Enter CVV: ")

            if Validation.validate_cvv(cvv):
                break

            print("CVV must be 3 digits!")

        payment_method = "Credit Card"

    elif paymethod_choice == "3":

        while True:
            card_number = input("Enter Card Number: ")

            if Validation.validate_card_number(card_number):
                break

            print("Card Number must be 16 digits!")

        while True:
            expiry = input("Enter Expiry Date (MM/YY): ")

            if Validation.validate_expiry(expiry):
                break

            print("Invalid Expiry Date!")

        while True:
            cvv = input("Enter CVV: ")

            if Validation.validate_cvv(cvv):
                break

            print("CVV must be 3 digits!")

        payment_method = "Debit Card"

    elif paymethod_choice == "4":

        print("\nSelect Bank")
        print("1. SBI")
        print("2. HDFC")
        print("3. ICICI")
        print("4. AXIS")
        print("5. PNB")

        bank_choice = input("Enter Choice: ")

        bank_map = {
            "1": "SBI",
            "2": "HDFC",
            "3": "ICICI",
            "4": "AXIS",
            "5": "PNB"
        }

        if bank_choice not in bank_map:
            print("Invalid Bank Choice!")
            return

        user_id = input("Enter Net Banking User ID: ")

        payment_method = (
            "Net Banking - "
            + bank_map[bank_choice]
        )

    elif paymethod_choice == "5":

        print("\nSelect Wallet")
        print("1. Paytm")
        print("2. Amazon Pay")
        print("3. PhonePe")

        wallet_choice = input("Enter Choice: ")

        wallet_map = {
            "1": "Paytm",
            "2": "Amazon Pay",
            "3": "PhonePe"
        }

        if wallet_choice not in wallet_map:
            print("Invalid Wallet Choice!")
            return

        while True:
            mobile = input(
                "Enter Mobile Number: "
            )

            if Validation.validate_mobile(mobile):
                break

            print("Invalid Mobile Number!")

        payment_method = (
            "Wallet - "
            + wallet_map[wallet_choice]
        )

    else:
        print("Invalid Payment Method!")
        return

    confirm = input(
        "\nConfirm Payment (Y/N): "
    )

    if confirm.upper() != "Y":
        print("Payment Cancelled!")
        return

    transaction_id = (
        "TXN"
        + selected_booking["booking_id"][1:]
    )

    selected_booking["payment_status"] = "Paid"
    selected_booking["payment_method"] = payment_method
    selected_booking["transaction_id"] = transaction_id

    selected_booking["payment_date"] = (
        datetime.now().strftime(
            "%d-%m-%Y %H:%M:%S"
        )
    )

    Database.save_bookings(bookings)

    print("\n===== Payment Receipt =====")
    print("Booking ID:", selected_booking["booking_id"])
    print("Transaction ID:", transaction_id)
    print("Amount Paid: Rs.", selected_booking["amount"])
    print("Method:", selected_booking["payment_method"])
    print("Status:", selected_booking["payment_status"])
    print("Payment Date:", selected_booking["payment_date"])

    # ----------------------------------------------------------------------
def track_parcel(self, customer_id):
    bookings = Database.load_bookings()

    print("\n===== Track Parcel =====")

    booking_id = input("Enter Booking ID: ")

    found = False

    for booking in bookings:
        if (
            booking["booking_id"] == booking_id
            and booking["customer_id"] == customer_id
        ):
            found = True

            print("\n===== Parcel Status =====")
            print("Booking ID:", booking["booking_id"])
            print("Receiver:", booking["receiver_name"])
            print("Pickup:", booking["pickup_location"])
            print("Destination:", booking["drop_location"])
            print("Status:", booking["status"])
            print("Payment Status:", booking["payment_status"])

            break

    if not found:
        print("Booking ID Not Found!")


# ----------------------------------------------------------------------
def view_my_bookings(self, customer_id):
    bookings = Database.load_bookings()

    print("\n===== View All Bookings =====")

    found = False

    for booking in bookings:
        if booking["customer_id"] == customer_id:
            found = True

            print("\n-----------------------------------")
            print("Booking ID:", booking["booking_id"])
            print("Receiver:", booking["receiver_name"])
            print("Pickup:", booking["pickup_location"])
            print("Destination:", booking["drop_location"])
            print("Amount: Rs.", booking["amount"])
            print("Payment Status:", booking["payment_status"])
            print("Parcel Status:", booking["status"])

    if not found:
        print("No Bookings Found!")


# -----------------------------------------------------------------------------
def cancel_booking(self, customer_id):
    bookings = Database.load_bookings()

    print("\n===== Cancel Booking =====")

    booking_id = input("Enter Booking ID: ")

    found = False

    for booking in bookings:
        if (
            booking["booking_id"] == booking_id
            and booking["customer_id"] == customer_id
        ):
            found = True

            if booking["status"] in [
                "Shipped",
                "Out For Delivery",
                "Delivered",
                "Cancelled"
            ]:
                print(
                    f"Booking cannot be cancelled! "
                    f"Current Status: {booking['status']}"
                )
                return

            print("\nBooking Details")
            print("Booking ID:", booking["booking_id"])
            print("Amount: Rs.", booking["amount"])
            print("Status:", booking["status"])

            confirm = input(
                "\nAre you sure you want to cancel "
                "this booking? (Y/N): "
            )

            if confirm.upper() != "Y":
                print("Cancellation Aborted!")
                return

            if booking["payment_status"] == "Paid":
                print(
                    "Refund will be processed "
                    "within 5-7 business days."
                )

            booking["status"] = "Cancelled"

            Database.save_bookings(bookings)

            print("\nBooking Cancelled Successfully!")
            print("Status:", booking["status"])

            return

    if not found:
        print("Booking ID Not Found!")


# ------------------------------------------------------------------------------
def feedback(self, customer_id):
    bookings = Database.load_bookings()

    has_delivered = False
    booking_id = None

    for booking in bookings:
        if (
            booking["customer_id"] == customer_id
            and booking["status"] == "Delivered"
        ):
            booking_id = booking["booking_id"]
            has_delivered = True
            break

    if not has_delivered:
        print(
            "Feedback can only be submitted "
            "for delivered parcels."
        )
        return

    feedbacks = Database.load_feedback()

    print("\n===== Feedback =====")

    while True:
        rating = input("Rate Our Service (1-5): ")

        if Validation.validate_rating(rating):
            break

        print("Rating must be between 1 and 5")

    while True:
        comments = input("Enter Feedback Comments: ")

        if comments.strip():
            break

        print("Feedback cannot be empty")

    feedback_id = "F" + str(
        1000 + len(feedbacks) + 1
    )

    feedback = {
        "feedback_id": feedback_id,
        "customer_id": customer_id,
        "booking_id": booking_id,
        "rating": int(rating),
        "comments": comments,
        "feedback_date": datetime.now().strftime(
            "%d-%m-%Y %H:%M:%S"
        )
    }

    feedbacks.append(feedback)

    Database.save_feedback(feedbacks)

    print("\nThank You For Your Feedback!")