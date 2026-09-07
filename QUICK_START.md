# Quick Start Guide - GrievanceConnect

## 🚀 Getting Started in 5 Minutes

### Step 1: Install Dependencies
```bash
cd c:\AI-Grievance-System\frontend\GrievanceConnect
pip install -r requirements.txt
```

### Step 2: Run the Application
```bash
python app.py
```

Application will be available at: **http://localhost:5000**

### Step 3: Access the System
1. Open your browser and go to `http://localhost:5000`
2. Click **"Register"** to create an account
3. Fill in your details:
   - Name
   - Email
   - Phone
   - Password

### Step 4: Submit Your First Complaint

#### Option A: Text-Based Complaint
1. Click **"New Complaint"** or **"✍️ Text Report"**
2. Fill in the form:
   - **Title**: Brief description (e.g., "Broken streetlight")
   - **Category**: Select from dropdown or let AI auto-detect
   - **Location**: Enter location or click **"📍 Get Current Location"**
   - **Description**: Detailed explanation
3. Watch **AI classification** update in real-time
4. Click **"Submit Complaint"**

#### Option B: Voice-Based Complaint
1. Click **"🎤 Voice Report"** button
2. Click **"🎙️ Start Recording"**
3. Speak your complaint clearly (e.g., "There's a pothole on Main Street that damaged my car")
4. Click **"⏹️ Stop Recording"**
5. Review the transcribed text (edit if needed)
6. Click **"📍 Get Current Location"**
7. Select category or let AI auto-detect
8. Click **"Submit Voice Complaint"**

### Step 5: View Your Complaints
1. Click **"Dashboard"** to see your submitted complaints
2. View statistics:
   - Total complaints
   - Pending complaints
   - Resolved complaints
   - Voice reports count
3. Click **"View"** on any complaint to see details
4. Complaints are sorted by **Priority** (High → Low)

### Step 6: Check Interactive Map
1. Open any complaint details
2. Scroll down to see the **Interactive Map**
3. Map shows exact location of the complaint
4. Marker displays location name

---

## 🎯 Key Features to Try

### 1. AI Classification Preview
- While filling the complaint form
- Watch the **"🤖 AI Analysis"** section update
- Shows:
  - Predicted category
  - Priority level (High/Medium/Low)
  - Confidence percentage

### 2. Priority Sorting
- Go to **"All Complaints"** page
- Click **"🔴 By Priority"** button
- Complaints are automatically sorted by importance

### 3. Voice Transcription
- Navigate to **"🎤 Voice Report"**
- Record your complaint
- System automatically transcribes your speech
- Edit transcription if needed

### 4. Geolocation Tagging
- Click **"📍 Get Current Location"** button
- System requests browser permission
- Captures GPS coordinates
- Automatically finds location name

### 5. Filter Complaints
- On Dashboard:
  - **All** - Show all complaints
  - **Pending** - Only pending complaints
  - **Resolved** - Only resolved complaints
  - **🎤 Voice** - Only voice-based reports
  - **🔴 High Priority** - Only high priority complaints

---

## 📊 Dashboard Overview

### Statistics Cards
- **Total Complaints** - Overall complaint count
- **Pending** - Awaiting resolution
- **Resolved** - Completed complaints
- **Voice Reports** - Voice-based submissions

### Complaint List
Each complaint shows:
- **ID** - Unique complaint number
- **Title** - Complaint description
- **Category** - AI-detected category
- **Priority** - Color-coded level
- **Status** - Current status
- **🎤 Badge** - If submitted via voice

---

## 🎤 Voice Reporting Tips

1. **Speak Clearly**: Articulate your words clearly for better transcription
2. **Quiet Environment**: Submit from a quiet place for accuracy
3. **Complete Sentences**: Use natural language for better AI classification
4. **Include Location Details**: Mention landmarks or address
5. **Be Descriptive**: More details = better prioritization

### Example Voice Complaints:
- "There's a pothole on Main Street near the grocery store that's causing accidents"
- "The streetlight near Central Park has been broken for three weeks"
- "The water supply in my neighborhood has been cut off for two days"

---

## 🗺️ Geolocation Features

### How It Works:
1. Click **"📍 Get Current Location"**
2. Browser asks for location permission (allow it)
3. System captures:
   - Latitude
   - Longitude
   - Location name (city/town)
4. Location is stored and displayed on interactive map

### Interactive Map:
- Zoom in/out with mouse wheel
- Drag to pan
- Marker shows exact complaint location
- Location name displayed in popup

---

## 🤖 AI Classification Examples

### High Priority Complaints (7-10)
- 🏥 "Person collapsed, needs urgent medical help"
- 🚨 "Gas leak, emergency situation"
- ⚡ "High-voltage cable fell on the road"
- 💧 "No water supply for 3 days"

### Medium Priority Complaints (4-6)
- 🏗️ "Road has multiple potholes"
- 🔊 "Neighbor's noise disturbance every evening"
- 🧹 "Garbage not collected for a week"

### Low Priority Complaints (0-3)
- 💨 "Minor dust issues in the area"
- 🚗 "Parking space unavailable"

---

## 📈 Statistics API

### Check System Statistics
Visit: **http://localhost:5000/api/complaint-stats**

Returns JSON with:
- Total complaints count
- Breakdown by status
- Voice complaint statistics
- Geo-tagged complaint count
- Priority distribution
- Category distribution

---

## ❓ FAQ

**Q: Does the system require internet for voice?**
A: Yes, voice transcription uses Google Speech API which requires internet.

**Q: What if I don't allow location access?**
A: You can manually enter location text, geolocation is optional.

**Q: Can I edit a complaint after submission?**
A: Currently, complaints cannot be edited. Submit a new complaint if needed.

**Q: What audio formats are supported?**
A: WAV, MP3, FLAC, OGG, M4A formats are supported.

**Q: How is priority calculated?**
A: Based on keywords in complaint text and category. High-priority keywords (urgent, emergency, danger) increase priority.

**Q: Is my location data private?**
A: Location is stored in database. System doesn't share with third parties.

**Q: How accurate is AI classification?**
A: Typically 85-95% accurate. Confidence score shown with each classification.

---

## 🔧 Troubleshooting

### Problem: Microphone not working
**Solution**: 
1. Check browser permissions for microphone
2. Test microphone in system settings
3. Try using Chrome or Firefox browser

### Problem: Voice transcription failing
**Solution**:
1. Check internet connection
2. Speak more clearly
3. Use shorter recording (system supports up to 10 seconds)
4. Try again after few seconds

### Problem: Location not updating
**Solution**:
1. Allow location permission in browser
2. Check if browser has location services enabled
3. Clear browser cache and cookies
4. Manually enter location if automatic fails

### Problem: AI Classification not showing
**Solution**:
1. Ensure both title and description are filled
2. Wait 1-2 seconds for classification
3. Check browser console for errors
4. Refresh the page

---

## 📞 Need Help?

- Check **IMPLEMENTATION_GUIDE.md** for detailed documentation
- Review comment code for more information
- Check browser console (F12) for error messages

---

**Happy Reporting! 🎉**
