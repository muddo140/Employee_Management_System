import streamlit as st
from analytics import (
    get_employee_dataframe,
    export_analytics_report
)
from database import (
    create_connection,
    add_employee,
    email_exists,
    phone_exists,
    get_employee_by_id,
    update_salary,
    delete_employee
)

from employee import Employee

from utils import (
    is_valid_name,
    is_valid_department,
    is_valid_email,
    is_valid_phone
)


st.set_page_config(
    page_title="Employee Management System",
    page_icon="👨‍💼",
    layout="wide"
)
st.title("Employee Management System")
st.caption("Manage employees, salaries, analytics, and reports")

st.sidebar.title("Employee Management System")
st.sidebar.caption("Management Dashboard")

st.sidebar.divider()

menu = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Add Employee",
        "View Employees",
        "Search Employee",
        "Update Salary",
        "Delete Employee",
        "Analytics",
        "Export Report"
    ]
)

st.sidebar.divider()

st.sidebar.caption("Employee Management System v1.0")


if menu == "Dashboard":
    st.header("Dashboard")

    df = get_employee_dataframe()

    if not df.empty:
        total_employees = len(df)
        average_salary = df["Salary"].mean()
        highest_salary = df["Salary"].max()
        lowest_salary = df["Salary"].min()

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Total Employees", total_employees)
        col2.metric("Average Salary", f"₹{average_salary:,.2f}")
        col3.metric("Highest Salary", f"₹{highest_salary:,.2f}")
        col4.metric("Lowest Salary", f"₹{lowest_salary:,.2f}")

        st.divider()

        st.subheader("Recent Employees")

        recent_employees = (
            df.sort_values("Employee_ID", ascending=False)
            .head(5)
        )

        recent_employees = recent_employees[
            [
                "Employee_ID",
                "First_Name",
                "Last_Name",
                "Department",
                "Salary",
                "Joining_Date"
            ]
        ]

        st.dataframe(
            recent_employees,
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info("No employee data available.")

elif menu == "Add Employee":
    st.header("Add Employee")

    with st.form("add_employee_form"):
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone Number")
        department = st.text_input("Department")

        salary = st.number_input(
            "Salary",
            min_value=1.0,
            step=1000.0
        )

        joining_date = st.date_input("Joining Date")

        submitted = st.form_submit_button("Add Employee")

    if submitted:
        first_name = first_name.strip()
        last_name = last_name.strip()
        email = email.strip()
        phone = phone.strip()
        department = department.strip()

        if not is_valid_name(first_name):
            st.error("Please enter a valid first name.")

        elif not is_valid_name(last_name):
            st.error("Please enter a valid last name.")

        elif not is_valid_email(email):
            st.error("Please enter a valid email address.")

        elif not is_valid_phone(phone):
            st.error("Phone number must contain exactly 10 digits.")

        elif not is_valid_department(department):
            st.error("Please enter a valid department name.")

        else:
            connection = create_connection()

            if connection is None:
                st.error("Unable to connect to the database.")

            else:
                try:
                    if email_exists(connection, email):
                        st.error("This email is already registered.")

                    elif phone_exists(connection, phone):
                        st.error("This phone number is already registered.")

                    else:
                        employee = Employee(
                            None,
                            first_name,
                            last_name,
                            email,
                            phone,
                            department,
                            salary,
                            joining_date.strftime("%Y-%m-%d")
                        )

                        employee_id = add_employee(
                            connection,
                            employee
                        )

                        if employee_id is not None:
                            st.success(
                                f"Employee added successfully! "
                                f"Employee ID: {employee_id}"
                            )
                        else:
                            st.error("Employee could not be added.")

                finally:
                    connection.close()

elif menu == "View Employees":
    st.header("View Employees")

    df = get_employee_dataframe()

    if not df.empty:
        st.write(f"Total Employees: {len(df)}")

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info("No employees found.")

elif menu == "Search Employee":
    st.header("Search Employee")

    employee_id = st.number_input(
        "Enter Employee ID",
        min_value=1,
        step=1
    )

    if st.button("Search Employee"):
        connection = create_connection()

        if connection is None:
            st.error("Unable to connect to the database.")

        else:
            try:
                employee = get_employee_by_id(
                    connection,
                    int(employee_id)
                )

                if employee:
                    st.success("Employee found.")

                    st.write("**Employee ID:**", employee[0])
                    st.write("**First Name:**", employee[1])
                    st.write("**Last Name:**", employee[2])
                    st.write("**Email:**", employee[3])
                    st.write("**Phone:**", employee[4])
                    st.write("**Department:**", employee[5])
                    st.write("**Salary:**", employee[6])
                    st.write("**Joining Date:**", employee[7])

                else:
                    st.warning("Employee not found.")

            finally:
                connection.close()
elif menu == "Update Salary":
    st.header("Update Salary")

    employee_id = st.number_input(
        "Enter Employee ID",
        min_value=1,
        step=1,
        key="update_employee_id"
    )

    if st.button("Find Employee"):
        connection = create_connection()

        if connection is None:
            st.error("Unable to connect to the database.")

        else:
            try:
                employee = get_employee_by_id(
                    connection,
                    int(employee_id)
                )

                if employee:
                    st.session_state["update_employee"] = employee
                    st.success("Employee found.")

                else:
                    st.session_state.pop("update_employee", None)
                    st.warning("Employee not found.")

            finally:
                connection.close()

    if "update_employee" in st.session_state:
        employee = st.session_state["update_employee"]

        st.write("**Employee ID:**", employee[0])
        st.write("**Name:**", employee[1], employee[2])
        st.write("**Department:**", employee[5])
        st.write("**Current Salary:**", employee[6])

        new_salary = st.number_input(
            "Enter New Salary",
            min_value=1.0,
            step=1000.0
        )

        if st.button("Update Salary"):
            connection = create_connection()

            if connection is None:
                st.error("Unable to connect to the database.")

            else:
                try:
                    rows_updated = update_salary(
                        connection,
                        employee[0],
                        new_salary
                    )

                    if rows_updated > 0:
                        st.success("Salary updated successfully!")

                        st.session_state.pop(
                            "update_employee",
                            None
                        )

                    else:
                        st.warning("Salary could not be updated.")

                finally:
                    connection.close()

elif menu == "Delete Employee":
    st.header("Delete Employee")

    employee_id = st.number_input(
        "Enter Employee ID",
        min_value=1,
        step=1,
        key="delete_employee_id"
    )

    if st.button("Find Employee", key="find_delete_employee"):
        connection = create_connection()

        if connection is None:
            st.error("Unable to connect to the database.")

        else:
            try:
                employee = get_employee_by_id(
                    connection,
                    int(employee_id)
                )

                if employee:
                    st.session_state["delete_employee"] = employee
                    st.success("Employee found.")

                else:
                    st.session_state.pop(
                        "delete_employee",
                        None
                    )
                    st.warning("Employee not found.")

            finally:
                connection.close()

    if "delete_employee" in st.session_state:
        employee = st.session_state["delete_employee"]

        st.write("**Employee ID:**", employee[0])
        st.write("**Name:**", employee[1], employee[2])
        st.write("**Department:**", employee[5])
        st.write("**Salary:**", employee[6])

        confirm_delete = st.checkbox(
            "I confirm that I want to delete this employee."
        )

        if st.button("Delete Employee"):
            if not confirm_delete:
                st.warning(
                    "Please confirm the deletion first."
                )

            else:
                connection = create_connection()

                if connection is None:
                    st.error(
                        "Unable to connect to the database."
                    )

                else:
                    try:
                        rows_deleted = delete_employee(
                            connection,
                            employee[0]
                        )

                        if rows_deleted > 0:
                            st.success(
                                "Employee deleted successfully!"
                            )

                            st.session_state.pop(
                                "delete_employee",
                                None
                            )

                        else:
                            st.warning(
                                "Employee could not be deleted."
                            )

                    finally:
                        connection.close()

elif menu == "Analytics":
    st.header("Employee Analytics")

    df = get_employee_dataframe()

    if not df.empty:
        total_employees = len(df)
        average_salary = df["Salary"].mean()
        highest_salary = df["Salary"].max()
        lowest_salary = df["Salary"].min()

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Total Employees", total_employees)
        col2.metric("Average Salary", f"₹{average_salary:,.2f}")
        col3.metric("Highest Salary", f"₹{highest_salary:,.2f}")
        col4.metric("Lowest Salary", f"₹{lowest_salary:,.2f}")

        st.subheader("Employees by Department")

        department_count = (
            df["Department"]
            .value_counts()
        )

        st.bar_chart(department_count)

        st.subheader("Average Salary by Department")

        average_department_salary = (
            df.groupby("Department")["Salary"]
            .mean()
        )

        st.bar_chart(average_department_salary)

    else:
        st.info("No employee data available.")

elif menu == "Export Report":
    st.header("Export Analytics Report")

    st.write(
        "Generate an Excel report using the latest employee data."
    )

    if st.button("Generate Excel Report"):
        df = get_employee_dataframe()

        if df.empty:
            st.warning("No employee data available.")

        else:
            export_analytics_report(df)

            st.session_state["report_ready"] = True

            st.success(
                "Analytics report generated successfully!"
            )

    if st.session_state.get("report_ready"):
        with open(
            "employee_analytics_report.xlsx",
            "rb"
        ) as file:

            st.download_button(
                label="Download Excel Report",
                data=file.read(),
                file_name="employee_analytics_report.xlsx",
                mime=(
                    "application/vnd.openxmlformats-"
                    "officedocument.spreadsheetml.sheet"
                )
            )