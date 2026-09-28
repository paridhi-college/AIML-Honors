# Assignment 4 - menu driven program to do curd operation in database for employee table
import mysql.connector

con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="pari1303@sql",
    database="company"
)

cursor = con.cursor()

while True:

    print("\n--- Employee Menu ---")
    print("1. Create")
    print("2. Read")
    print("3. Update")
    print("4. Delete")
    print("5. Exit")

    choice = input("Enter choice: ")

    if choice == "1":

        eid = int(input("Enter Employee ID: "))
        name = input("Enter Name: ")
        dept = input("Enter Department: ")
        salary = float(input("Enter Salary: "))

        query = "INSERT INTO employee VALUES (%s, %s, %s, %s)"

        cursor.execute(query, (eid, name, dept, salary))
        con.commit()

        print("Employee added successfully.")

    elif choice == "2":

        cursor.execute("SELECT * FROM employee")

        rows = cursor.fetchall()

        for row in rows:
            print(row)

    elif choice == "3":

        eid = int(input("Enter Employee ID: "))
        salary = float(input("Enter new Salary: "))

        query = "UPDATE employee SET salary=%s WHERE id=%s"

        cursor.execute(query, (salary, eid))
        con.commit()

        print("Employee updated successfully.")

    elif choice == "4":

        eid = int(input("Enter Employee ID: "))

        query = "DELETE FROM employee WHERE id=%s"

        cursor.execute(query, (eid,))
        con.commit()

        print("Employee deleted successfully.")

    elif choice == "5":

        print("Program ended.")
        break

    else:
        print("Invalid choice.")
