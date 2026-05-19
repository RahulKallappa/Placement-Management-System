CREATE DATABASE IF NOT EXISTS placement_management;
USE placement_management;

-- Admin Table
CREATE TABLE IF NOT EXISTS admin (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

-- Students Table
CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    branch VARCHAR(50) NOT NULL,
    year INT NOT NULL,
    semester INT NOT NULL,
    cgpa DECIMAL(4, 2) NOT NULL,
    skills TEXT,
    resume_path VARCHAR(255)
);

-- Companies Table
CREATE TABLE IF NOT EXISTS companies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    company_name VARCHAR(100) NOT NULL,
    role VARCHAR(100) NOT NULL,
    min_cgpa DECIMAL(4, 2) NOT NULL,
    package VARCHAR(50) NOT NULL
);

-- Applications Table
CREATE TABLE IF NOT EXISTS applications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    company_id INT NOT NULL,
    status ENUM('Applied', 'Selected', 'Rejected') DEFAULT 'Applied',
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE
);

-- Insert sample admin (password: admin123 hashed using werkzeug - or we can just hash it in python on creation, but let's insert a raw one for now and we'll handle hash checking. Actually, let's just create an endpoint to init db)
-- Let's put a plain text password for now, or just handle hashing in the app setup.
