# Import database functions
from database import (
    create_connection,
    add_employee,
    get_all_employees,
    get_employee_count,
    get_employee_by_id,
    email_exists,
    phone_exists,
    update_salary,
    delete_employee
)
# Import Employee class
from employee import Employee
from utils import (
    get_integer_input,
    get_float_input,
    get_text_input,
    get_email_input,
    get_phone_input,
    get_date_input,
    get_confirmation,
    get_name_input,
    get_department_input
)
from analytics import (
    get_employee_dataframe,
    show_employee_statistics,
    show_department_analysis,
    export_analytics_report
)


# Create a connection with MySQL
connection = create_connection()

# Check whether the database connection was successful
if connection is None:
    print("Unable to start Employee Management System.")
    print("Please check your MySQL connection.")
    exit()


# Display the main menu
def show_menu():
    print("\n========== Employee Management System ==========")
    print("1. Add Employee")
    print("2. View All Employees")
    print("3. Search Employee")
    print("4. Update Salary")
    print("5. Delete Employee")
    print("6. View Analytics")
    print("7. Export Analytics Report")
    print("8. Exit")


# Keep showing the menu until the user chooses Exit
while True:

    show_menu()

    choice = input("Enter your choice: ")


    # Option 1: Add Employee
    if choice == "1":

        first_name = get_name_input("Enter First Name: ")
        last_name = get_name_input("Enter Last Name: ")

        while True:

            email = get_email_input("Enter Email: ")

            if email_exists(connection, email):
                print("This email is already registered. Please enter another email.")
            else:
                break
        while True:

            phone = get_phone_input("Enter Phone: ")

            if phone_exists(connection, phone):
                print("This phone number is already registered. Please enter another phone number.")
            else:
                break

        department = get_department_input("Enter Department: ")

        salary = get_float_input("Enter Salary: ")

        joining_date = get_date_input(
            "Enter Joining Date (YYYY-MM-DD): "
        )

        employee = Employee(
            None,
            first_name,
            last_name,
            email,
            phone,
            department,
            salary,
            joining_date
        )

        # Add the employee to MySQL
        employee_id = add_employee(connection, employee)

        if employee_id is not None:
            print("Employee added successfully!")
            print("Employee ID:", employee_id)
        else:
            print("Employee could not be added.")

    # Option 2: View All Employees
    elif choice == "2":

        employees = get_all_employees(connection)

        print("Total Employees:", get_employee_count(connection))

        if employees:

            for row in employees:

                employee = Employee(
                    row[0],
                    row[1],
                    row[2],
                    row[3],
                    row[4],
                    row[5],
                    row[6],
                    row[7]
                )

                employee.display_info()

                print("--------------------")

        else:
            print("No employees found.")


    # Option 3: Search Employee
    elif choice == "3":

        while True:

            employee_id = get_integer_input("Enter Employee ID: ")

            row = get_employee_by_id(connection, employee_id)

            if row:

                employee = Employee(
                    row[0],
                    row[1],
                    row[2],
                    row[3],
                    row[4],
                    row[5],
                    row[6],
                    row[7]
                )

                employee.display_info()

                break

            else:
                print("Employee not found. Please try again.")

    # Option 4: Update Salary
    elif choice == "4":

        employee_id = get_integer_input("Enter Employee ID: ")

        # Check whether the employee exists
        employee = get_employee_by_id(connection, employee_id)

        if employee:

            new_salary = get_float_input("Enter New Salary: ")

            rows_updated = update_salary(
                connection,
                employee_id,
                new_salary
            )

            if rows_updated > 0:
                print("Salary updated successfully!")

        else:
            print("Employee not found.")


    # Option 5: Delete Employee
    elif choice == "5":

        employee_id = get_integer_input("Enter Employee ID: ")

        # Check whether the employee exists
        employee = get_employee_by_id(connection, employee_id)

        if employee:

            confirmation = get_confirmation(
                "Are you sure you want to delete this employee? (y/n): "
            )

            if confirmation == "y":

                rows_deleted = delete_employee(
                    connection,
                    employee_id
                )

                if rows_deleted > 0:
                    print("Employee deleted successfully!")

            else:
                print("Delete operation cancelled.")

        else:
            print("Employee not found.")


    # Option 6: Exit
    elif choice == "6":

        df = get_employee_dataframe()

        print("\nEmployee Analytics:")

        if not df.empty:
            print("\nEmployee Data:")
            print(df)

            show_employee_statistics(df)
            show_department_analysis(df)

        else:
            print("No employee data available.")

    elif choice == "7":

        df = get_employee_dataframe()

        export_analytics_report(df)


    elif choice == "8":

        print("Thank you for using Employee Management System!")

        connection.close()

        break


    # Invalid choice
    else:
        print("Invalid choice. Please try again.")