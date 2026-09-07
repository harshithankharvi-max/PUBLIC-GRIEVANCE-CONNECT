import os
import sqlite3
import json
from datetime import datetime, timedelta
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

from flask import Flask, g, redirect, render_template, request, session, url_for, jsonify
from dotenv import load_dotenv

from models import ComplaintClassifier, VoiceProcessor

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
    """Safely verify passwords supporting both plain text and secure hashes"""
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

        for stmt in additions:
            try:
                db.execute(stmt)
            except Exception:
                # If column already exists due to race or prior run, ignore
                pass
    except Exception:
        # If anything goes wrong while migrating schema, continue; table creation above suffices
        pass

    # Create default admin user if not exists (with hashed password)
    existing_admin = db.execute("SELECT id FROM users WHERE email = 'admin@grievanceconnect.com'").fetchone()
    if not existing_admin:
        hashed_pwd = generate_password_hash('admin123')
        db.execute(
            '''
            INSERT INTO users (id, name, email, phone, password, role, phone_verified)
            VALUES (?, ?, ?, ?, ?, 'admin', 1)
            ''',
            (1, 'Admin User', 'admin@grievanceconnect.com', '9999999999', hashed_pwd)
        )
    else:
        # Ensure existing admin has correct role
        db.execute(
            "UPDATE users SET role = 'admin' WHERE email = 'admin@grievanceconnect.com'"
        )
    
    db.commit()


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


