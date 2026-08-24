# Employee Management System

A Python-based Employee Management System that allows users to manage employee records through an interactive Streamlit web application.

The application uses MySQL for data storage, Pandas for employee analytics, and Streamlit for the user interface.

## Features

- Add new employees
- View all employees
- Search employee by ID
- Update employee salary
- Delete employee with confirmation
- Input validation
- Duplicate email and phone validation
- Employee analytics dashboard
- Department-wise employee analysis
- Average, highest, and lowest salary analysis
- Recent employee records
- Export analytics reports to Excel
- Download Excel reports from the web application
- Secure database credentials using environment variables

## Technologies Used

- Python
- MySQL
- Pandas
- Streamlit
- OpenPyXL
- python-dotenv

## Project Structure

Employee_Management_System/
│
├── app.py
├── main.py
├── database.py
├── employee.py
├── analytics.py
├── utils.py
├── schema.sql
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md


### Database Setup

Open MySQL Workbench and run the `schema.sql` file included in this repository.

It will automatically create:

- `employee_management` database
- `employee` table
- All required employee columns

```text
employee_management
```

Main table:

```text
employee
```

Employee fields include:

- Employee ID
- First Name
- Last Name
- Email
- Phone
- Department
- Salary
- Joining Date

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/muddo140/Employee_Management_System.git
```

### 2. Install required packages

```bash
python -m pip install -r requirements.txt
```

### 3. Create a `.env` file

Use `.env.example` as a template:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=employee_management
```

Replace the values with your own MySQL credentials.

## Run the Streamlit Application

```bash
python -m streamlit run app.py
```

The application will open in your web browser.

## Analytics

The analytics dashboard provides:

- Total employees
- Average salary
- Highest salary
- Lowest salary
- Employees by department
- Average salary by department

## Excel Reporting

The application can generate an Excel analytics report containing:

- Employees
- Department Summary
- Top Salaries

## Security

Database credentials are stored in a `.env` file.

The `.env` file is excluded from Git using `.gitignore`, so sensitive credentials are not uploaded to GitHub.
## Screenshots

### Dashboard

![Dashboard](screenshots/dashboard.png)

### Add Employee

![Add Employee](screenshots/add_employee.png)

### Analytics Dashboard

![Analytics](screenshots/analytics.png)

## Future Improvements

- Employee authentication and login
- Role-based access
- Attendance management
- Leave management
- More advanced analytics
- Cloud deployment

## Author

Mohd Mudassir