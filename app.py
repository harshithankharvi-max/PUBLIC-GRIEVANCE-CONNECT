import os
import sqlite3
import json
from datetime import datetime, timedelta

# Optional geopy import – provide fallbacks if the library is unavailable
try:
    from geopy.geocoders import Nominatim
    from geopy.extra.rate_limiter import RateLimiter
except ImportError:  # pragma: no cover
    class Nominatim:
        def __init__(self, user_agent=None):
            pass
        def reverse(self, location, language='en'):
            return None
    class RateLimiter:
        def __init__(self, func, min_delay_seconds=1):
            self.func = func
        def __call__(self, *args, **kwargs):
            return self.func(*args, **kwargs)
except ImportError:  # pragma: no cover
    class Nominatim:
        def __init__(self, user_agent=None):
            pass
        def reverse(self, location, language='en'):
            return None
    class RateLimiter:
        def __init__(self, func, min_delay_seconds=1):
            self.func = func
        def __call__(self, *args, **kwargs):
            return self.func(*args, **kwargs)

from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

import json
from datetime import datetime, timedelta

from flask import Flask, g, redirect, render_template, request, session, url_for, jsonify
from dotenv import load_dotenv

from models import ComplaintClassifier, VoiceProcessor
from models.classifier import get_department_for_category, CATEGORY_DEPARTMENT_MAP, DEPARTMENTS, REJECTION_MESSAGE

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'grievanceconnect-secret-key')
app.config['DATABASE'] = os.path.join(os.path.dirname(__file__), 'database', 'grievance.db')
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'static', 'voice_notes')
app.config['IMAGE_UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

# Allowed file extensions for voice notes and images
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'flac', 'ogg', 'm4a'}
IMAGE_ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['IMAGE_UPLOAD_FOLDER'], exist_ok=True)

# Initialize AI classifier and voice processor
classifier = ComplaintClassifier()
voice_processor = VoiceProcessor(app.config['UPLOAD_FOLDER'])

# Initialize OTP Service
from services.otp_service import otp_service

# Import authorization decorators
from utils.auth_decorators import admin_required, citizen_required, login_required


def verify_user_password(stored_password, provided_password):
    """Safely verify passwords supporting both plain-text legacy and bcrypt hashes."""
    if not stored_password or not provided_password:
        return False
    if stored_password == provided_password:
        return True
    try:
        return check_password_hash(stored_password, provided_password)
    except Exception:
        return False


def allowed_file(filename, allowed_extensions=None):
    allowed_extensions = allowed_extensions or ALLOWED_EXTENSIONS
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


def save_uploaded_file(file, folder_key, allowed_extensions=None):
    if file is None or file.filename == '':
        return None

    allowed_extensions = allowed_extensions or ALLOWED_EXTENSIONS
    if not allowed_file(file.filename, allowed_extensions):
        return None

    upload_folder = app.config.get(folder_key)
    if not upload_folder:
        return None

    os.makedirs(upload_folder, exist_ok=True)
    filename = secure_filename(file.filename)
    unique_name = f"{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}_{filename}"
    file_path = os.path.join(upload_folder, unique_name)
    file.save(file_path)
    return os.path.relpath(file_path, os.path.join(app.root_path, 'static')).replace('\\', '/')


def get_db():
    if 'db' not in g:
        conn = sqlite3.connect(app.config['DATABASE'])
        conn.row_factory = sqlite3.Row
        g.db = conn
    return g.db


@app.teardown_appcontext
def close_db(error):
    if 'db' in g:
        g.db.close()


