# API Documentation & Testing Guide

## 🔌 REST API Reference

### Base URL
```
http://localhost:5000/api
```

---

## 📋 API Endpoints

### 1. Complaint Classification
**Endpoint:** `POST /api/classify-complaint`

**Purpose:** Classify a complaint into category and priority

**Request:**
```json
{
  "title": "Broken streetlight",
  "description": "The streetlight near Main Street intersection is broken and creating a safety hazard",
  "location": "Main Street, Downtown Area"
}
```

**Response (Success):**
```json
{
  "success": true,
  "category": "Electricity",
  "priority": 6,
  "confidence": 0.89
}
```

**Response (Error):**
```json
{
  "success": false,
  "error": "Title and description are required"
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:5000/api/classify-complaint \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Broken streetlight",
    "description": "The streetlight is broken",
    "location": "Main Street"
  }'
```

**Python Example:**
```python
import requests

url = "http://localhost:5000/api/classify-complaint"
data = {
    "title": "Broken streetlight",
    "description": "The streetlight is broken",
    "location": "Main Street"
}

response = requests.post(url, json=data)
result = response.json()

print(f"Category: {result['category']}")
print(f"Priority: {result['priority']}")
print(f"Confidence: {result['confidence']}")
```

---

### 2. Voice Transcription
**Endpoint:** `POST /api/transcribe-voice`

**Purpose:** Convert audio file to text

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Parameter: `voice_file` (audio file)

**Supported Formats:**
- WAV (.wav)
- MP3 (.mp3)
- FLAC (.flac)
- OGG (.ogg)
- M4A (.m4a)

**Response (Success):**
```json
{
  "success": true,
  "text": "There's a large pothole on Main Street that damaged my car",
  "confidence": 0.95,
  "error_message": null
}
```

**Response (Error):**
```json
{
  "success": false,
  "text": "",
  "confidence": 0,
  "error_message": "Could not understand audio. Please speak clearly."
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:5000/api/transcribe-voice \
  -F "voice_file=@/path/to/audio.wav"
```

**Python Example:**
```python
import requests

url = "http://localhost:5000/api/transcribe-voice"
files = {"voice_file": open("/path/to/audio.wav", "rb")}

response = requests.post(url, files=files)
result = response.json()

if result['success']:
    print(f"Transcribed: {result['text']}")
else:
    print(f"Error: {result['error_message']}")
```

---

### 3. Process Voice Complaint
**Endpoint:** `POST /api/process-voice-complaint`

**Purpose:** Complete voice complaint processing (requires authentication)

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Parameters:
  - `voice_file` (audio file) - Required
  - `location` (string) - Required
  - `latitude` (float) - Optional
  - `longitude` (float) - Optional

**Response (Success):**
```json
{
  "success": true,
  "complaint_id": 42,
  "transcribed_text": "There's a large pothole on Main Street",
  "classification": {
    "category": "Infrastructure",
    "priority": 5,
    "confidence": 0.87
  },
  "message": "Voice complaint processed successfully"
}
```

**Response (Error):**
```json
{
  "success": false,
  "error": "User not authenticated"
}
```

**Python Example:**
```python
import requests

url = "http://localhost:5000/api/process-voice-complaint"
session = requests.Session()

# Assuming logged in via session
files = {"voice_file": open("complaint.wav", "rb")}
data = {
    "location": "Main Street, Downtown",
    "latitude": "40.7128",
    "longitude": "-74.0060"
}

response = session.post(url, files=files, data=data)
result = response.json()

if result['success']:
    print(f"Complaint ID: {result['complaint_id']}")
    print(f"Category: {result['classification']['category']}")
```

---

### 4. Get Voice Complaints
**Endpoint:** `GET /api/voice-complaints`

**Purpose:** Retrieve all voice-based complaints

**Request:**
```
GET /api/voice-complaints
```

**Response:**
```json
{
  "success": true,
  "complaints": [
    {
      "id": 42,
      "user_id": 5,
      "title": "Broken pothole",
      "category": "Infrastructure",
      "location": "Main Street",
      "description": "Large pothole...",
      "status": "Pending",
      "priority": 5,
      "ai_category": "Infrastructure",
      "voice_note_path": "voice_notes/user_5_20240818_143022.wav",
      "latitude": 40.7128,
      "longitude": -74.0060,
      "is_voice_complaint": 1,
      "created_at": "2024-08-18 14:30:22",
      "submitted_by": "John Doe"
    }
  ]
}
```

**cURL Example:**
```bash
curl -X GET http://localhost:5000/api/voice-complaints
```

---

### 5. Get Complaints by Priority
**Endpoint:** `GET /api/complaints-by-priority`

**Purpose:** Get complaints sorted by priority

**Query Parameters:**
- `order` (asc|desc) - Default: desc (highest priority first)
- `limit` (integer) - Default: 20

**Request:**
```
GET /api/complaints-by-priority?order=desc&limit=10
```

**Response:**
```json
{
  "success": true,
  "complaints": [
    {
      "id": 1,
      "title": "Gas leak - emergency",
      "priority": 10,
      "category": "Public Safety",
      "status": "Pending",
      "submitted_by": "Jane Smith"
    },
    {
      "id": 2,
      "title": "Pothole on Main Street",
      "priority": 5,
      "category": "Infrastructure",
      "status": "In Progress",
      "submitted_by": "John Doe"
    }
  ]
}
```

**cURL Example:**
```bash
curl -X GET "http://localhost:5000/api/complaints-by-priority?order=desc&limit=10"
```

---

### 6. Get Complaint Statistics
**Endpoint:** `GET /api/complaint-stats`

