import validation
from database import Database
import re
from validation import Validation
from booking import Booking


class Customer:

    def __init__(self):
        self.current_customer = None

    def register(self):
        customers = Database.load_customers()

        print("\n===== Customer Registration =====")

        # Name
        while True:
            name = input("Enter Name: ").strip()
            if name and name.isalpha():
                break
            print("Invalid Name!")

        # Email
        while True:
            email = input("Enter Email: ")

            if not Validation.validate_email(email):
                print("Invalid Email Format!")
                continue

            if Validation.email_exists(email, customers):
                print("Email Already Exists!")
                continue

            break

        # Mobile
        while True:
            mobile = input("Enter Mobile Number: ")

            if not Validation.validate_mobile(mobile):
                print(
                    "Mobile number must be 10 digits and start with 6, 7, 8, or 9"
                )
                continue

            if Validation.mobile_exists(mobile, customers):
                print("Mobile Number Already Exists!")
                continue

            break

        # Address
        address = input("Enter Address: ")

        # Password
        while True:
            password = input("Enter Password: ")

            if Validation.validate_password(password):
                break

            print("\nPassword must contain:")
            print("- Minimum 8 characters")
            print("- At least 1 uppercase letter")
            print("- At least 1 lowercase letter")
            print("- At least 1 digit")
            print("- At least 1 special character")

        customer_id = "C" + str(1000 + len(customers) + 1)

        customer = {
            "customer_id": customer_id,
            "name": name,
            "email": email,
            "mobile": mobile,
            "address": address,
            "password": password
        }

        customers.append(customer)
        Database.save_customers(customers)

        print("\nRegistration Successful!")
        print(f"Customer ID: {customer_id}")

    def login(self):
        customers = Database.load_customers()

        print("\n===== Customer Login =====")

        attempt = 3

        while attempt > 0:
            customer_id = input("Enter Customer ID: ")
            password = input("Enter Password: ")

            for customer in customers:
                if (
                    customer["customer_id"] == customer_id
                    and customer["password"] == password
                ):
                    self.current_customer = customer
                    print("\nLogin Successful!")
                    return customer

            attempt -= 1
            print("Invalid Customer ID or Password!")
            print("Attempts Left:", attempt)

        print("Account Locked!")
        return None

    def customer_menu(self):
        bookings = Booking()

        while True:
            print("\n===== Customer Menu =====")
            print("1. Book Parcel")
            print("2. Pay Parcel")
            print("3. Track Parcel")
            print("4. View My Bookings")
            print("5. Cancel Booking")
            print("6. Feedback")
            print("7. Logout")

            choice = input("Enter Choice: ")

            if choice == "1":
                bookings.book_parcel(
                    self.current_customer["customer_id"]
                )

            elif choice == "2":
                bookings.pay_parcel(
                    self.current_customer["customer_id"]
                )

            elif choice == "3":
                bookings.track_parcel(
                    self.current_customer["customer_id"]
                )

            elif choice == "4":
                bookings.view_my_bookings(
                    self.current_customer["customer_id"]
                )

            elif choice == "5":
                bookings.cancel_booking(
                    self.current_customer["customer_id"]
                )

            elif choice == "6":
                bookings.feedback(
                    self.current_customer["customer_id"]
                )

            elif choice == "7":
                print("Logged Out Successfully")
                break

            else:
                print("Feature Coming Soon...")