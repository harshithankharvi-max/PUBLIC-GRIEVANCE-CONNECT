# GrievanceConnect - AI-Powered Geo-Tagged Grievance Redressal System

## 🎯 Project Overview

GrievanceConnect is an intelligent grievance management system that combines cutting-edge technologies to provide a comprehensive solution for citizen complaints and grievances. The system features:

1. **📍 Geo-Tagged Complaint Reporting** - Track complaints with precise GPS coordinates and interactive maps
2. **🎤 Voice-Based Complaint System** - Submit complaints using natural voice input with automatic transcription
3. **🤖 AI-Based Classification & Prioritization** - Automatic complaint categorization and priority scoring for faster resolution
4. **📊 Advanced Analytics** - Comprehensive dashboard with priority-based sorting and filtering

---

## ✨ Key Features Implemented

### 1. **Geolocation System** 📍
**Features:**
- Automatic GPS location capture using browser Geolocation API
- Manual location input with reverse geocoding (using OpenStreetMap Nominatim)
- Interactive maps using Leaflet.js for complaint visualization
- Latitude/Longitude storage in database for accurate location tracking

**How to Use:**
- Click "📍 Get Current Location" button on complaint form
- System will request permission to access your location
- Location name is automatically fetched from coordinates
- Location is displayed on interactive map in complaint details

**Database Schema:**
```sql
latitude REAL          -- Latitude coordinate
longitude REAL         -- Longitude coordinate
```

---

### 2. **Voice-Based Reporting System** 🎤
**Features:**
- Real-time audio recording using Web Audio API
- Automatic speech-to-text transcription using Google Speech Recognition
- Support for multiple audio formats (WAV, MP3, FLAC, OGG, M4A)
- Live recording timer and status indicator
- Automatic location acquisition during voice report
- Editable transcription before submission

**Supported Files:**
- `.wav` - WAV Format
- `.mp3` - MP3 Format
- `.flac` - FLAC Format
- `.ogg` - OGG Format
- `.m4a` - M4A Format

**How to Use:**
1. Navigate to "🎤 Voice Report" page
2. Click "🎙️ Start Recording" button
3. Speak your complaint clearly
4. Click "⏹️ Stop Recording"
5. Review transcribed text (editable)
6. Allow location access
7. Select category (optional - AI will auto-detect)
8. Submit

**Database Schema:**
```sql
voice_note_path TEXT           -- Path to saved voice file
is_voice_complaint BOOLEAN     -- Flag indicating voice-based complaint
```

---

### 3. **AI Classification & Prioritization System** 🤖
**Features:**
- Automatic complaint categorization into 10 predefined categories
- Smart priority scoring (0-10 scale) based on content analysis
- Confidence score for classification accuracy
- Real-time preview during text input
- Keyword-based classification engine

**Complaint Categories:**
- 🏗️ **Infrastructure** - Roads, bridges, construction issues
- 💧 **Water & Sanitation** - Water supply, sewage, drainage
- ⚡ **Electricity** - Power supply, streetlights, outages
- 🏥 **Public Health** - Hospitals, clinics, health issues
- 🔊 **Noise Pollution** - Loud sounds, disturbances
- 💨 **Air Quality** - Pollution, emissions, smoke
- 🚨 **Public Safety** - Crime, accidents, security
- 🚗 **Traffic** - Congestion, parking, accidents
- 🧹 **Cleanliness** - Garbage, waste, litter
- ❓ **Other** - Miscellaneous complaints

**Priority Levels:**
- 🔴 **High Priority (7-10)** - Urgent/critical issues
- 🟡 **Medium Priority (4-6)** - Important but not urgent
- 🟢 **Low Priority (0-3)** - Routine maintenance

**Priority Calculation:**
- **High Priority Keywords**: urgent, emergency, critical, dangerous, hazard, injury, death
- **Medium Priority Keywords**: problem, issue, complaint, needs, important
- **Category-Based Defaults**: Safety/Health issues get higher priority

