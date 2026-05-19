1. Full Project Generator Prompt
Create a complete Placement Management System project using:
- Frontend: HTML, CSS, JavaScript
- Backend: Python Flask
- Database: MySQL

The system should include:
- Student registration and login using email and password
- Admin login system
- Student dashboard to view companies and apply for jobs
- Admin dashboard to add companies and manage applications
- Eligibility check: only students with required CGPA can apply
- Application status tracking (Applied, Selected, Rejected)
- Branch-wise student data handling

Provide:
- Complete folder structure
- Backend code (Flask)
- Frontend templates (HTML + CSS)
- MySQL database connection code
- Sample data

2. Database Design Prompt
Design a MySQL database for a Placement Management System with the following tables:
- Students (id, name, email, password, branch, year, semester, cgpa, skills)
- Companies (id, company_name, role, min_cgpa, package)
- Applications (id, student_id, company_id, status)
- Admin (id, username, password)

Include:
- Primary keys
- Foreign key relationships
- Proper data types
- Insert sample records

3. Backend (Flask) Prompt
Create a Flask backend for a Placement Management System with:
- MySQL database connection
- Student registration and login APIs
- Admin login API
- Route to add companies
- Route to fetch companies
- Route for students to apply for a job
- Route to view applications
- Eligibility check based on CGPA before applying

Use clean code structure and include comments

4. Frontend UI Prompt
Create a responsive frontend UI for a Placement Management System using HTML, CSS, and JavaScript with:

Pages:
- Student login and registration page
- Student dashboard
- Company listing page with apply button
- Application status page
- Admin login page
- Admin dashboard

Design should be modern with clean layout, cards, buttons, and navigation bar

5. Authentication System Prompt
Create a login and registration system in Flask with:
- Password hashing
- Session management
- Separate login for students and admin
- Validation for email and password

Connect it with MySQL database

6. CRUD Operations Prompt
Write Flask APIs to perform CRUD operations for:
- Students
- Companies
- Applications

Include:
- Insert
- Update
- Delete
- Fetch data

Connect all operations with MySQL

7. Dashboard & Data Visualization Prompt
Create a dashboard for Placement Management System showing:
- Number of students per branch
- Number of placed students
- Company-wise selections

Use:
- Chart.js (frontend) OR
- Python Matplotlib / Plotly (backend)

Include sample data visualization

8. ER Diagram Prompt
Create an ER diagram for a Placement Management System showing:
- Students
- Companies
- Applications
- Admin

Include:
- Relationships
- Primary keys
- Foreign keys
- Proper labeling

9. Deployment Prompt
Explain how to deploy a Flask + MySQL Placement Management System project online:

- Backend hosting options
- Database hosting
- Frontend hosting
- Step-by-step deployment guide

10. Advanced Features Prompt
Enhance the Placement Management System with:
- Resume upload feature
- Email notifications for application status
- Auto eligibility filtering
- Admin analytics dashboard

Provide implementation approach and code snippets