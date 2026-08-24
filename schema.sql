CREATE DATABASE IF NOT EXISTS employee_management;

USE employee_management;

CREATE TABLE IF NOT EXISTS employee (
    employee_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(15),
    department VARCHAR(50),
    salary DECIMAL(10,2),
    joining_date DATE
);