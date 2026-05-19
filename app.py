import os
import pymysql
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Database Configuration
# Update these based on your MySQL setup
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_USER = os.environ.get('DB_USER', 'root')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'Rahul2006') # Empty by default in XAMPP
DB_NAME = os.environ.get('DB_NAME', 'placement_management')

UPLOAD_FOLDER = 'static/uploads/resumes'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def get_db_connection():
    try:
        connection = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

# --- Custom Filters ---
@app.template_filter('datetimeformat')
def datetimeformat(value, format='%Y-%m-%d %H:%M'):
    if value is None:
        return ""
    if isinstance(value, str):
        try:
            value = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return value
    return value.strftime(format)

# --- Routes ---

@app.route('/')
def index():
    return render_template('index.html')

# --- Student Authentication ---
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        branch = request.form['branch']
        year = request.form['year']
        semester = request.form['semester']
        cgpa = request.form['cgpa']
        skills = request.form['skills']
        
        hashed_password = generate_password_hash(password)
        
        conn = get_db_connection()
        if not conn:
            flash('Database connection failed', 'danger')
            return redirect(url_for('register'))
            
        cursor = conn.cursor()
        
        try:
            # Check if email exists
            cursor.execute('SELECT id FROM students WHERE email = %s', (email,))
            if cursor.fetchone():
                flash('Email already registered!', 'danger')
                return redirect(url_for('register'))
                
            cursor.execute('''
                INSERT INTO students (name, email, password, branch, year, semester, cgpa, skills) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ''', (name, email, hashed_password, branch, year, semester, cgpa, skills))
            conn.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash(f'An error occurred: {e}', 'danger')
        finally:
            cursor.close()
            conn.close()
            
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn = get_db_connection()
        if not conn:
            flash('Database connection failed', 'danger')
            return redirect(url_for('login'))
            
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT * FROM students WHERE email = %s', (email,))
            student = cursor.fetchone()
            
            if student and check_password_hash(student['password'], password):
                session['student_id'] = student['id']
                session['student_name'] = student['name']
                session['user_type'] = 'student'
                flash('Login successful!', 'success')
                return redirect(url_for('student_dashboard'))
            else:
                flash('Invalid email or password.', 'danger')
        except Exception as e:
            flash(f'An error occurred: {e}', 'danger')
        finally:
            cursor.close()
            conn.close()
            
    return render_template('login.html')

# --- Admin Authentication ---
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        if not conn:
            flash('Database connection failed', 'danger')
            return redirect(url_for('admin_login'))
            
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT * FROM admin WHERE username = %s', (username,))
            admin = cursor.fetchone()
            
            # Allow default admin creation if doesn't exist for demo purposes
            if not admin and username == 'admin':
                 hashed_password = generate_password_hash('admin123')
                 cursor.execute('INSERT INTO admin (username, password) VALUES (%s, %s)', ('admin', hashed_password))
                 conn.commit()
                 admin = {'id': 1, 'username': 'admin', 'password': hashed_password}
                 flash('Default admin user created (admin/admin123).', 'info')

            if admin and check_password_hash(admin['password'], password):
                session['admin_id'] = admin['id']
                session['admin_name'] = admin['username']
                session['user_type'] = 'admin'
                flash('Admin Login successful!', 'success')
                return redirect(url_for('admin_dashboard'))
            else:
                flash('Invalid username or password.', 'danger')
        except Exception as e:
            flash(f'An error occurred: {e}', 'danger')
        finally:
            cursor.close()
            conn.close()
            
    return render_template('admin_login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

# --- Dashboards ---

@app.route('/student/dashboard')
def student_dashboard():
    if session.get('user_type') != 'student':
        flash('Please login as a student.', 'warning')
        return redirect(url_for('login'))
        
    student_id = session['student_id']
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get student details
    cursor.execute('SELECT * FROM students WHERE id = %s', (student_id,))
    student = cursor.fetchone()
    
    # Get all companies
    cursor.execute('SELECT * FROM companies')
    all_companies = cursor.fetchall()
    
    # Get student's applications
    cursor.execute('''
        SELECT a.id as application_id, c.company_name, c.role, a.status, a.applied_at 
        FROM applications a 
        JOIN companies c ON a.company_id = c.id 
        WHERE a.student_id = %s
        ORDER BY a.applied_at DESC
    ''', (student_id,))
    applications = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('student_dashboard.html', student=student, companies=all_companies, applications=applications)

@app.route('/admin/dashboard')
def admin_dashboard():
    if session.get('user_type') != 'admin':
        flash('Please login as an admin.', 'warning')
        return redirect(url_for('admin_login'))
        
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get counts
    cursor.execute('SELECT COUNT(*) as count FROM students')
    students_count = cursor.fetchone()['count']
    
    cursor.execute('SELECT COUNT(*) as count FROM companies')
    companies_count = cursor.fetchone()['count']
    
    cursor.execute('SELECT COUNT(*) as count FROM applications')
    applications_count = cursor.fetchone()['count']
    
    cursor.execute('SELECT COUNT(*) as count FROM applications WHERE status = "Selected"')
    placed_count = cursor.fetchone()['count']
    
    # Get branch wise stats for chart
    cursor.execute('SELECT branch, COUNT(*) as count FROM students GROUP BY branch')
    branch_stats = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('admin_dashboard.html', 
                          students_count=students_count,
                          companies_count=companies_count,
                          applications_count=applications_count,
                          placed_count=placed_count,
                          branch_stats=branch_stats)

# --- Student Actions ---

@app.route('/apply/<int:company_id>', methods=['POST'])
def apply_job(company_id):
    if session.get('user_type') != 'student':
        return jsonify({'success': False, 'message': 'Not logged in as student'})
        
    student_id = session['student_id']
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Check eligibility
        cursor.execute('SELECT cgpa FROM students WHERE id = %s', (student_id,))
        student_cgpa = cursor.fetchone()['cgpa']
        
        cursor.execute('SELECT min_cgpa FROM companies WHERE id = %s', (company_id,))
        company = cursor.fetchone()
        
        if not company:
            return jsonify({'success': False, 'message': 'Company not found'})
            
        if float(student_cgpa) < float(company['min_cgpa']):
             return jsonify({'success': False, 'message': 'You do not meet the minimum CGPA requirement.'})
             
        # Check if already applied
        cursor.execute('SELECT * FROM applications WHERE student_id = %s AND company_id = %s', (student_id, company_id))
        if cursor.fetchone():
             return jsonify({'success': False, 'message': 'You have already applied to this company.'})
        
        # Insert application
        cursor.execute('INSERT INTO applications (student_id, company_id) VALUES (%s, %s)', (student_id, company_id))
        conn.commit()
        return jsonify({'success': True, 'message': 'Successfully applied!'})
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})
    finally:
        cursor.close()
        conn.close()

