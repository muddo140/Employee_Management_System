class Employee:
    def __init__(self, employee_id, first_name, last_name, email,
                 phone, department, salary, joining_date):

        # Store employee ID
        self.employee_id = employee_id

        # Store employee first name
        self.first_name = first_name

        # Store employee last name
        self.last_name = last_name

        # Store employee email
        self.email = email

        # Store employee phone number
        self.phone = phone

        # Store employee department
        self.department = department

        # Store employee salary
        self.salary = salary

        # Store employee joining date
        self.joining_date = joining_date

    def display_info(self):
        # Display all employee information
        print("Employee ID:", self.employee_id)
        print("Name:", self.first_name, self.last_name)
        print("Email:", self.email)
        print("Phone:", self.phone)
        print("Department:", self.department)
        print("Salary:", self.salary)
        print("Joining Date:", self.joining_date)