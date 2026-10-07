import os
import sys
import json
import sqlite3
from datetime import datetime, timedelta

# Set standard encoding
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Import Flask app
sys.path.insert(0, os.path.dirname(__file__))
from app import app, get_db, init_db, sync_automatic_statuses

def run_tests():
    print("==================================================")
    print("STARTING FULL GRIEVANCECONNECT VERIFICATION")
    print("==================================================")
    client = app.test_client()

    with app.app_context():
        init_db()

    # TEST 1: HOME PAGE
    print("\n[TEST 1] Testing Home Page...")
    res = client.get('/')
    assert res.status_code == 200, f"Expected 200, got {res.status_code}"
    html = res.data.decode('utf-8')
    assert "Civic Redressal Live Architecture" not in html, "Architecture section should be removed"
    assert "rural_civic_redressal.svg" in html, "Project SVG image should be present in hero"
    assert "AI-enabled Geospatial Public Grievance Redressal System for Rural Areas" in html
    assert "/authority/select" in html
    assert "/login" in html
    print("[PASS] TEST 1 PASSED: Home page renders correctly with image and without architecture box.")

    # TEST 2: AUTHORITY DEPARTMENT SELECTION
    print("\n[TEST 2] Testing Authority Department Selection Page...")
    res = client.get('/authority/select')
    assert res.status_code == 200, f"Expected 200, got {res.status_code}"
    html = res.data.decode('utf-8')
    assert "ELECTRICITY DEPARTMENT" in html
    assert "PWD INFRASTRUCTURE" in html
    assert "WATER & SANITATION" in html
    assert "card-electricity" in html
    assert "card-pwd" in html
    assert "card-water" in html
    assert "/admin/department/electricity/login" in html
    assert "/admin/department/pwd/login" in html
    assert "/admin/department/water/login" in html
    print("[PASS] TEST 2 PASSED: Exactly 3 balanced department cards appear with proper routes.")

    # TEST 3: DEPARTMENT LOGIN PAGES & NO DEMO CREDENTIALS
    print("\n[TEST 3] Testing 3 Department Login Pages (Checking Demo Credentials Removal)...")
    for dept in ['electricity', 'pwd', 'water']:
        res = client.get(f'/admin/department/{dept}/login')
        assert res.status_code == 200
        html = res.data.decode('utf-8')
        assert "Demonstration Authority Access" not in html, f"Demo credentials should not appear on {dept} page"
        assert "Default Password:" not in html, f"Default password should not appear on {dept} page"
        assert "Officer Email:" not in html, f"Officer email label should not appear on {dept} page"
    print("[PASS] TEST 3 PASSED: All 3 department login pages render without demonstration credential boxes.")

    # TEST 4: DEPARTMENT LOGIN FUNCTIONALITY
    print("\n[TEST 4] Testing Department Login Authentication...")
    with client.session_transaction() as sess:
        sess.clear()

    res = client.post('/admin/department/electricity/login', data={
        'email': 'electricity@grievanceconnect.com',
        'password': 'elec123'
    }, follow_redirects=False)
    assert res.status_code in [302, 200], f"Expected redirect, got {res.status_code}"
    
    # Check portal access
    res = client.get('/admin/department/electricity')
    assert res.status_code == 200
    html = res.data.decode('utf-8')
    assert "Electricity Department Portal" in html
    assert "Rejected/Cancelled" in html, "Rejected/Cancelled option should be present in status select"
    print("[PASS] TEST 4 PASSED: Department authority login works and portal has Rejected/Cancelled status.")

    # TEST 5: UNSUPPORTED GRIEVANCE SCOPE REJECTION
    print("\n[TEST 5] Testing Unsupported Grievance Scope Validation...")
    # Log in as citizen
    with client.session_transaction() as sess:
        sess['user_id'] = 1
        sess['user_name'] = 'Test Citizen'
        sess['role'] = 'citizen'

    unsupported_payload = {
        'title': 'College admission problem help needed',
        'description': 'My son did not get college admission this year please help with admission process',
        'location': 'Town Hall',
        'latitude': '',
        'longitude': ''
    }

    # Count complaints before
    with app.app_context():
        count_before = get_db().execute("SELECT COUNT(*) FROM complaints").fetchone()[0]

    res = client.post('/new-complaint', headers={'X-Requested-With': 'XMLHttpRequest', 'Accept': 'application/json'}, data=unsupported_payload)
    assert res.status_code == 400, f"Expected 400 for unsupported, got {res.status_code}"
    data = json.loads(res.data.decode('utf-8'))
    assert data.get('is_supported') is False, "is_supported must be False"
    assert "outside the supported civic categories" in data.get('message', ''), "Expected rejection message"

    with app.app_context():
        count_after = get_db().execute("SELECT COUNT(*) FROM complaints").fetchone()[0]
    assert count_before == count_after, "Unsupported complaint must NOT be inserted into database!"
    print("[PASS] TEST 5 PASSED: Unsupported grievance rejected without inserting into database.")

    # TEST 6: VALID CIVIC COMPLAINT SUBMISSION & AUTOMATIC REGISTRATION
    print("\n[TEST 6] Testing Valid Civic Complaint Auto-Classification & Instant Creation...")
    valid_payload = {
        'title': 'Streetlight broken and dark',
        'description': 'Main junction street light pole number 14 is broken and completely dark at night causing danger',
        'location': 'Hebbal Village Ward 2',
        'latitude': '13.0358',
        'longitude': '77.5970'
    }

    res = client.post('/new-complaint', headers={'X-Requested-With': 'XMLHttpRequest', 'Accept': 'application/json'}, data=valid_payload)
    assert res.status_code == 200, f"Expected 200, got {res.status_code}: {res.data}"
    data = json.loads(res.data.decode('utf-8'))
    assert data.get('success') is True
    assert data.get('is_supported') is True
    assert 'complaint_id' in data
    assert data.get('department') == 'ELECTRICITY'
    assert 'Streetlight' in data.get('category')
    assert data.get('status') == 'Pending'
    assert 'demo_sms' in data
    assert 'Govt of Karnataka - GrievanceConnect' in data['demo_sms']['text']
    
    cid = data['complaint_id']
    print(f"[PASS] TEST 6 PASSED: Complaint #{cid} auto-created, mapped to ELECTRICITY, demo SMS generated.")

    # TEST 7: TIME-BASED AUTO STATUS PROGRESSION & MANUAL STATUS
    print("\n[TEST 7] Testing Time-Based Auto Status Progression (0-10m: Pending, 10-20m: In Progress, >20m: Resolved)...")
    with app.app_context():
        db = get_db()
        # Set complaint to 5 mins ago
        five_ago = (datetime.utcnow() - timedelta(minutes=5)).strftime('%Y-%m-%d %H:%M:%S')
        db.execute("UPDATE complaints SET created_at = ?, manual_status = 0 WHERE id = ?", (five_ago, cid))
        db.commit()
        sync_automatic_statuses(db)
        status_5 = db.execute("SELECT status FROM complaints WHERE id = ?", (cid,)).fetchone()['status']
        assert status_5 == 'Pending', f"Expected Pending for 5 min old complaint, got {status_5}"

        # Set complaint to 15 mins ago
        fifteen_ago = (datetime.utcnow() - timedelta(minutes=15)).strftime('%Y-%m-%d %H:%M:%S')
        db.execute("UPDATE complaints SET created_at = ?, manual_status = 0 WHERE id = ?", (fifteen_ago, cid))
        db.commit()
        sync_automatic_statuses(db)
        status_15 = db.execute("SELECT status FROM complaints WHERE id = ?", (cid,)).fetchone()['status']
        assert status_15 == 'In Progress', f"Expected In Progress for 15 min old complaint, got {status_15}"

        # Set complaint to 25 mins ago
        twentyfive_ago = (datetime.utcnow() - timedelta(minutes=25)).strftime('%Y-%m-%d %H:%M:%S')
        db.execute("UPDATE complaints SET created_at = ?, manual_status = 0 WHERE id = ?", (twentyfive_ago, cid))
        db.commit()
        sync_automatic_statuses(db)
        status_25 = db.execute("SELECT status FROM complaints WHERE id = ?", (cid,)).fetchone()['status']
        assert status_25 == 'Resolved', f"Expected Resolved for 25 min old complaint, got {status_25}"

        # Test Authority Manual Override to Rejected/Cancelled
        with client.session_transaction() as sess:
            sess['role'] = 'admin'
            sess['user_id'] = 1

        res = client.post(f'/admin/complaint/{cid}/status', json={'status': 'Rejected/Cancelled'})
        assert res.status_code == 200
        
        # Verify manual status protected against auto-sync
        sync_automatic_statuses(db)
        status_manual = db.execute("SELECT status, manual_status FROM complaints WHERE id = ?", (cid,)).fetchone()
        assert status_manual['status'] == 'Rejected/Cancelled'
        assert status_manual['manual_status'] == 1
    print("[PASS] TEST 7 PASSED: Auto-status progression works accurately and manual status is preserved.")

    # TEST 8: CITIZEN DASHBOARD
    print("\n[TEST 8] Testing Citizen Dashboard...")
    with client.session_transaction() as sess:
        sess['user_id'] = 1
        sess['user_name'] = 'Test Citizen'
        sess['role'] = 'citizen'

    res = client.get('/dashboard')
    assert res.status_code == 200
    html = res.data.decode('utf-8')
    assert f"#{cid}" in html
    assert "ELECTRICITY" in html
    assert "Rejected/Cancelled" in html
    assert "filterComplaints" in html
    print("[PASS] TEST 8 PASSED: Citizen dashboard accurately displays complaint history and statuses.")

    print("\n==================================================")
    print("ALL TESTS COMPLETED SUCCESSFULLY! SYSTEM READY.")
    print("==================================================")

if __name__ == '__main__':
    run_tests()
