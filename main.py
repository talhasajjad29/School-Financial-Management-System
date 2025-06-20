import csv
from datetime import datetime
import os

def admin_login():
        print(" Admin Login")
        username = input("Enter username: ")
        password = input("Enter password: ")

        if username == "admin" and password == "1234":
            return True
        else:
            print("Invalid credentials.")
            return False

# Create CSV files if they don't exist
def setup_files():
    if not os.path.exists("students.csv"):
        with open("students.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Name", "Class", "Contact", "Monthly Fee"])

    if not os.path.exists("fees.csv"):
        with open("fees.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Name", "Month", "Amount", "Date"])

# 1. Add a new student
def add_student():
    name = input("Enter Student Name: ")
    student_class = input("Enter Class: ")
    contact = input("Enter Contact Number: ")
    monthly_fee = input("Enter Monthly Fee: ")

    with open("students.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([name, student_class, contact, monthly_fee])

    print(f" Student '{name}' added successfully.")

# 2. View all students
def view_students():
    print("\nRegistered Students:")
    with open("students.csv", "r") as file:
        reader = csv.reader(file)
        next(reader)  # skip header
        for row in reader:
            print(f"Name: {row[0]}, Class: {row[1]}, Contact: {row[2]}, Fee: {row[3]}")

# 3. Submit fee
def submit_fee():
    name = input("Enter Student Name: ")
    month = input("Enter Month (e.g. June): ")
    amount = float(input("Enter Amount Submitted: "))
    date = datetime.now().strftime("%Y-%m-%d")

    with open("fees.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([name, month, amount, date])

    print("Fee submitted and recorded.")

# 4. View fee records
def view_fee_records():
    print("\nFee Records:")
    with open("fees.csv", "r") as file:
        reader = csv.reader(file)
        next(reader)  # skip header
        for row in reader:
            print(f"Name: {row[0]}, Month: {row[1]}, Amount: {row[2]}, Date: {row[3]}")

def calculate_pending_fees():
    from datetime import datetime

    print("\nPending Fee Report (Till Current Month):\n")

    current_month = datetime.now().month  # e.g., June = 6

    students = {}  # Step 1: empty dictionary

    # Step 2: Read all students from students.csv
    with open("students.csv", "r") as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        for row in reader:
            name = row[0]                 # Name
            monthly_fee = float(row[3])   # Monthly Fee
            students[name] = {"monthly_fee": monthly_fee, "total_paid": 0.0}

    # Step 3: Read fee records and add to total_paid
    with open("fees.csv", "r") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            name = row[0]                 # Name
            amount = float(row[2])        # Amount Paid
            if name in students:
                students[name]["total_paid"] += amount

    # Step 4: Show pending fees
    for name, data in students.items():
        expected = data["monthly_fee"] * current_month
        pending = expected - data["total_paid"]
        status = "Clear" if pending <= 0 else "Pending"
        print(f"{name} | Paid: {data['total_paid']} | Expected (till {current_month} months): {expected} | Pending: {pending:.2f} | {status}")

def generate_fee_slip():
    name = input("Enter Student Name: ")

    # STEP 1: Find student
    student_found = False
    with open("students.csv", "r") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if row[0].lower() == name.lower():
                student_found = True
                student_name = row[0]
                student_class = row[1]
                monthly_fee = float(row[3])
                break

    if not student_found:
        print("Student not found.")
        return

    # STEP 2: Calculate total paid and get last payment
    total_paid = 0.0
    last_payment = None
    with open("fees.csv", "r") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if row[0].lower() == name.lower():
                total_paid += float(row[2])
                last_payment = row  # latest row will stay last

    # STEP 3: Calculate expected till present month
    current_month = datetime.now().month  # Jan=1, Jun=6, etc.
    expected_fee = monthly_fee * current_month
    pending = expected_fee - total_paid
    pending = max(0, pending)  # never negative returns higher value due to max built in function

    # STEP 4: Generate slip number and display
    slip_number = f"{name[:2].upper()}{datetime.now().strftime('%Y%m%d%H%M%S')}"

    print("\nFee Slip")
    print("----------------------------")
    print(f"Slip No     : {slip_number}")
    print(f"Name        : {student_name}")
    print(f"Class       : {student_class}")
    print(f"Monthly Fee : {monthly_fee}")
    print(f"Expected Fee Till Now: {expected_fee}")
    print(f"Total Paid  : {total_paid}")
    print(f"Pending     : {pending}")
    if last_payment:
        print(f"Last Paid   : {last_payment[2]} on {last_payment[3]}")
    else:
        print("Last Paid   : No payment yet.")
    print("----------------------------")

def monthly_fee_report():
    month_input = input("Enter Month Name (e.g. June): ").strip().lower()
    total_collected = 0.0
    records_found = False

    print(f"\nFee Report for {month_input.capitalize()}:\n")
    print(f"{'Name':<15} {'Amount':<10} {'Date'}")
    print("-" * 40)

    with open("fees.csv", "r") as f:
        reader = csv.reader(f)
        next(reader)  # Skip header

        for row in reader:
            name, month, amount, date = row
            if month.lower() == month_input:
                print(f"{name:<15} {amount:<10} {date}")
                total_collected += float(amount)
                records_found = True

    if not records_found:
        print("No fee records found for this month.")
    else:
        print("-" * 40)
        print(f"Total Collected in {month_input.capitalize()}: {total_collected}")


# Main menu
def main():
    setup_files()

    attempts = 3
    while attempts > 0:
        if admin_login():
            print("Login successful!")
            break
        else:
            attempts -= 1
            print(f"Attempts left: {attempts}")

    if attempts == 0:
        print("Too many failed attempts. Exiting...")
        return

    while True:
        print("\n===== Student Fee Management System =====")
        print("1. Add Student")
        print("2. View Students")
        print("3. Submit Fee")
        print("4. View Fee Records")
        print("5. Calculate Pending Fees")
        print("6. Generate Fee Slip")
        print("7. Monthly Fee Report")
        print("8. Exit")
        choice = input("Enter your choice (1-8): ")

        if choice == "1":
            add_student()
        elif choice == "2":
            view_students()
        elif choice == "3":
            submit_fee()
        elif choice == "4":
            view_fee_records()
        elif choice == "5":
            calculate_pending_fees()
        elif choice == "6":
            generate_fee_slip()
        elif choice == "7":
            monthly_fee_report()
        elif choice == "8":
            print("Exiting system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


# Run the program
if __name__ == "__main__":
    main()