**Purpose:** Get comprehensive complaint statistics

**Request:**
```
GET /api/complaint-stats
```

**Response:**
```json
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
      "Priority 8": 3,
      "Priority 5": 12,
      "Priority 3": 30
    },
    "by_category": {
      "Infrastructure": 15,
      "Electricity": 8,
      "Water & Sanitation": 10,
      "Public Health": 5,
      "Other": 7
    }
  }
}
```

**cURL Example:**
```bash
curl -X GET http://localhost:5000/api/complaint-stats
```

**JavaScript Example:**
```javascript
async function getStats() {
  const response = await fetch('/api/complaint-stats');
  const data = await response.json();
  
  if (data.success) {
    console.log(`Total Complaints: ${data.stats.total}`);
    console.log(`Voice Complaints: ${data.stats.voice_complaints}`);
    console.log(`Geo-Tagged: ${data.stats.geo_tagged}`);
  }
}
```

---

## 🧪 Testing Examples

### Test Classification with Different Complaints

**High Priority Example:**
```bash
curl -X POST http://localhost:5000/api/classify-complaint \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Gas leak emergency",
    "description": "There is a strong gas smell coming from the building, emergency situation",
    "location": "123 Oak Street"
  }'

# Expected Response:
# "priority": 9-10 (High Priority)
# "category": "Public Safety"
```

**Medium Priority Example:**
```bash
curl -X POST http://localhost:5000/api/classify-complaint \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Pothole on street",
    "description": "There is a large pothole that needs to be fixed",
    "location": "Main Street"
  }'

# Expected Response:
# "priority": 4-6 (Medium Priority)
# "category": "Infrastructure"
```

**Low Priority Example:**
```bash
curl -X POST http://localhost:5000/api/classify-complaint \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Minor dust issue",
    "description": "There is some dust on the street",
    "location": "Park Area"
  }'

# Expected Response:
# "priority": 0-3 (Low Priority)
# "category": "Cleanliness"
```

---

### Test Voice Transcription

**Python Script:**
```python
import requests

def test_voice_transcription():
    # Assuming you have a voice_sample.wav file
    url = "http://localhost:5000/api/transcribe-voice"
    
    with open("voice_sample.wav", "rb") as f:
        files = {"voice_file": f}
        response = requests.post(url, files=files)
    
    result = response.json()
    
    print(f"Success: {result['success']}")
    print(f"Transcribed Text: {result['text']}")
    print(f"Confidence: {result['confidence']}")
    
    if not result['success']:
        print(f"Error: {result['error_message']}")

test_voice_transcription()
```

---

### Test Analytics APIs

**Get Top Priority Complaints:**
```bash
curl -X GET "http://localhost:5000/api/complaints-by-priority?order=desc&limit=5"
```

**Get Statistics Summary:**
```bash
curl -X GET http://localhost:5000/api/complaint-stats | python -m json.tool
```

---

## 🔐 Authentication

Most endpoints don't require authentication. However, `/api/process-voice-complaint` requires the user to be logged in (session-based).

### Authenticated Request Example:
```python
import requests

session = requests.Session()

# First, login
login_data = {
    "email": "user@example.com",
    "password": "password123"
}

# Login via the web interface or API
# Then use the session for authenticated requests

files = {"voice_file": open("complaint.wav", "rb")}
data = {"location": "Main Street"}

response = session.post(
    "http://localhost:5000/api/process-voice-complaint",
    files=files,
    data=data
)

print(response.json())
```

---

## 📊 Response Status Codes

| Code | Meaning | Example |
|------|---------|---------|
| 200 | Success | Classification returned |
| 400 | Bad Request | Missing required fields |
| 401 | Unauthorized | User not authenticated |
| 404 | Not Found | Endpoint doesn't exist |
| 500 | Server Error | Internal error |

---

## ⚠️ Error Handling

All API responses include a `success` field:

```json
{
  "success": true/false,
  "data": { ... },
  "error": "error message if applicable"
}
```

**Best Practice:**
```python
response = requests.get(url)
data = response.json()

if data.get('success'):
    # Process successful response
    print(data['data'])
else:
    # Handle error
    print(f"Error: {data.get('error')}")
```

---

## 🚀 Rate Limiting

Currently, no rate limiting is implemented. In production:
- Implement rate limiting (e.g., 100 requests/minute)
- Use caching for frequently accessed data
- Optimize database queries

---

## 📚 Usage Statistics

Track API usage:
```bash
# Check logs for API call patterns
tail -f app.log
```

---

## 🔄 Integration Examples

### JavaScript/Frontend
```javascript
// Classify a complaint
async function classifyComplaint(title, description, location) {
  const response = await fetch('/api/classify-complaint', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      title, description, location
    })
  });
  return await response.json();
}

// Get statistics
async function getStats() {
  const response = await fetch('/api/complaint-stats');
  return await response.json();
}
```

### Python/Backend
```python
import requests

# Classify complaint
def classify(title, desc, location):
    return requests.post(
        'http://localhost:5000/api/classify-complaint',
        json={'title': title, 'description': desc, 'location': location}
    ).json()

# Get voice complaints
def get_voice_complaints():
    return requests.get(
        'http://localhost:5000/api/voice-complaints'
    ).json()
```

---

## 🎯 Testing Checklist

- [ ] Classification API returns correct categories
- [ ] Voice transcription works with different audio formats
- [ ] Priority scoring is accurate
- [ ] Confidence scores are reasonable
- [ ] Geolocation coordinates are stored correctly
- [ ] API error handling works properly
- [ ] Response times are acceptable
- [ ] Database stores all information correctly

---

**Last Updated:** August 2024
