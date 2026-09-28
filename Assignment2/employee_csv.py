# Assignment 2 - menu driven program  to write a class to do curd operation in csv file for employee table

import csv

class Employee:
    def __init__(self):
        self.filename = "employee.csv"

    def create(self):
        eid = input("Enter Employee ID: ")
        name = input("Enter Name: ")
        dept = input("Enter Department: ")
        salary = input("Enter Salary: ")

        with open(self.filename, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([eid, name, dept, salary])

        print("Employee added successfully.")

    def read(self):
        try:
            with open(self.filename, "r") as file:
                reader = csv.reader(file)

                for row in reader:
                    print(row)
        except FileNotFoundError:
            print("File not found.")

    def update(self):
        eid = input("Enter Employee ID to update: ")
        rows = []

        try:
            with open(self.filename, "r") as file:
                reader = csv.reader(file)

                for row in reader:
                    if row[0] == eid:
                        row[1] = input("Enter new Name: ")
                        row[2] = input("Enter new Department: ")
                        row[3] = input("Enter new Salary: ")
                    rows.append(row)

            with open(self.filename, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerows(rows)

            print("Employee updated successfully.")

        except FileNotFoundError:
            print("File not found.")

    def delete(self):
        eid = input("Enter Employee ID to delete: ")
        rows = []

        try:
            with open(self.filename, "r") as file:
                reader = csv.reader(file)

                for row in reader:
                    if row[0] != eid:
                        rows.append(row)

            with open(self.filename, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerows(rows)

            print("Employee deleted successfully.")

        except FileNotFoundError:
            print("File not found.")


emp = Employee()

while True:
    print("\n--- Employee Menu ---")
    print("1. Create")
    print("2. Read")
    print("3. Update")
    print("4. Delete")
    print("5. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        emp.create()
    elif choice == "2":
        emp.read()
    elif choice == "3":
        emp.update()
    elif choice == "4":
        emp.delete()
    elif choice == "5":
        print("Program ended.")
        break
    else:
        print("Invalid choice.")