**Database Schema:**
```sql
ai_category TEXT               -- AI-predicted category
priority INTEGER DEFAULT 0     -- Priority score (0-10)
```

**API Endpoint:**
```
POST /api/classify-complaint
Content-Type: application/json

Request Body:
{
    "title": "Broken streetlight",
    "description": "The streetlight near Main Street is broken",
    "location": "Main Street, Downtown"
}

Response:
{
    "success": true,
    "category": "Electricity",
    "priority": 5,
    "confidence": 0.87
}
```

---

### 4. **Voice Transcription API** 🎙️
**Endpoint:**
```
POST /api/transcribe-voice
Content-Type: multipart/form-data

Parameters:
- voice_file: Audio file (WAV, MP3, FLAC, OGG, M4A)

Response:
{
    "success": true,
    "text": "Transcribed complaint text",
    "confidence": 0.95,
    "error_message": null
}
```

---

### 5. **Advanced Analytics APIs** 📊

#### Get Complaints by Priority
```
GET /api/complaints-by-priority?order=desc&limit=20

Response:
{
    "success": true,
    "complaints": [
        {
            "id": 1,
            "title": "...",
            "priority": 8,
            ...
        }
    ]
}
```

#### Get Voice Complaints
```
GET /api/voice-complaints

Response:
{
    "success": true,
    "complaints": [...]
}
```

#### Get Complaint Statistics
```
GET /api/complaint-stats

Response:
{
    "success": true,
    "stats": {
        "total": 45,
        "pending": 10,
        "resolved": 30,
        "critical": 5,
        "voice_complaints": 8,
        "geo_tagged": 42,
        "by_priority": {
            "Priority 8": 5,
            "Priority 5": 15
        },
        "by_category": {
            "Infrastructure": 12,
            "Electricity": 8
        }
    }
}
```

---

## 🗄️ Database Schema

### Enhanced Database Tables

#### Complaints Table (Updated)
```sql
CREATE TABLE complaints (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    category TEXT NOT NULL,
    location TEXT NOT NULL,
    description TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'Pending',
    priority INTEGER DEFAULT 0,              -- NEW: Priority score (0-10)
    ai_category TEXT,                        -- NEW: AI-predicted category
    voice_note_path TEXT,                    -- NEW: Path to voice file
    latitude REAL,                           -- NEW: GPS latitude
    longitude REAL,                          -- NEW: GPS longitude
    is_voice_complaint BOOLEAN DEFAULT 0,    -- NEW: Voice flag
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id)
)
```

#### Complaint Priority Log Table (New)
```sql
CREATE TABLE complaint_priority_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    complaint_id INTEGER NOT NULL,
    priority_score REAL,
    classification_confidence REAL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(complaint_id) REFERENCES complaints(id)
)
```

---

## 🚀 Installation & Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Required Python Packages
```
Flask==3.0.3
SpeechRecognition==3.10.0
pyaudio==0.2.13
scikit-learn==1.3.2
numpy==1.24.3
pandas==2.0.3
python-dotenv==1.0.0
geopy==2.3.0
requests==2.31.0
Werkzeug==3.0.0
```

### 3. Initialize Database
```python
python
from app import app, init_db
with app.app_context():
    init_db()
```

### 4. Run Application
```bash
python app.py
```

Application will be available at: `http://localhost:5000`

---

## 📱 Frontend Features

### Dashboard Enhancements
- ✅ Real-time priority indicator (🔴 High, 🟡 Medium, 🟢 Low)
- ✅ Voice complaint filter and indicator
- ✅ Complaint statistics with breakdowns
- ✅ Sort complaints by priority, status, date
- ✅ Geolocation indicator for tagged complaints

### New Complaint Form
- ✅ Real-time AI classification preview
- ✅ One-click geolocation capture
- ✅ Category auto-detection
- ✅ Priority level preview
- ✅ Confidence score display