@app.route('/upload_resume', methods=['POST'])
def upload_resume():
    if session.get('user_type') != 'student':
        flash('Please login as student', 'danger')
        return redirect(url_for('login'))
        
    if 'resume' not in request.files:
        flash('No file part', 'danger')
        return redirect(url_for('student_dashboard'))
        
    file = request.files['resume']
    if file.filename == '':
        flash('No selected file', 'danger')
        return redirect(url_for('student_dashboard'))
        
    if file and file.filename.endswith('.pdf'):
        filename = secure_filename(f"resume_student_{session['student_id']}.pdf")
        file.path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file.path)
        
        # Update db
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE students SET resume_path = %s WHERE id = %s', (filename, session['student_id']))
        conn.commit()
        cursor.close()
        conn.close()
        
        flash('Resume uploaded successfully', 'success')
    else:
        flash('Only PDF files are allowed', 'danger')
        
    return redirect(url_for('student_dashboard'))

# --- Admin Actions ---

@app.route('/admin/companies', methods=['GET', 'POST'])
def manage_companies():
    if session.get('user_type') != 'admin':
        return redirect(url_for('admin_login'))
        
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        name = request.form['company_name']
        role = request.form['role']
        min_cgpa = request.form['min_cgpa']
        package = request.form['package']
        
        cursor.execute('''
            INSERT INTO companies (company_name, role, min_cgpa, package) 
            VALUES (%s, %s, %s, %s)
        ''', (name, role, min_cgpa, package))
        conn.commit()
        flash('Company added successfully!', 'success')
        
    cursor.execute('SELECT * FROM companies')
    companies = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('admin_companies.html', companies=companies)

@app.route('/admin/companies/delete/<int:company_id>', methods=['POST'])
def delete_company(company_id):
    if session.get('user_type') != 'admin':
        return redirect(url_for('admin_login'))
        
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('DELETE FROM companies WHERE id = %s', (company_id,))
        conn.commit()
        flash('Company deleted successfully.', 'success')
    except Exception as e:
        flash(f'An error occurred: {e}', 'danger')
    finally:
        cursor.close()
        conn.close()
        
    return redirect(url_for('manage_companies'))

@app.route('/admin/applications')
def manage_applications():
    if session.get('user_type') != 'admin':
        return redirect(url_for('admin_login'))
        
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT a.id, s.name as student_name, s.branch, s.cgpa, c.company_name, c.role, a.status, a.applied_at
        FROM applications a
        JOIN students s ON a.student_id = s.id
        JOIN companies c ON a.company_id = c.id
        ORDER BY a.applied_at DESC
    ''')
    applications = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('admin_applications.html', applications=applications)

@app.route('/admin/applications/update/<int:app_id>', methods=['POST'])
def update_application_status(app_id):
    if session.get('user_type') != 'admin':
        return jsonify({'success': False, 'message': 'Unauthorized'})
        
    new_status = request.form['status']
    if new_status not in ['Applied', 'Selected', 'Rejected']:
        return jsonify({'success': False, 'message': 'Invalid status'})
        
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('UPDATE applications SET status = %s WHERE id = %s', (new_status, app_id))
        conn.commit()
        return jsonify({'success': True, 'message': 'Status updated'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