def init_db():
    db = get_db()

    # Create or ensure base tables exist
    db.execute(
        '''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            phone TEXT,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'citizen',
            phone_verified BOOLEAN DEFAULT 0
        )
        '''
    )
    
    # Create OTP Sessions table for phone-based authentication
    db.execute(
        '''
        CREATE TABLE IF NOT EXISTS otp_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone TEXT NOT NULL,
            otp_code TEXT NOT NULL,
            expires_at TEXT NOT NULL,
            attempts INTEGER DEFAULT 0,
            verified BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        '''
    )
    db.execute(
        '''
        CREATE TABLE IF NOT EXISTS complaints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            department TEXT,
            location TEXT NOT NULL,
            description TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Pending',
            priority INTEGER DEFAULT 0,
            ai_category TEXT,
            voice_note_path TEXT,
            image_path TEXT,
            language TEXT DEFAULT 'en',
            latitude REAL,
            longitude REAL,
            is_voice_complaint BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
        '''
    )
    # Ensure older databases gain new columns without rebuilding the DB file
    try:
        existing = db.execute("PRAGMA table_info('users')").fetchall()
        existing_cols = {row['name'] for row in existing}

        user_additions = []
        if 'role' not in existing_cols:
            user_additions.append("ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'citizen'")
        if 'phone_verified' not in existing_cols:
            user_additions.append("ALTER TABLE users ADD COLUMN phone_verified BOOLEAN DEFAULT 0")
        if 'department' not in existing_cols:
            user_additions.append("ALTER TABLE users ADD COLUMN department TEXT")

        for stmt in user_additions:
            try:
                db.execute(stmt)
            except Exception:
                pass
    except Exception:
        pass
    
    try:
        existing = db.execute("PRAGMA table_info('complaints')").fetchall()
        existing_cols = {row['name'] for row in existing}

        additions = []
        if 'department' not in existing_cols:
            additions.append("ALTER TABLE complaints ADD COLUMN department TEXT")
        if 'ai_category' not in existing_cols:
            additions.append("ALTER TABLE complaints ADD COLUMN ai_category TEXT")
        if 'voice_note_path' not in existing_cols:
            additions.append("ALTER TABLE complaints ADD COLUMN voice_note_path TEXT")
        if 'image_path' not in existing_cols:
            additions.append("ALTER TABLE complaints ADD COLUMN image_path TEXT")
        if 'language' not in existing_cols:
            additions.append("ALTER TABLE complaints ADD COLUMN language TEXT DEFAULT 'en'")
        if 'latitude' not in existing_cols:
            additions.append("ALTER TABLE complaints ADD COLUMN latitude REAL")
        if 'longitude' not in existing_cols:
            additions.append("ALTER TABLE complaints ADD COLUMN longitude REAL")
        if 'is_voice_complaint' not in existing_cols:
            additions.append("ALTER TABLE complaints ADD COLUMN is_voice_complaint BOOLEAN DEFAULT 0")
        if 'priority' not in existing_cols:
            additions.append("ALTER TABLE complaints ADD COLUMN priority INTEGER DEFAULT 0")
        if 'status' not in existing_cols:
            additions.append("ALTER TABLE complaints ADD COLUMN status TEXT NOT NULL DEFAULT 'Pending'")
        if 'created_at' not in existing_cols:
            additions.append("ALTER TABLE complaints ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
        if 'manual_status' not in existing_cols:
            additions.append("ALTER TABLE complaints ADD COLUMN manual_status BOOLEAN DEFAULT 0")

        for stmt in additions:
            try:
                db.execute(stmt)
            except Exception:
                pass
    except Exception:
        pass

    # Create default admin user if not exists
    existing_admin = db.execute("SELECT id FROM users WHERE email = 'admin@grievanceconnect.com'").fetchone()
    if not existing_admin:
        hashed_pwd = generate_password_hash('admin123')
        db.execute(
            '''
            INSERT INTO users (id, name, email, phone, password, role, phone_verified, department)
            VALUES (?, ?, ?, ?, ?, 'admin', 1, 'ALL')
            ''',
            (1, 'Admin User', 'admin@grievanceconnect.com', '9999999999', hashed_pwd)
        )
    else:
        db.execute("UPDATE users SET role = 'admin', department = 'ALL' WHERE email = 'admin@grievanceconnect.com'")

    # Seed the 3 Department Authority Officers
    dept_authorities = [
        ('Electricity Authority Officer', 'electricity@grievanceconnect.com', '9999900001', 'elec123', 'authority', 'ELECTRICITY'),
        ('PWD Infrastructure Officer', 'pwd@grievanceconnect.com', '9999900002', 'pwd123', 'authority', 'PWD'),
        ('Water & Sanitation Officer', 'water@grievanceconnect.com', '9999900003', 'water123', 'authority', 'WATER'),
    ]
    for name, email, phone, pwd, role, dept in dept_authorities:
        existing_auth = db.execute("SELECT id FROM users WHERE email = ?", (email,)).fetchone()
        if not existing_auth:
            h_pwd = generate_password_hash(pwd)
            db.execute(
                '''
                INSERT INTO users (name, email, phone, password, role, phone_verified, department)
                VALUES (?, ?, ?, ?, ?, 1, ?)
                ''',
                (name, email, phone, h_pwd, role, dept)
            )
        else:
            db.execute("UPDATE users SET role = ?, department = ? WHERE email = ?", (role, dept, email))

    # Create default guest citizen for skip-login / instant reporting
    existing_guest = db.execute("SELECT id FROM users WHERE email = 'guest@grievanceconnect.local'").fetchone()
    if not existing_guest:
        hashed_guest = generate_password_hash('guest123')
        db.execute(
            '''
            INSERT INTO users (name, email, phone, password, role, phone_verified)
            VALUES (?, ?, ?, ?, 'citizen', 1)
            ''',
            ('Rural Citizen', 'guest@grievanceconnect.local', '9999999000', hashed_guest)
        )
    
    db.commit()


def sync_automatic_statuses(db):
    """
    Automatic time-based status progression for college demonstration:
    - 0 to 10 minutes -> Pending
    - 10 to 20 minutes -> In Progress
    - More than 20 minutes -> Resolved
    Preserves manual override if manual_status == 1 or status is 'Rejected/Cancelled'.
    """
    try:
        now = datetime.utcnow()
        rows = db.execute(
            """
            SELECT id, created_at, status 
            FROM complaints 
            WHERE (manual_status IS NULL OR manual_status = 0)
              AND status != 'Rejected/Cancelled'
            """
        ).fetchall()
        for r in rows:
            created_str = r['created_at']
            if not created_str:
                continue
            try:
                clean_str = str(created_str).replace('T', ' ')[:19]
                dt = datetime.strptime(clean_str, '%Y-%m-%d %H:%M:%S')
                diff_mins = (now - dt).total_seconds() / 60.0
                if diff_mins < 0:
                    diff_mins = 0
                
                if diff_mins < 10:
                    new_status = 'Pending'
                elif diff_mins < 20:
                    new_status = 'In Progress'
                else:
                    new_status = 'Resolved'
                    
                if r['status'] != new_status:
                    db.execute("UPDATE complaints SET status = ? WHERE id = ?", (new_status, r['id']))
            except Exception:
                pass
        db.commit()
    except Exception:
        pass


def reverse_geocode(lat, lon):
    """Return a human-readable location name for given coordinates."""
    try:
        geolocator = Nominatim(user_agent='grievanceconnect')
        # RateLimiter to be polite to Nominatim
        reverse = RateLimiter(geolocator.reverse, min_delay_seconds=1)
        location = reverse((lat, lon), language='en')
        if location and location.raw and 'address' in location.raw:
            addr = location.raw['address']
            return addr.get('city') or addr.get('town') or addr.get('village') or addr.get('county') or addr.get('state') or location.address
    except Exception:
        pass
    return None


@app.route('/')
def index():
    return render_template('index.html')


# ==================== PHASE 1: OTP & ROLE-BASED AUTHENTICATION ====================

@app.route('/phone-login', methods=['GET', 'POST'])
def phone_login():
    """Citizen login with phone number - sends OTP via SMS"""
    if request.method == 'POST':
        phone = request.form.get('phone', '').strip()
        
        if not phone:
            return render_template('phone_login.html', error='Please enter your phone number')
        
        # Send OTP
        result = otp_service.generate_otp(phone)
        
        if result['success']:
            # Store phone in session for OTP verification
            session['phone_for_otp'] = phone
            return redirect(url_for('verify_otp'))
        else:
            return render_template('phone_login.html', error=result['message'])
    
    return render_template('phone_login.html')


@app.route('/verify-otp', methods=['GET', 'POST'])
def verify_otp():
    """Verify OTP sent to phone number"""
    if 'phone_for_otp' not in session:
        return redirect(url_for('phone_login'))
    
    if request.method == 'POST':
        otp_code = request.form.get('otp', '').strip()
        phone = session.get('phone_for_otp')
        
        if not otp_code:
            return render_template('otp_verification.html', error='Please enter OTP')
        
        # Verify OTP
        result = otp_service.verify_otp(phone, otp_code)
        
        if result['success']:
            user_id = result['user_id']
            
            # Get user details
            user = get_db().execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
            
            if user:
                # Set session
                session['user_id'] = user_id
                session['user_name'] = user['name']
                session['role'] = user['role']
                session.permanent = True
                
                # Clear OTP session data
                session.pop('phone_for_otp', None)
                
                return redirect(url_for('dashboard'))
        
        return render_template('otp_verification.html', error=result['message'])
    
    return render_template('otp_verification.html')


@app.route('/resend-otp', methods=['POST'])
def resend_otp():
    """Resend OTP with cooldown protection"""
    phone = session.get('phone_for_otp')
    
    if not phone:
        return jsonify({'success': False, 'message': 'No phone session found'}), 400
    
    result = otp_service.generate_otp(phone)
    
    if result['success']:
        return jsonify({
            'success': True,
            'message': result['message'],
            'otp': result.get('otp', '')  # Only for dev/testing
        })
    else:
        return jsonify({'success': False, 'message': result['message']})


@app.route('/skip-login')
def skip_login():
    """Allow citizen to file complaint without upfront login (guest citizen flow)."""
    db = get_db()
    guest = db.execute("SELECT * FROM users WHERE email = 'guest@grievanceconnect.local'").fetchone()
    if guest:
        session['user_id'] = guest['id']
        session['user_name'] = guest['name']
        session['role'] = 'citizen'
        session.permanent = True
    return redirect(url_for('new_complaint'))




# Authority selection entry point
@app.route('/authority/select')
def authority_select():
    """Render a page where authority users choose their department before logging in."""
    return render_template('authority_select.html')
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Secure admin login with email and password supporting hashed & plain passwords."""
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        
        if not email or not password:
            return render_template('admin_login.html', error='Email and password required')
        
        user = get_db().execute(
            'SELECT * FROM users WHERE email = ? AND role = ?',
            (email, 'admin')
        ).fetchone()
        
        if user and verify_user_password(user['password'], password):
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            session['role'] = 'admin'
            session.permanent = True
            
            return redirect(url_for('admin_dashboard'))
        
        return render_template('admin_login.html', error='Invalid email or password')
    
    return render_template('admin_login.html')


@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    sync_automatic_statuses(get_db())
    """Admin Executive Dashboard showing all complaints, GIS metrics, and 3 Department Portals."""
    complaints = get_db().execute(
        '''
        SELECT c.*, u.name AS submitted_by, u.phone
        FROM complaints c
        JOIN users u ON c.user_id = u.id
        ORDER BY c.created_at DESC
        '''
    ).fetchall()
    
    complaint_list = []
    for c in complaints:
        c_dict = dict(c)
        dept = c_dict.get('department') or get_department_for_category(c_dict.get('category'))
        c_dict['department'] = dept
        p = c_dict.get('priority') or 0
        if p >= 7:
            c_dict['priority_level'] = 'HIGH'
        elif p >= 4:
            c_dict['priority_level'] = 'MEDIUM'
        else:
            c_dict['priority_level'] = 'LOW'
        complaint_list.append(c_dict)

    stats = {
        'total': len(complaint_list),
        'pending': len([c for c in complaint_list if c['status'] == 'Pending']),
        'in_progress': len([c for c in complaint_list if c['status'] == 'In Progress']),
        'resolved': len([c for c in complaint_list if c['status'] == 'Resolved']),
        'high_priority': len([c for c in complaint_list if c['priority_level'] == 'HIGH']),
        'medium_priority': len([c for c in complaint_list if c['priority_level'] == 'MEDIUM']),
        'low_priority': len([c for c in complaint_list if c['priority_level'] == 'LOW']),
        'electricity_count': len([c for c in complaint_list if c['department'] == 'ELECTRICITY']),
        'pwd_count': len([c for c in complaint_list if c['department'] == 'PWD']),
        'water_count': len([c for c in complaint_list if c['department'] == 'WATER']),
    }
    
    return render_template('admin_dashboard.html', stats=stats, complaints=complaint_list)


@app.route('/admin/department/<dept_name>/login', methods=['GET', 'POST'])
def admin_department_login(dept_name):
    """Dedicated login for each of the 3 Authority Departments: ELECTRICITY, PWD, WATER"""
    dept_upper = dept_name.upper().strip()
    if dept_upper not in ['ELECTRICITY', 'PWD', 'WATER']:
        return redirect(url_for('index'))

    dept_meta = {
        'ELECTRICITY': {
            'title': 'ELECTRICITY DEPARTMENT',
            'kannada_title': 'ವಿದ್ಯುತ್ ಇಲಾಖೆ ಪ್ರಾಧಿಕಾರ',
            'icon': '⚡',
            'badge': 'Energy & Power Infrastructure Redressal',
            'color': '#f59e0b',
            'demo_email': 'electricity@grievanceconnect.com',
            'demo_pass': 'elec123',
            'categories': ['Electricity / Power Supply', 'Streetlight']
        },
        'PWD': {
            'title': 'PWD INFRASTRUCTURE',
            'kannada_title': 'ಲೋಕೋಪಯೋಗಿ ಇಲಾಖೆ (PWD) ಪ್ರಾಧಿಕಾರ',
            'icon': '🏗️',
            'badge': 'Roads & Public Infrastructure Redressal',
            'color': '#3b82f6',
            'demo_email': 'pwd@grievanceconnect.com',
            'demo_pass': 'pwd123',
            'categories': ['Road Damage', 'Drainage / Public Infrastructure', 'Other PWD / Public Infrastructure']
        },
        'WATER': {
            'title': 'WATER & SANITATION',
            'kannada_title': 'ಜಲಮಂಡಳಿ ಮತ್ತು ನೈರ್ಮಲ್ಯ ಪ್ರಾಧಿಕಾರ',
            'icon': '💧',
            'badge': 'Potable Water & Contamination Redressal',
            'color': '#06b6d4',
            'demo_email': 'water@grievanceconnect.com',
            'demo_pass': 'water123',
            'categories': ['Water Supply', 'Water Leakage / Pipeline', 'Water Quality / Contamination']
        }
    }

    error = request.args.get('error')

    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        if not email or not password:
            return render_template('department_login.html', 
                                   department=dept_upper, 
                                   dept_info=dept_meta[dept_upper],
                                   error='Email and password are required.')

        user = get_db().execute(
            'SELECT * FROM users WHERE email = ?',
            (email,)
        ).fetchone()

        if user and verify_user_password(user['password'], password):
            u_role = user['role']
            u_dept = (user['department'] or '').upper()

            # Master admin can access any department; Department officer only accesses their assigned dept
            if u_role == 'admin' or u_dept == dept_upper:
                session['user_id'] = user['id']
                session['user_name'] = user['name']
                session['role'] = u_role if u_role == 'admin' else 'authority'
                session['department'] = dept_upper
                session.permanent = True
                return redirect(url_for('admin_department_portal', dept_name=dept_name.lower()))
            else:
                return render_template('department_login.html',
                                       department=dept_upper,
                                       dept_info=dept_meta[dept_upper],
                                       error=f"Access Denied: Your account ({u_dept or u_role}) is not authorized for the {dept_upper} Department. Please log in with {dept_upper} Authority credentials.")

        return render_template('department_login.html',
                               department=dept_upper,
                               dept_info=dept_meta[dept_upper],
                               error='Invalid credentials. Please check your email and password.')

    return render_template('department_login.html',
                           department=dept_upper,
                           dept_info=dept_meta[dept_upper],
                           error=error)


@app.route('/admin/department/<dept_name>')
def admin_department_portal(dept_name):
    sync_automatic_statuses(get_db())
    """Dedicated portal for each of the 3 Authority Departments: ELECTRICITY, PWD, WATER"""
    dept_upper = dept_name.upper().strip()
    if dept_upper not in ['ELECTRICITY', 'PWD', 'WATER']:
        return redirect(url_for('admin_dashboard'))

    # Strict Department Access Authorization:
    # User must be logged in as an authority or admin
    if 'user_id' not in session or session.get('role') not in ['admin', 'authority']:
        return redirect(url_for('admin_department_login', dept_name=dept_name.lower()))

    # Department Isolation: Electricity authority cannot access Water or PWD, etc.
    user_dept = (session.get('department') or '').upper()
    user_role = session.get('role')
    if user_role != 'admin' and user_dept != dept_upper:
        return redirect(url_for('admin_department_login', dept_name=dept_name.lower(),
                                error=f"Access Denied: You are logged in as {user_dept} authority. Unauthorized access to {dept_upper} portal."))

    all_complaints = get_db().execute(
        '''
        SELECT c.*, u.name AS submitted_by, u.phone
        FROM complaints c
        JOIN users u ON c.user_id = u.id
        ORDER BY c.created_at DESC
        '''
    ).fetchall()

    dept_complaints = []
    for c in all_complaints:
        c_dict = dict(c)
        c_dept = c_dict.get('department') or get_department_for_category(c_dict.get('category'))
        c_dict['department'] = c_dept
        p = c_dict.get('priority') or 0
        if p >= 7:
            c_dict['priority_level'] = 'HIGH'
        elif p >= 4:
            c_dict['priority_level'] = 'MEDIUM'
        else:
            c_dict['priority_level'] = 'LOW'

        if c_dept == dept_upper:
            dept_complaints.append(c_dict)

    stats = {
        'total': len(dept_complaints),
        'pending': len([c for c in dept_complaints if c['status'] == 'Pending']),
        'in_progress': len([c for c in dept_complaints if c['status'] == 'In Progress']),
        'resolved': len([c for c in dept_complaints if c['status'] == 'Resolved']),
        'high_priority': len([c for c in dept_complaints if c['priority_level'] == 'HIGH']),
        'medium_priority': len([c for c in dept_complaints if c['priority_level'] == 'MEDIUM']),
        'low_priority': len([c for c in dept_complaints if c['priority_level'] == 'LOW']),
    }

    dept_meta = {
        'ELECTRICITY': {
            'title': 'Electricity Department Portal',
            'kannada_title': 'ವಿದ್ಯುತ್ ಇಲಾಖೆ ಪೋರ್ಟಲ್',
            'icon': '⚡',
            'color': '#f59e0b',
            'desc': 'Power Supply & Streetlights Management',
            'categories': ['Electricity / Power Supply', 'Streetlight']
        },
        'PWD': {
            'title': 'Public Works Department (PWD) Portal',
            'kannada_title': 'ಲೋಕೋಪಯೋಗಿ ಇಲಾಖೆ (PWD) ಪೋರ್ಟಲ್',
            'icon': '🏗',
            'color': '#3b82f6',
            'desc': 'Roads, Bridges, Drainage & Public Infrastructure Management',
            'categories': ['Road Damage', 'Drainage / Public Infrastructure', 'Other PWD / Public Infrastructure']
        },
        'WATER': {
            'title': 'Water & Sanitation Authority Portal',
            'kannada_title': 'ಜಲಮಂಡಳಿ ಮತ್ತು ನೈರ್ಮಲ್ಯ ಇಲಾಖೆ ಪೋರ್ಟಲ್',
            'icon': '💧',
            'color': '#06b6d4',
            'desc': 'Drinking Water Supply, Pipelines & Contamination Management',
            'categories': ['Water Supply', 'Water Leakage / Pipeline', 'Water Quality / Contamination']
        }
    }

    return render_template(
        'department_portal.html',
        department=dept_upper,
        dept_info=dept_meta.get(dept_upper, {}),
        stats=stats,
        complaints=dept_complaints
    )


@app.route('/admin/complaint/<int:complaint_id>/status', methods=['POST'])
@login_required
def update_complaint_status(complaint_id):
    """Update resolution status of a complaint by administrative authority or master admin."""
    if session.get('role') not in ['admin', 'authority']:
        if request.is_json:
            return jsonify({'error': 'Unauthorized authority access', 'success': False}), 403
        return redirect(url_for('login'))

    new_status = request.form.get('status') or (request.get_json() or {}).get('status')
    allowed = ['Pending', 'In Progress', 'Resolved', 'Rejected/Cancelled']
    if new_status not in allowed:
        if request.is_json:
            return jsonify({'error': 'Invalid status', 'success': False}), 400
        return redirect(request.referrer or url_for('admin_dashboard'))

    get_db().execute('UPDATE complaints SET status = ?, manual_status = 1 WHERE id = ?', (new_status, complaint_id))
    get_db().commit()

    if request.is_json:
        return jsonify({'success': True, 'complaint_id': complaint_id, 'new_status': new_status})
    return redirect(request.referrer or url_for('admin_dashboard'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = get_db().execute(
            'SELECT * FROM users WHERE email = ?',
            (email,)
        ).fetchone()

        if user and verify_user_password(user['password'], password):
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            session['role'] = user['role'] or 'citizen'
            if session['role'] == 'admin':
                return redirect(url_for('admin_dashboard'))
            return redirect(url_for('dashboard'))

        return render_template('login.html', error='Invalid email or password')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')

        if not name or not email or not password:
            return render_template('register.html', error='All required fields must be filled')

        try:
            hashed_pwd = generate_password_hash(password)
            get_db().execute(
                'INSERT INTO users (name, email, phone, password, role) VALUES (?, ?, ?, ?, ?)',
                (name, email, phone, hashed_pwd, 'citizen')
            )
            get_db().commit()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            return render_template('register.html', error='Email already exists')

    return render_template('register.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    sync_automatic_statuses(get_db())
    user_id = session.get('user_id')
    role = session.get('role', 'citizen')
    
    # Ensure citizen only sees their own complaints
    if role == 'citizen':
        complaints = get_db().execute(
            '''
            SELECT * FROM complaints
            WHERE user_id = ?
            ORDER BY created_at DESC
            ''',
            (user_id,)
        ).fetchall()
    else:
        # Admins see all
        complaints = get_db().execute(
            '''
            SELECT * FROM complaints
            ORDER BY created_at DESC
            '''
        ).fetchall()

    complaint_list = []
    for c in complaints:
        c_dict = dict(c)
        c_dict['department'] = c_dict.get('department') or get_department_for_category(c_dict.get('category'))
        p = c_dict.get('priority') or 0
        if p >= 7:
            c_dict['priority_level'] = 'HIGH'
        elif p >= 4:
            c_dict['priority_level'] = 'MEDIUM'
        else:
            c_dict['priority_level'] = 'LOW'
        complaint_list.append(c_dict)

    recent_submission = session.pop('recent_submission', None)

    return render_template('dashboard.html', complaints=complaint_list, recent_submission=recent_submission)


@app.route('/new-complaint', methods=['GET', 'POST'])
def new_complaint():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form.get('title')
        category = request.form.get('category')
        location = request.form.get('location')
        description = request.form.get('description')
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        is_voice = request.form.get('is_voice_complaint', '0') == '1'
        language = request.form.get('language', 'en')

        voice_note_path = None
        image_path = None

        # Handle voice note upload if provided
        if is_voice and 'voice_note' in request.files:
            file = request.files['voice_note']
            if file and allowed_file(file.filename):
                save_result = voice_processor.save_voice_note(file, session['user_id'])
                if save_result['success']:
                    voice_note_path = save_result['relative_path']

        # Handle optional complaint image upload
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename:
                saved_path = save_uploaded_file(file, 'IMAGE_UPLOAD_FOLDER', IMAGE_ALLOWED_EXTENSIONS)
                if saved_path:
                    image_path = saved_path

        # If coordinates provided but no location name, try reverse geocoding
        try:
            if (not location or location.strip() == '') and latitude and longitude:
                resolved = reverse_geocode(float(latitude), float(longitude))
                if resolved:
                    location = resolved
        except Exception:
            pass

        # Validate required fields
        if not title or not location or not description:
            return render_template('new_complaint.html', error='Please fill all required complaint fields')

        # AI Classification & Civic Scope Validation
        classification_result = classifier.classify_complaint(title, description, location)
        
        is_ajax = (
            request.is_json or 
            request.headers.get('X-Requested-With') == 'XMLHttpRequest' or 
            'application/json' in request.headers.get('Accept', '')
        )

        # CRUCIAL RULE: UNSUPPORTED COMPLAINTS MUST NOT BE SUBMITTED OR STORED IN DB
        if not classification_result.get('is_supported', True):
            if is_ajax:
                return jsonify({
                    'success': False,
                    'is_supported': False,
                    'message': classification_result.get('message', REJECTION_MESSAGE)
                }), 400
            return render_template(
                'new_complaint.html',
                unsupported_error=classification_result.get('message', REJECTION_MESSAGE),
                prev_title=title,
                prev_desc=description,
                prev_loc=location
            ), 400

        ai_category = classification_result['category']
        department = classification_result['department']
        priority = int(classification_result['priority'])

        # Insert complaint into database
        get_db().execute(
            '''
            INSERT INTO complaints 
            (user_id, title, category, department, location, description, status, latitude, longitude,
             is_voice_complaint, voice_note_path, image_path, language, ai_category, priority, manual_status)
            VALUES (?, ?, ?, ?, ?, ?, 'Pending', ?, ?, ?, ?, ?, ?, ?, ?, 0)
            ''',
            (session['user_id'], title, category or ai_category, department, location, description,
             latitude, longitude, is_voice, voice_note_path, image_path, language, ai_category, priority)
        )

        complaint_id = get_db().execute('SELECT last_insert_rowid()').fetchone()[0]

        # Log priority classification
        try:
            get_db().execute(
                '''
                INSERT INTO complaint_priority_log (complaint_id, priority_score, classification_confidence)
                VALUES (?, ?, ?)
                ''',
                (complaint_id, classification_result['priority'], classification_result['confidence'])
            )
        except Exception:
            pass

        get_db().commit()

        # Set flash banner confirmation for dashboard
        session['recent_submission'] = {
            'id': complaint_id,
            'category': ai_category,
            'department': department,
            'priority_level': classification_result.get('priority_level', 'MEDIUM'),
            'priority': priority
        }

        # Build Demo SMS Details for Acknowledgement
        user_row = get_db().execute("SELECT phone, name FROM users WHERE id = ?", (session['user_id'],)).fetchone()
        user_phone = (user_row['phone'] if user_row and user_row['phone'] else '') or '+91 98765 43210'
        
        dept_title = department
        if department == 'ELECTRICITY':
            dept_title = 'Electricity Department'
        elif department == 'PWD':
            dept_title = 'PWD Infrastructure Department'
        elif department == 'WATER':
            dept_title = 'Water & Sanitation Department'

        created_time_str = datetime.now().strftime('%d %b %Y, %I:%M %p')
        demo_sms_text = f"Govt of Karnataka - GrievanceConnect: Your complaint #{complaint_id} for '{ai_category}' has been registered and forwarded to {dept_title}. Initial Status: Pending."

        if is_ajax:
            return jsonify({
                'success': True,
                'is_supported': True,
                'complaint_id': complaint_id,
                'category': ai_category,
                'department': department,
                'dept_title': dept_title,
                'priority_level': classification_result.get('priority_level', 'MEDIUM'),
                'priority': priority,
                'location': location,
                'status': 'Pending',
                'created_at': created_time_str,
                'message': f"Your complaint has been successfully received, categorized under {ai_category}, and routed to the {dept_title} for immediate action.",
                'demo_sms': {
                    'to': user_phone,
                    'text': demo_sms_text,
                    'status': 'Simulated Demo SMS Delivery (Zero Cost)'
                }
            })

        return redirect(url_for('dashboard'))

    return render_template('new_complaint.html')


@app.route('/voice-complaint', methods=['GET', 'POST'])
def voice_complaint():
    """Voice-based complaint submission page"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        title = request.form.get('title', '')[:100]
        description = request.form.get('description')
        location = request.form.get('location')
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        
        # If coordinates provided but no location name, try reverse geocoding
        try:
            if (not location or location.strip() == '') and latitude and longitude:
                resolved = reverse_geocode(float(latitude), float(longitude))
                if resolved:
                    location = resolved
        except Exception:
            pass

        if not location or not description:
            return render_template('voice_complaint.html', error='Location and description are required')
        
        # AI Classification & Validation
        classification_result = classifier.classify_complaint(title or description[:50], description, location)
        
        if not classification_result.get('is_supported', True):
            return render_template(
                'voice_complaint.html',
                unsupported_error=classification_result.get('message', REJECTION_MESSAGE)
            ), 400

        ai_category = classification_result['category']
        department = classification_result['department']
        priority = int(classification_result['priority'])
        
        # Insert complaint
        get_db().execute(
            '''
            INSERT INTO complaints 
            (user_id, title, category, department, location, description, status, latitude, longitude, 
             is_voice_complaint, ai_category, priority)
            VALUES (?, ?, ?, ?, ?, ?, 'Pending', ?, ?, 1, ?, ?)
            ''',
            (session['user_id'], title or description[:100], ai_category, department, location, description,
             latitude, longitude, ai_category, priority)
        )
        
        complaint_id = get_db().execute('SELECT last_insert_rowid()').fetchone()[0]
        
        try:
            get_db().execute(
                '''
                INSERT INTO complaint_priority_log (complaint_id, priority_score, classification_confidence)
                VALUES (?, ?, ?)
                ''',
                (complaint_id, classification_result['priority'], classification_result['confidence'])
            )
        except Exception:
            pass
        
        get_db().commit()

        session['recent_submission'] = {
            'id': complaint_id,
            'category': ai_category,
            'department': department,
            'priority_level': classification_result.get('priority_level', 'MEDIUM'),
            'priority': priority
        }

        return redirect(url_for('dashboard'))
    
    return render_template('voice_complaint.html')


@app.route('/complaints')
def complaints():
    sync_automatic_statuses(get_db())
    complaint_list = get_db().execute(
        '''
        SELECT c.*, u.name AS submitted_by
        FROM complaints c
        JOIN users u ON c.user_id = u.id
        ORDER BY c.created_at DESC
        '''
    ).fetchall()

    formatted_complaints = []
    for item in complaint_list:
        c_dict = dict(item)
        c_dict['department'] = c_dict.get('department') or get_department_for_category(c_dict.get('category'))
        p = c_dict.get('priority') or 0
        c_dict['priority_level'] = 'HIGH' if p >= 7 else ('MEDIUM' if p >= 4 else 'LOW')
        formatted_complaints.append(c_dict)

    return render_template('complaints.html', complaints=formatted_complaints)


@app.route('/complaint/<int:complaint_id>')
def complaint_details(complaint_id):
    sync_automatic_statuses(get_db())
    complaint = get_db().execute(
        '''
        SELECT c.*, u.name AS submitted_by
        FROM complaints c
        JOIN users u ON c.user_id = u.id
        WHERE c.id = ?
        ''',
        (complaint_id,)
    ).fetchone()

    if complaint is None:
        return redirect(url_for('complaints'))

    complaint_data = dict(complaint)
    complaint_data['date'] = datetime.strptime(complaint_data['created_at'], '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
    complaint_data['department'] = complaint_data.get('department') or get_department_for_category(complaint_data.get('category'))
    
    p = complaint_data.get('priority') or 0
    if p >= 7:
        complaint_data['priority_level'] = 'HIGH'
        complaint_data['priority_label'] = 'High'
    elif p >= 4:
        complaint_data['priority_level'] = 'MEDIUM'
        complaint_data['priority_label'] = 'Medium'
    else:
        complaint_data['priority_level'] = 'LOW'
        complaint_data['priority_label'] = 'Low'
    
    return render_template('complaint_details.html', complaint=complaint_data)


@app.route('/admin')
def admin_home():
    if session.get('role') == 'admin':
        return redirect(url_for('admin_dashboard'))
    return redirect(url_for('admin_login'))


# ==================== AI & VOICE API ENDPOINTS ====================

@app.route('/api/classify-complaint', methods=['POST'])
def api_classify_complaint():
    """API endpoint for AI-based complaint classification, department mapping and scope validation."""
    try:
        data = request.get_json() or {}
        title = data.get('title', '')
        description = data.get('description') or data.get('text', '')
        location = data.get('location', '')
        
        if not title and not description:
            return jsonify({'error': 'Title or description is required', 'success': False}), 400
        
        result = classifier.classify_complaint(title, description, location)
        
        return jsonify({
            'success': True,
            'is_supported': result.get('is_supported', True),
            'category': result['category'],
            'department': result.get('department'),
            'priority': result['priority'],
            'priority_level': result.get('priority_level', 'MEDIUM'),
            'confidence': result['confidence'],
            'message': result.get('message')
        })
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500


@app.route('/api/transcribe-voice', methods=['POST'])
def api_transcribe_voice():
    """API endpoint for voice transcription"""
    try:
        if 'voice_file' not in request.files:
            return jsonify({'error': 'No voice file provided', 'success': False}), 400
        
        file = request.files['voice_file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected', 'success': False}), 400
        
        if not allowed_file(file.filename):
            return jsonify({
                'error': f'File type not allowed. Allowed: {", ".join(ALLOWED_EXTENSIONS)}',
                'success': False
            }), 400
        
        # Save temporary file
        temp_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
        file.save(temp_path)
        
        # Transcribe
        result = voice_processor.transcribe_audio(temp_path)
        
        # Clean up temporary file
        if os.path.exists(temp_path):
            os.remove(temp_path)
        
        return jsonify({
            'success': result['success'],
            'text': result['text'],
            'confidence': result['confidence'],
            'error_message': result['error_message']
        })
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500


@app.route('/api/complaints-by-priority', methods=['GET'])
def api_complaints_by_priority():
    """API endpoint to get complaints sorted by priority"""
    try:
        sort_order = request.args.get('order', 'desc')  # 'asc' or 'desc'
        limit = request.args.get('limit', 20, type=int)
        
        query = '''
            SELECT c.*, u.name AS submitted_by
            FROM complaints c
            JOIN users u ON c.user_id = u.id
            ORDER BY c.priority {}
            LIMIT ?
        '''
        
        query = query.format('DESC' if sort_order == 'desc' else 'ASC')
        
        complaints = get_db().execute(query, (limit,)).fetchall()
        
        return jsonify({
            'success': True,
            'complaints': [dict(c) for c in complaints]
        })
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500


@app.route('/api/voice-complaints', methods=['GET'])
def api_voice_complaints():
    """API endpoint to get all voice-based complaints"""
    try:
        voice_complaints = get_db().execute(
            '''
            SELECT c.*, u.name AS submitted_by
            FROM complaints c
            JOIN users u ON c.user_id = u.id
            WHERE c.is_voice_complaint = 1
            ORDER BY c.created_at DESC
            '''
        ).fetchall()
        
        return jsonify({
            'success': True,
            'complaints': [dict(c) for c in voice_complaints]
        })
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500


@app.route('/api/complaint-stats', methods=['GET'])
def api_complaint_stats():
    """API endpoint for detailed complaint statistics with priority breakdown"""
    try:
        db = get_db()
        
        stats = {
            'total': db.execute('SELECT COUNT(*) FROM complaints').fetchone()[0],
            'pending': db.execute("SELECT COUNT(*) FROM complaints WHERE status = 'Pending'").fetchone()[0],
            'resolved': db.execute("SELECT COUNT(*) FROM complaints WHERE status = 'Resolved'").fetchone()[0],
            'critical': db.execute("SELECT COUNT(*) FROM complaints WHERE status = 'Critical'").fetchone()[0],
            'voice_complaints': db.execute("SELECT COUNT(*) FROM complaints WHERE is_voice_complaint = 1").fetchone()[0],
            'geo_tagged': db.execute("SELECT COUNT(*) FROM complaints WHERE latitude IS NOT NULL").fetchone()[0],
            'by_priority': {},
            'by_category': {}
        }
        
        # Priority breakdown
        priority_data = db.execute(
            'SELECT priority, COUNT(*) as count FROM complaints GROUP BY priority ORDER BY priority DESC'
        ).fetchall()
        for row in priority_data:
            stats['by_priority'][f"Priority {row['priority']}"] = row['count']
        
        # Category breakdown
        category_data = db.execute(
            'SELECT ai_category, COUNT(*) as count FROM complaints WHERE ai_category IS NOT NULL GROUP BY ai_category'
        ).fetchall()
        for row in category_data:
            stats['by_category'][row['ai_category']] = row['count']
        
        return jsonify({'success': True, 'stats': stats})
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500


@app.route('/api/complaint-analytics', methods=['GET'])
def api_complaint_analytics():
    """Return raw complaint records for analytics (uses real DB data)."""
    try:
        if 'user_id' not in session:
            return jsonify({'error': 'User not authenticated', 'success': False}), 401

        db = get_db()
        rows = db.execute(
            '''
            SELECT id, title, category, department, ai_category, status, priority, created_at
            FROM complaints
            WHERE user_id = ?
            ORDER BY created_at ASC
            ''',
            (session['user_id'],)
        ).fetchall()

        complaints = []
        for r in rows:
            rec = {k: r[k] for k in r.keys()}
            rec['category'] = rec.get('ai_category') or rec.get('category') or 'Uncategorized'
            rec['department'] = rec.get('department') or get_department_for_category(rec['category'])
            try:
                rec['priority'] = int(rec.get('priority') or 0)
            except Exception:
                rec['priority'] = 0
            complaints.append(rec)

        return jsonify({'success': True, 'complaints': complaints})
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500


@app.route('/api/process-voice-complaint', methods=['POST'])
def api_process_voice_complaint():
    """API endpoint to process a complete voice-based complaint with scope validation."""
    try:
        if 'user_id' not in session:
            return jsonify({'error': 'User not authenticated', 'success': False}), 401

        location = (request.form.get('location') or '').strip()
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        description = (request.form.get('description') or '').strip()
        title = (request.form.get('title') or '').strip()[:100]
        category = (request.form.get('category') or '').strip()

        try:
            latitude = float(latitude) if latitude not in (None, '') else None
        except Exception:
            latitude = None
        try:
            longitude = float(longitude) if longitude not in (None, '') else None
        except Exception:
            longitude = None

        save_result = None
        transcribed_text = description

        if 'voice_file' in request.files and request.files['voice_file'] and request.files['voice_file'].filename:
            file = request.files['voice_file']
            if not allowed_file(file.filename):
                return jsonify({'error': 'Invalid file type', 'success': False}), 400

            save_result = voice_processor.save_voice_note(file, session['user_id'])
            if not save_result['success']:
                return jsonify({'error': save_result['error_message'], 'success': False}), 400

            transcribe_result = voice_processor.transcribe_audio(save_result['filepath'])
            if transcribe_result['success'] and transcribe_result.get('text'):
                transcribed_text = transcribe_result['text'].strip()
            elif description:
                transcribed_text = description
            else:
                return jsonify({'error': transcribe_result.get('error_message') or 'Unable to process the voice note. Please enter the complaint manually.', 'success': False}), 400

        elif not description:
            return jsonify({'error': 'No voice input or complaint text provided', 'success': False}), 400

        if not transcribed_text:
            return jsonify({'error': 'Complaint text is required', 'success': False}), 400

        # If coords provided but no location name, try reverse geocoding
        if (not location or location.strip() == '') and latitude is not None and longitude is not None:
            try:
                resolved = reverse_geocode(latitude, longitude)
                if resolved:
                    location = resolved
            except Exception:
                pass

        if not location or not location.strip():
            return jsonify({'error': 'Location is required', 'success': False}), 400

        # AI Classification & Validation
        classification = classifier.classify_complaint(
            (title or transcribed_text[:50]),
            transcribed_text,
            location
        )

        if not classification.get('is_supported', True):
            return jsonify({
                'success': False,
                'is_supported': False,
                'error': classification.get('message', REJECTION_MESSAGE)
            }), 400

        ai_category = classification['category']
        department = classification['department']
        priority = int(classification['priority'])

        # Insert complaint
        get_db().execute(
            '''
            INSERT INTO complaints 
            (user_id, title, category, department, location, description, status, latitude, longitude,
             is_voice_complaint, voice_note_path, ai_category, priority)
            VALUES (?, ?, ?, ?, ?, ?, 'Pending', ?, ?, 1, ?, ?, ?)
            ''',
            (session['user_id'], (title or transcribed_text[:100]), category or ai_category,
             department, location, transcribed_text, latitude, longitude,
             save_result['relative_path'] if save_result and save_result.get('relative_path') else None,
             ai_category, priority)
        )

        complaint_id = get_db().execute('SELECT last_insert_rowid()').fetchone()[0]

        # Log priority
        try:
            get_db().execute(
                '''
                INSERT INTO complaint_priority_log (complaint_id, priority_score, classification_confidence)
                VALUES (?, ?, ?)
                ''',
                (complaint_id, classification['priority'], classification['confidence'])
            )
        except Exception:
            pass

        get_db().commit()

        session['recent_submission'] = {
            'id': complaint_id,
            'category': ai_category,
            'department': department,
            'priority_level': classification.get('priority_level', 'MEDIUM'),
            'priority': priority
        }

        return jsonify({
            'success': True,
            'is_supported': True,
            'complaint_id': complaint_id,
            'transcribed_text': transcribed_text,
            'category': ai_category,
            'department': department,
            'priority_level': classification.get('priority_level', 'MEDIUM'),
            'classification': classification,
            'message': 'Voice complaint processed successfully'
        })
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500


with app.app_context():
    init_db()


if __name__ == '__main__':
    app.run(debug=True)