### Voice Complaint Page
- ✅ Live audio recording with timer
- ✅ Real-time transcription display
- ✅ Editable transcription
- ✅ Automatic location detection
- ✅ Tab-based navigation (Voice/Text)
- ✅ AI classification in real-time

### Complaint Details
- ✅ Interactive map display with Leaflet
- ✅ Priority badge with color coding
- ✅ Voice note player with audio controls
- ✅ AI classification breakdown
- ✅ Geolocation coordinates display
- ✅ Voice indicator badge

---

## 🎨 UI Components

### Priority Badges
```html
🔴 High Priority (7-10)   - Red background
🟡 Medium Priority (4-6)  - Orange background
🟢 Low Priority (0-3)     - Green background
```

### Voice Indicators
```html
🎤 Voice - Blue indicator showing voice-based complaint
```

### Status Badges
```html
Pending   - Yellow
Resolved  - Green
Critical  - Red
```

---

## 🔒 Security Features

- SQLite database with parameterized queries (SQL injection protection)
- Session-based authentication
- File upload validation (whitelisted extensions)
- File size limits (50MB max for voice notes)
- Secure filename handling with Werkzeug
- CORS headers for API endpoints

---

## 🌍 Third-Party Services

1. **Google Speech Recognition API**
   - Free tier available
   - Automatic transcription of voice input
   - Supports multiple languages

2. **OpenStreetMap Nominatim**
   - Free reverse geocoding service
   - Converts GPS coordinates to location names
   - No API key required

3. **Leaflet.js**
   - Open-source mapping library
   - Interactive complaint location visualization
   - Tile layer from OpenStreetMap

---

## 📊 Usage Statistics & Monitoring

### View Complaint Statistics
Visit API endpoint: `/api/complaint-stats`

Returns comprehensive breakdown:
- Total complaints count
- Status distribution (Pending, Resolved, Critical)
- Voice complaint statistics
- Geo-tagged complaint count
- Priority distribution
- Category breakdown

---

## 🔧 Configuration

### App Configuration (app.py)
```python
app.config['SECRET_KEY'] = 'grievanceconnect-secret-key'
app.config['DATABASE'] = 'database/grievance.db'
app.config['UPLOAD_FOLDER'] = 'static/voice_notes'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB limit
```

### Allowed Audio Formats
```python
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'flac', 'ogg', 'm4a'}
```

---

## 📝 File Structure

```
GrievanceConnect/
├── app.py                    # Main Flask application
├── requirements.txt          # Python dependencies
├── database/
│   └── grievance.db         # SQLite database
├── models/
│   ├── __init__.py
│   ├── classifier.py        # AI classification engine
│   └── voice_processor.py   # Voice processing module
├── routes/
│   └── __init__.py
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── script.js
│   └── voice_notes/         # Voice file storage
└── templates/
    ├── index.html
    ├── login.html
    ├── register.html
    ├── dashboard.html       # UPDATED
    ├── new_complaint.html   # UPDATED
    ├── voice_complaint.html # NEW
    ├── complaint_details.html # UPDATED
    ├── complaints.html      # UPDATED
    └── admin_dashboard.html
```

---

## 🚀 Future Enhancements

- [ ] Image/photo attachment support for complaints
- [ ] Multi-language voice input support
- [ ] Advanced sentiment analysis
- [ ] Complaint clustering and duplicate detection
- [ ] Push notifications for complaint updates
- [ ] Mobile app (React Native/Flutter)
- [ ] Admin portal with advanced analytics
- [ ] SMS/Email notifications
- [ ] Integration with municipal databases
- [ ] Real-time complaint tracking map

---

## 📞 Support

For issues or feature requests, please contact the development team.

---

## 📄 License

This project is licensed under the MIT License.

---

**Last Updated:** August 2024  
**Version:** 1.0.0  
**Status:** ✅ Production Ready
