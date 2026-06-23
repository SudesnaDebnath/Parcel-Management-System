from customer import Customer
from officer import Officer

customer = Customer()
officer = Officer()

while True:
    print("\n===== Parcel Management System =====")
    print("1. Customer Registration")
    print("2. Customer Login")
    print("3. Officer Login")
    print("4. Exit")

    choice = input("Enter Choice: ")

    if choice == "1":
        customer.register()

    elif choice == "2":
        user = customer.login()
        if user:
            print("Welcome", user["name"])
            customer.customer_menu()

    elif choice == "3":
        user = officer.login()
        if user:
            print("Welcome", user["name"])
            officer.officer_menu()

    elif choice == "4":
        print("Thank You")
        break

    else:
        print("Invalid Choice")