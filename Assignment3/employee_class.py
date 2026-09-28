# Assignment 3 - menu driven program to write class to do curd operation in database for employee table
import mysql.connector

class Employee:
    def __init__(self):
        self.con = mysql.connector.connect(
            host="localhost",
            user="root",
            password="pari1303@sql",
            database="company"
        )

        self.cursor = self.con.cursor()

    def create(self):
        eid = int(input("Enter Employee ID: "))
        name = input("Enter Name: ")
        dept = input("Enter Department: ")
        salary = float(input("Enter Salary: "))

        query = "INSERT INTO employee VALUES (%s, %s, %s, %s)"

        self.cursor.execute(query, (eid, name, dept, salary))
        self.con.commit()

        print("Employee added successfully.")

    def read(self):
        self.cursor.execute("SELECT * FROM employee")

        rows = self.cursor.fetchall()

        for row in rows:
            print(row)

    def update(self):
        eid = int(input("Enter Employee ID: "))
        salary = float(input("Enter new Salary: "))

        query = "UPDATE employee SET salary=%s WHERE id=%s"

        self.cursor.execute(query, (salary, eid))
        self.con.commit()

        print("Employee updated successfully.")

    def delete(self):
        eid = int(input("Enter Employee ID: "))

        query = "DELETE FROM employee WHERE id=%s"

        self.cursor.execute(query, (eid,))
        self.con.commit()

        print("Employee deleted successfully.")


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