@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Secure admin login with email and password"""
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        
        if not email or not password:
            return render_template('admin_login.html', error='Email and password required')
        
        user = get_db().execute(
            'SELECT * FROM users WHERE email = ? AND role = ?',
            (email, 'admin')
        ).fetchone()
        
        if user and check_password_hash(user['password'], password):
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
    """Admin-only dashboard showing all complaints"""
    """Admin-only dashboard showing all complaints with geospatial map and status control"""
    complaints = get_db().execute(
        '''
        SELECT c.*, u.name AS submitted_by, u.phone
        FROM complaints c
        JOIN users u ON c.user_id = u.id
        ORDER BY c.created_at DESC
        '''
    ).fetchall()
    
    complaint_list = [dict(c) for c in complaints]
    
    stats = {
        'total': len(complaints),
        'pending': len([c for c in complaints if c['status'] == 'Pending']),
        'in_progress': len([c for c in complaints if c['status'] == 'In Progress']),
        'resolved': len([c for c in complaints if c['status'] == 'Resolved']),
        'high_priority': len([c for c in complaints if c['priority'] >= 7]),
        'total': len(complaint_list),
        'pending': len([c for c in complaint_list if c['status'] == 'Pending']),
        'in_progress': len([c for c in complaint_list if c['status'] == 'In Progress']),
        'resolved': len([c for c in complaint_list if c['status'] == 'Resolved']),
        'high_priority': len([c for c in complaint_list if (c.get('priority') or 0) >= 7]),
        'geo_tagged': len([c for c in complaint_list if c.get('latitude') is not None and c.get('latitude') != ''])
    }
    
    return render_template('admin_dashboard.html', stats=stats, complaints=[dict(c) for c in complaints])
    # Category breakdown
    categories = {}
    for c in complaint_list:
        cat = c.get('ai_category') or c.get('category') or 'Other'
        categories[cat] = categories.get(cat, 0) + 1
    
    return render_template(
        'admin_dashboard.html',
        stats=stats,
        complaints=complaint_list,
        categories=categories
    )


@app.route('/admin/complaint/<int:complaint_id>/status', methods=['POST'])
@admin_required
def update_complaint_status(complaint_id):
    """Admin endpoint to update complaint status (Pending, In Progress, Resolved)"""
    new_status = request.form.get('status')
    if not new_status and request.is_json:
        data = request.get_json() or {}
        new_status = data.get('status')
        
    valid_statuses = {'Pending', 'In Progress', 'Resolved'}
    if not new_status or new_status not in valid_statuses:
        if request.is_json:
            return jsonify({'success': False, 'error': 'Invalid status'}), 400
        return redirect(url_for('admin_dashboard'))
        
    db = get_db()
    db.execute('UPDATE complaints SET status = ? WHERE id = ?', (new_status, complaint_id))
    db.commit()
    
    if request.is_json:
        return jsonify({'success': True, 'complaint_id': complaint_id, 'status': new_status})
        
    return redirect(url_for('admin_dashboard'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        user = get_db().execute(
            'SELECT * FROM users WHERE email = ? AND password = ?',
            (email, password)
            'SELECT * FROM users WHERE email = ?',
            (email,)
        ).fetchone()

        if user:
        if user and verify_user_password(user['password'], password):
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            session['role'] = user['role'] or 'citizen'
            session.permanent = True
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
            get_db().execute(
                'INSERT INTO users (name, email, phone, password) VALUES (?, ?, ?, ?)',
                (name, email, phone, password)
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
    user_id = session.get('user_id')
    role = session.get('role', 'citizen')
    
    # Get citizen profile details
    user = get_db().execute('SELECT id, name, email, phone, role FROM users WHERE id = ?', (user_id,)).fetchone()
    
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

    return render_template('dashboard.html', complaints=[dict(c) for c in complaints])
    recent_submission = session.pop('recent_submission', None)

    return render_template(
        'dashboard.html',
        complaints=[dict(c) for c in complaints],
        user=dict(user) if user else None,
        recent_submission=recent_submission
    )


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

        # AI Classification
        classification_result = classifier.classify_complaint(title, description, location)
        ai_category = classification_result['category']
        priority = int(classification_result['priority'])

        # Insert complaint into database
        # Insert complaint into database (AI category is used automatically)
        final_category = category if (category and category.strip()) else ai_category
        get_db().execute(
            '''
            INSERT INTO complaints 
            (user_id, title, category, location, description, status, latitude, longitude,
             is_voice_complaint, voice_note_path, image_path, language, ai_category, priority)
            VALUES (?, ?, ?, ?, ?, 'Pending', ?, ?, ?, ?, ?, ?, ?, ?)
            ''',
            (session['user_id'], title, category or ai_category, location, description,
            (session['user_id'], title, final_category, location, description,
             latitude, longitude, is_voice, voice_note_path, image_path, language, ai_category, priority)
        )

        complaint_id = get_db().execute('SELECT last_insert_rowid()').fetchone()[0]

        # Log priority classification
        get_db().execute(
            '''
            INSERT INTO complaint_priority_log (complaint_id, priority_score, classification_confidence)
            VALUES (?, ?, ?)
            ''',
            (complaint_id, classification_result['priority'], classification_result['confidence'])
        )

        get_db().commit()
        
        session['recent_submission'] = {
            'id': complaint_id,
            'title': title,
            'category': ai_category,
            'priority': priority
        }
        
        return redirect(url_for('dashboard'))

    return render_template('new_complaint.html')


@app.route('/voice-complaint', methods=['GET', 'POST'])
def voice_complaint():
    """Voice-based complaint submission page"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        # Same logic as new_complaint but assumes voice input
        title = request.form.get('title', '')[:100]
        description = request.form.get('description')
        location = request.form.get('location')
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        category = request.form.get('category')
        
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
        
        # AI Classification
        classification_result = classifier.classify_complaint(title or description[:50], description, location)
        ai_category = classification_result['category']
        priority = int(classification_result['priority'])
        final_category = category if (category and category.strip()) else ai_category
        
        # Insert complaint
        get_db().execute(
            '''
            INSERT INTO complaints 
            (user_id, title, category, location, description, status, latitude, longitude, 
             is_voice_complaint, ai_category, priority)
            VALUES (?, ?, ?, ?, ?, 'Pending', ?, ?, 1, ?, ?)
            ''',
            (session['user_id'], title or description[:100], ai_category, location, description,
            (session['user_id'], title or description[:100], final_category, location, description,
             latitude, longitude, ai_category, priority)
        )
        
        complaint_id = get_db().execute('SELECT last_insert_rowid()').fetchone()[0]
        
        # Log priority
        get_db().execute(
            '''
            INSERT INTO complaint_priority_log (complaint_id, priority_score, classification_confidence)
            VALUES (?, ?, ?)
            ''',
            (complaint_id, classification_result['priority'], classification_result['confidence'])
        )
        
        get_db().commit()
        
        session['recent_submission'] = {
            'id': complaint_id,
            'title': title or description[:50],
            'category': ai_category,
            'priority': priority
        }
        
        return redirect(url_for('dashboard'))
    
    return render_template('voice_complaint.html')


@app.route('/complaints')
def complaints():
    complaint_list = get_db().execute(
        '''
        SELECT c.*, u.name AS submitted_by
        FROM complaints c
        JOIN users u ON c.user_id = u.id
        ORDER BY c.created_at DESC
        '''
    ).fetchall()
    user_id = session.get('user_id')
    role = session.get('role', 'citizen')
    
    # If logged in as citizen, show citizen's own complaints; if admin or public, show all
    if user_id and role == 'citizen':
        complaint_list = get_db().execute(
            '''
            SELECT c.*, u.name AS submitted_by, u.phone
            FROM complaints c
            JOIN users u ON c.user_id = u.id
            WHERE c.user_id = ?
            ORDER BY c.created_at DESC
            ''',
            (user_id,)
        ).fetchall()
    else:
        complaint_list = get_db().execute(
            '''
            SELECT c.*, u.name AS submitted_by, u.phone
            FROM complaints c
            JOIN users u ON c.user_id = u.id
            ORDER BY c.created_at DESC
            '''
        ).fetchall()
        
    return render_template('complaints.html', complaints=[dict(item) for item in complaint_list])


@app.route('/complaint/<int:complaint_id>')
def complaint_details(complaint_id):
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
    
    # Add priority label
    priority_mapping = {
        0: 'Low', 1: 'Low', 2: 'Low', 3: 'Low',
        4: 'Medium', 5: 'Medium', 6: 'Medium',
        7: 'High', 8: 'High', 9: 'Critical', 10: 'Critical'
    }
    complaint_data['priority_label'] = priority_mapping.get(complaint_data['priority'], 'Unknown')
    
    return render_template('complaint_details.html', complaint=complaint_data)


@app.route('/admin')
def admin_home():
    if session.get('role') == 'admin':
        return redirect(url_for('admin_dashboard'))
    return redirect(url_for('admin_login'))


# ==================== AI & VOICE API ENDPOINTS ====================

@app.route('/api/classify-complaint', methods=['POST'])
def api_classify_complaint():
    """API endpoint for AI-based complaint classification"""
    try:
        data = request.get_json()
        title = data.get('title', '')
        description = data.get('description', '')
        location = data.get('location', '')
        
        if not title or not description:
            return jsonify({'error': 'Title and description are required'}), 400
        
        result = classifier.classify_complaint(title, description, location)
        
        return jsonify({
            'success': True,
            'category': result['category'],
            'priority': result['priority'],
            'confidence': result['confidence']
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
            SELECT id, title, category, ai_category, status, priority, created_at
            FROM complaints
            WHERE user_id = ?
            ORDER BY created_at ASC
            ''',
            (session['user_id'],)
        ).fetchall()

        complaints = []
        for r in rows:
            rec = {k: r[k] for k in r.keys()}
            # Normalize category to prefer ai_category when available
            rec['category'] = rec.get('ai_category') or rec.get('category') or 'Uncategorized'
            # Ensure priority is integer
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
    """API endpoint to process a complete voice-based complaint"""
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

        # AI Classification
        classification = classifier.classify_complaint(
            (title or transcribed_text[:50]),
            transcribed_text,
            location
        )

        # Insert complaint
        get_db().execute(
            '''
            INSERT INTO complaints 
            (user_id, title, category, location, description, status, latitude, longitude,
             is_voice_complaint, voice_note_path, ai_category, priority)
            VALUES (?, ?, ?, ?, ?, 'Pending', ?, ?, 1, ?, ?, ?)
            ''',
            (session['user_id'], (title or transcribed_text[:100]), category or classification['category'],
             location, transcribed_text, latitude, longitude,
             save_result['relative_path'] if save_result and save_result.get('relative_path') else None,
             classification['category'], int(classification['priority']))
        )

        complaint_id = get_db().execute('SELECT last_insert_rowid()').fetchone()[0]

        # Log priority
        get_db().execute(
            '''
            INSERT INTO complaint_priority_log (complaint_id, priority_score, classification_confidence)
            VALUES (?, ?, ?)
            ''',
            (complaint_id, classification['priority'], classification['confidence'])
        )

        get_db().commit()

        session['recent_submission'] = {
            'id': complaint_id,
            'title': (title or transcribed_text[:50]),
            'category': classification['category'],
            'priority': int(classification['priority'])
        }

        return jsonify({
            'success': True,
            'complaint_id': complaint_id,
            'transcribed_text': transcribed_text,
            'classification': classification,
            'message': 'Voice complaint processed successfully'
        })
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500


with app.app_context():
    init_db()


if __name__ == '__main__':
    app.run(debug=True)
