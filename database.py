import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()


def create_connection():

    try:

        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )

        return connection

    except mysql.connector.Error as error:

        print("Database connection failed.")
        print("Error:", error)

        return None

def add_employee(connection, employee):

    try:

        query = """
        INSERT INTO employee
        (first_name, last_name, email, phone, department, salary, joining_date)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        values = (
            employee.first_name,
            employee.last_name,
            employee.email,
            employee.phone,
            employee.department,
            employee.salary,
            employee.joining_date
        )

        cursor = connection.cursor()

        cursor.execute(query, values)
        connection.commit()

        employee.employee_id = cursor.lastrowid

        cursor.close()

        return employee.employee_id

    except mysql.connector.Error as error:

        print("Error while adding employee.")
        print("Error:", error)

        return None

def get_all_employees(connection):

    try:

        cursor = connection.cursor()

        cursor.execute("SELECT * FROM employee")

        employees = cursor.fetchall()

        cursor.close()

        return employees

    except mysql.connector.Error as error:

        print("Error while fetching employees.")
        print("Error:", error)

        return []

def get_employee_count(connection):

    # Count total employees in the database
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM employee")

    count = cursor.fetchone()[0]

    cursor.close()

    return count

def get_employee_by_id(connection, employee_id):

    try:

        cursor = connection.cursor()

        cursor.execute(
            "SELECT * FROM employee WHERE employee_id = %s",
            (employee_id,)
        )

        employee = cursor.fetchone()

        cursor.close()

        return employee

    except mysql.connector.Error as error:

        print("Error while searching for employee.")
        print("Error:", error)

        return None

def email_exists(connection, email):

    # Check whether the email already exists
    cursor = connection.cursor()

    cursor.execute(
        "SELECT employee_id FROM employee WHERE email = %s",
        (email,)
    )

    result = cursor.fetchone()

    cursor.close()

    return result is not None

def phone_exists(connection, phone):

    # Check whether the phone number already exists
    cursor = connection.cursor()

    cursor.execute(
        "SELECT employee_id FROM employee WHERE phone = %s",
        (phone,)
    )

    result = cursor.fetchone()

    cursor.close()

    return result is not None

def update_salary(connection, employee_id, new_salary):

    try:

        cursor = connection.cursor()

        # Update the employee salary
        cursor.execute(
            "UPDATE employee SET salary = %s WHERE employee_id = %s",
            (new_salary, employee_id)
        )

        # Save the change
        connection.commit()

        # Store the number of updated rows
        rows_updated = cursor.rowcount

        cursor.close()

        return rows_updated

    except mysql.connector.Error as error:

        # Undo the transaction if something goes wrong
        connection.rollback()

        print("Error while updating employee salary.")
        print("Error:", error)

        return 0

def delete_employee(connection, employee_id):

    try:

        cursor = connection.cursor()

        # Delete the employee
        cursor.execute(
            "DELETE FROM employee WHERE employee_id = %s",
            (employee_id,)
        )

        # Save the deletion
        connection.commit()

        # Store the number of deleted rows
        rows_deleted = cursor.rowcount

        cursor.close()

        return rows_deleted

    except mysql.connector.Error as error:

        # Undo the transaction if something goes wrong
        connection.rollback()

        print("Error while deleting employee.")
        print("Error:", error)

        return 0