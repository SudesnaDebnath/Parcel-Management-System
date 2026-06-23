from database import Database
from validation import Validation


class Officer:
    bookings = Database.load_bookings()

    def __init__(self):
        self.current_officer_id = None

    # -----------------------------------------------------------
    def login(self):
        officers = Database.load_officers()

        print("\n===== Officer Login =====")
        attempts = 3

        while attempts > 0:
            officer_id = input("Enter Officer ID: ")
            password = input("Enter Password: ")

            for officer in officers:
                if (
                    officer["officer_id"] == officer_id
                    and officer["password"] == password
                ):
                    self.current_officer_id = officer
                    print("\nLogin Successful")
                    return officer

            attempts -= 1
            print("\nInvalid Officer ID or Password")
            print("Attempts left:", attempts)

        print("Account Locked!")
        return None

    # ---------------------------------------------------------------
    def officer_menu(self):
        while True:
            print("\n===== Officer Menu =====")
            print("1. View All Bookings")
            print("2. Update Parcel Status")
            print("3. Update Pickup/Drop Date")
            print("4. Search Bookings")
            print("5. View Feedback")
            print("6. Cancel Booking")
            print("7. Logout")

            choice = input("Enter Choice: ")

            if choice == "1":
                self.view_all_bookings()

            elif choice == "2":
                self.update_parcel_status()

            elif choice == "3":
                self.update_dates()

            elif choice == "4":
                self.search_bookings()

            elif choice == "5":
                self.view_feedback()

            elif choice == "6":
                self.cancel_booking()

            elif choice == "7":
                print("Logged Out Successfully")
                break

            else:
                print("Invalid Choice!")

    # -------------------------------------------------------------
    def get_booking(self, booking_id):
        bookings = Database.load_bookings()

        for booking in bookings:
            if booking["booking_id"] == booking_id:
                return booking, bookings

        return None, bookings

    # -------------------------------------------------------------
    def display_booking(self, booking):
        print("\nBooking ID:", booking["booking_id"])
        print("Customer ID:", booking["customer_id"])
        print("Receiver:", booking["receiver_name"])
        print("Receiver Mobile:", booking["receiver_mobile"])
        print("Pickup:", booking["pickup_location"])
        print("Drop:", booking["drop_location"])
        print("Pickup Date:", booking["pickup_date"])
        print("Deliver Date:", booking["drop_date"])
        print("Amount:", booking["amount"])
        print("Payment Status:", booking["payment_status"])
        print("Status:", booking["status"])
        print("-" * 40)

    # -------------------------------------------------------------
    def view_all_bookings(self):
        bookings = Database.load_bookings()

        print("\n===== All Bookings =====")

        if not bookings:
            print("No bookings found")
            return

        for booking in bookings:
            self.display_booking(booking)

    # --------------------------------------------------------------------------
    def update_parcel_status(self):
        booking_id = input("\nEnter Booking ID: ")

        booking, bookings = self.get_booking(booking_id)

        if not booking:
            print("Booking ID not Found")
            return

        print("\nCurrent Status:", booking["status"])
        print("Current Payment Status:", booking["payment_status"])

        print("\nSelect New Status:")
        print("1. Booked")
        print("2. Shipped")
        print("3. Out of Delivery")
        print("4. Delivered")

        choice = input("Enter Choice: ")

        status_map = {
            "1": "Booked",
            "2": "Shipped",
            "3": "Out of Delivery",
            "4": "Delivered"
        }

        if choice not in status_map:
            print("Invalid Choice")
            return

        new_status = status_map[choice]

        if booking["status"] == new_status:
            print("Parcel is already in this status")
            return

        if booking["payment_status"] != "Paid" and choice in ["2", "3", "4"]:
            print("Parcel cannot be shipped before payment.")
            return

        booking["status"] = new_status
        Database.save_bookings(bookings)

        print("Status Updated Successfully")
        print("New Status:", booking["status"])

    # --------------------------------------------------------------------------
    def update_dates(self):
        booking_id = input("Enter Booking ID: ")

        booking, bookings = self.get_booking(booking_id)

        if not booking:
            print("Booking ID not Found")
            return

        if booking["status"] == "Delivered":
            print("Cannot update dates for delivered parcels.")
            return

        print("\nCurrent Pickup Date:", booking["pickup_date"])
        print("Current Deliver Date:", booking["drop_date"])

        pickup_date = input("Enter Pickup Date (DD-MM-YYYY): ")

        if not Validation.valid_pickup_date(pickup_date):
            print("Invalid Pickup Date")
            return

        drop_date = input("Enter Deliver Date (DD-MM-YYYY): ")

        if not Validation.valid_drop_date(pickup_date, drop_date):
            print("Invalid Deliver Date")
            return

        booking["pickup_date"] = pickup_date
        booking["drop_date"] = drop_date

        Database.save_bookings(bookings)

        print("\nBooking Updated Successfully")
        print("New Pickup Date:", booking["pickup_date"])
        print("New Deliver Date:", booking["drop_date"])

    # --------------------------------------------------------------------------
    def search_bookings(self):
        bookings = Database.load_bookings()

        if not bookings:
            print("No bookings found")
            return

        print("\n===== Search Bookings =====")
        print("1. Booking ID")
        print("2. Customer ID")
        print("3. Receiver Mobile")

        choice = input("Enter Choice: ")
        search_value = input("Enter Search Value: ")

        found = False

        for booking in bookings:
            if (
                (choice == "1" and booking["booking_id"] == search_value)
                or (choice == "2" and booking["customer_id"] == search_value)
                or (choice == "3" and booking["receiver_mobile"] == search_value)
            ):
                self.display_booking(booking)
                found = True

        if not found:
            print("No bookings found")

    # --------------------------------------------------------------------------
    def view_feedback(self):
        feedbacks = Database.load_feedback()

        if not feedbacks:
            print("No feedback found")
            return

        print("\n===== Customer Feedback =====")

        for feedback in feedbacks:
            print("-" * 40)
            print("Customer ID:", feedback["customer_id"])
            print("Booking ID:", feedback["booking_id"])
            print("Rating:", feedback["rating"])
            print("Feedback:", feedback["comments"])
            print("Feedback Date:", feedback["feedback_date"])
            print("-" * 40)

    # --------------------------------------------------------------------------
    def cancel_booking(self):
        booking_id = input("Enter Booking ID: ")

        booking, bookings = self.get_booking(booking_id)

        if not booking:
            print("Booking ID not Found")
            return

        self.display_booking(booking)

        if booking["status"] != "Booked":
            print(f'{booking["status"]} parcels cannot be cancelled')
            return

        confirm = input(
            "Do you want to cancel the parcel? (Y/N): "
        ).lower()

        if confirm != "y":
            print("Cancellation Aborted")
            return

        booking["status"] = "Cancelled"

        Database.save_bookings(bookings)

        print("\nBooking Cancelled Successfully")

        if booking["payment_status"] == "Paid":
            print("Refund will be processed within 5-7 business days.")