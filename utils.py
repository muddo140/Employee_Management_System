from datetime import datetime
import re



def get_integer_input(message):
    # Get a valid integer from the user
    while True:
        try:
            return int(input(message))
        except ValueError:
            print("Please enter a valid number.")


def get_float_input(message):
    # Get a positive decimal number from the user
    while True:
        try:
            value = float(input(message))

            if value > 0:
                return value

            print("Salary must be greater than 0.")

        except ValueError:
            print("Please enter a valid number.")

def get_text_input(message):
    # Get non-empty text from the user
    while True:
        value = input(message).strip()

        if value:
            return value

        print("This field cannot be empty.")
def get_name_input(message):
    while True:
        name = input(message).strip()

        if re.fullmatch(r"[A-Za-z]+(?:[ '-][A-Za-z]+)*", name):
            return name

        print("Name can contain only letters, spaces, hyphens, or apostrophes.")
def get_department_input(message):
    while True:
        department = input(message).strip()

        if re.fullmatch(r"[A-Za-z]+(?:[ &-][A-Za-z]+)*", department):
            return department

        print("Department can contain only letters, spaces, '&', or hyphens.")

def get_email_input(message):
    # Get a basic valid email address
    while True:
        email = input(message).strip()

        if "@" in email and "." in email.split("@")[-1]:
            return email

        print("Please enter a valid email address.")

def get_phone_input(message):
    # Get a valid 10-digit phone number
    while True:
        phone = input(message).strip()

        if phone.isdigit() and len(phone) == 10:
            return phone

        print("Please enter a valid 10-digit phone number.")



def get_date_input(message):
    # Get a valid date in YYYY-MM-DD format
    while True:
        date_input = input(message).strip()

        try:
            datetime.strptime(date_input, "%Y-%m-%d")
            return date_input
        except ValueError:
            print("Please enter a valid date in YYYY-MM-DD format.")

def get_confirmation(message):
    # Get a yes or no confirmation from the user
    while True:
        choice = input(message).strip().lower()

        if choice in ("y", "n"):
            return choice

        print("Please enter y or n.")
        
def is_valid_name(name):
    return bool(
        re.fullmatch(r"[A-Za-z]+(?:[ '-][A-Za-z]+)*", name)
    )


def is_valid_department(department):
    return bool(
        re.fullmatch(r"[A-Za-z]+(?:[ &-][A-Za-z]+)*", department)
    )


def is_valid_email(email):
    return "@" in email and "." in email.split("@")[-1]


def is_valid_phone(phone):
    return phone.isdigit() and len(phone) == 10