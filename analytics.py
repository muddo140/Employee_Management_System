import pandas as pd

from database import create_connection, get_all_employees


def get_employee_dataframe():
    connection = create_connection()

    if connection is None:
        return pd.DataFrame()

    employees = get_all_employees(connection)

    columns = [
        "Employee_ID",
        "First_Name",
        "Last_Name",
        "Email",
        "Phone",
        "Department",
        "Salary",
        "Joining_Date"
    ]

    df = pd.DataFrame(employees, columns=columns)
    df["Salary"] = pd.to_numeric(df["Salary"], errors="coerce")

    connection.close()

    return df


def show_employee_statistics(df):
    if df.empty:
        print("No employee data available.")
        return

    print("\nEmployee Statistics:")
    print("Total Employees:", len(df))
    print("Average Salary:", df["Salary"].mean())
    print("Highest Salary:", df["Salary"].max())
    print("Lowest Salary:", df["Salary"].min())


def show_department_analysis(df):
    if df.empty:
        return

    print("\nEmployees per Department:")
    print(df["Department"].value_counts())

    print("\nAverage Salary by Department:")
    print(
        df.groupby("Department")["Salary"].mean()
    )
def export_analytics_report(df):
    if df.empty:
        print("No employee data available to export.")
        return

    department_summary = (
        df.groupby("Department")["Salary"]
        .agg(["count", "mean", "min", "max"])
        .reset_index()
    )

    top_salaries = df.nlargest(3, "Salary")

    with pd.ExcelWriter("employee_analytics_report.xlsx") as writer:
        df.to_excel(
            writer,
            sheet_name="Employees",
            index=False
        )

        department_summary.to_excel(
            writer,
            sheet_name="Department Summary",
            index=False
        )

        top_salaries.to_excel(
            writer,
            sheet_name="Top Salaries",
            index=False
        )

    print("\nAnalytics report exported successfully.") 


if __name__ == "__main__":
    df = get_employee_dataframe()

    print("\nEmployee Data from MySQL:")
    print(df)

    show_employee_statistics(df)
    show_department_analysis(df)
    export_analytics_report(df)