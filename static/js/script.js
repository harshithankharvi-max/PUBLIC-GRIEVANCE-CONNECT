const STORAGE_KEY = 'grievance_language';

const translations = {
    en: {
        'GrievanceConnect': 'GrievanceConnect',
        'Home': 'Home',
        'Complaints': 'Complaints',
        'Complaint': 'Complaint',
        'Login': 'Login',
        'Register': 'Register',
        'Dashboard': 'Dashboard',
        'Submit Complaint': 'Submit Complaint',
        'My Complaints': 'My Complaints',
        'Analytics': 'Analytics',
        'Voice Reporting': 'Voice Reporting',
        'Logout': 'Logout',
        'File Complaint': 'File Complaint',
        'View Dashboard': 'View Dashboard',
        'Fast Reporting': 'Fast Reporting',
        'Live Tracking': 'Live Tracking',
        'Admin Oversight': 'Admin Oversight',
        'Create Account': 'Create Account',
        'Email': 'Email',
        'Password': 'Password',
        'Phone Number': 'Phone Number',
        'Full Name': 'Full Name',
        'Citizen Login': 'Citizen Login',
        'Admin Login': 'Admin Login',
        'Master Admin Login': 'Master Admin Login',
        'Authority Login': 'Authority Login',
        'Send OTP': 'Send OTP',
        'Verify OTP': 'Verify OTP',
        'Resend OTP': 'Resend OTP',
        'All Complaints': 'All Complaints',
        'Latest': 'Latest',
        'By Priority': 'By Priority',
        'By Status': 'By Status',
        'Title': 'Title',
        'Category': 'Category',
        'Department': 'Department',
        'Priority': 'Priority',
        'Status': 'Status',
        'Action': 'Action',
        'Details': 'Details',
        'Location': 'Location',
        'Get Current Location': 'Get Current Location',
        'AI Analysis': 'AI Analysis',
        'Language': 'Language',
        'English': 'English',
        'ಕನ್ನಡ': 'ಕನ್ನಡ',
        'Submit': 'Submit',
        'Cancel': 'Cancel',
        'Close': 'Close',
        'Pending': 'Pending',
        'In Progress': 'In Progress',
        'Resolved': 'Resolved',
        'Submitted': 'Submitted',
        'Under Review': 'Under Review',
        'High Priority': 'High Priority',
        'Medium Priority': 'Medium Priority',
        'Low Priority': 'Low Priority',
        'Voice Report': 'Voice Report',
        'Use Voice': 'Use Voice',
        'Total Complaints': 'Total Complaints',
        'Recent Grievances': 'Recent Grievances',
        'View all': 'View all',
        'Date': 'Date',
        'Submitted by': 'Submitted by',
        'Complaint ID': 'Complaint ID',
        'High': 'High',
        'Medium': 'Medium',
        'Low': 'Low',
        'Description': 'Description',
        'Electricity / Power Supply': 'Electricity / Power Supply',
        'Streetlight': 'Streetlight',
        'Road Damage': 'Road Damage',
        'Drainage / Public Infrastructure': 'Drainage / Public Infrastructure',
        'Water Supply': 'Water Supply',
        'Water Leakage / Pipeline': 'Water Leakage / Pipeline',
        'Water Quality / Contamination': 'Water Quality / Contamination',
        'Other PWD / Public Infrastructure': 'Other PWD / Public Infrastructure',
        'ELECTRICITY': 'ELECTRICITY',
        'PWD': 'PWD',
        'WATER': 'WATER',
        'ELECTRICITY DEPARTMENT': 'ELECTRICITY DEPARTMENT',
        'PWD INFRASTRUCTURE': 'PWD INFRASTRUCTURE',
        'WATER & SANITATION': 'WATER & SANITATION',
        'HIGH': 'HIGH',
        'MEDIUM': 'MEDIUM',
        'LOW': 'LOW',
        'HIGH HAZARD': 'HIGH HAZARD',
        'Direct Citizen Filing': 'Direct Citizen Filing',
        'File Grievance': 'File Grievance',
        'Instant Citizen Report': 'Instant Citizen Report',
        'Skip Login / Continue': 'Skip Login / Continue',
        'Open Electricity Portal': 'Open Electricity Portal',
        'Open PWD Portal': 'Open PWD Portal',
        'Open Water Portal': 'Open Water Portal',
        'Master Overview': 'Master Overview',
        'Close & Modify Grievance': 'Close & Modify Grievance',
        'Understood': 'Understood',
        'Pending Review': 'Pending Review',
        'Pending Action': 'Pending Action',
        'High Priority Hazards': 'High Priority Hazards',
        'Department Redressal Cell': 'Department Redressal Cell',
        'Authority Governance Portal': 'Authority Governance Portal',
        'Rural Grievance Redressal Command Center': 'Rural Grievance Redressal Command Center',
        'Geospatial Grievance GIS Map': 'Geospatial Grievance GIS Map',
        'Complaint Details': 'Complaint Details',
        'Resolution Status': 'Resolution Status',
        'Update Status': 'Update Status',
        'Save': 'Save',
        'Update': 'Update',
        'Back to Home': 'Back to Home',
        '← Back to Home': '← Back to Home',
        'Back to Dashboard': 'Back to Dashboard',
        '← Back to Dashboard': '← Back to Dashboard',
        'Citizen Login Portal': 'Citizen Login Portal',
        'Citizen Registration': 'Citizen Registration',
        'Sign in to track and submit your grievances': 'Sign in to track and submit your grievances',
        'Email Address': 'Email Address',
        'Enter your registered email': 'Enter your registered email',
        'Enter your password': 'Enter your password',
        'Sign In': 'Sign In',
        'Sign In →': 'Sign In →',
        "Don't have an account?": "Don't have an account?",
        'Create Account →': 'Create Account →',
        'Login with Phone Number (OTP)': 'Login with Phone Number (OTP)',
        'Register to file and track your village grievances': 'Register to file and track your village grievances',
        'Create a strong password': 'Create a strong password',
        'Enter your phone number (optional)': 'Enter your phone number (optional)'
    },
    kn: {
        'GrievanceConnect': 'ಗ್ರಿವಾನ್ಸ್‌ಕನೆಕ್ಟ್',
        'Home': 'ಮುಖಪುಟ',
        'Complaints': 'ದೂರುಗಳು',
        'Complaint': 'ದೂರು',
        'Login': 'ಲಾಗಿನ್',
        'Register': 'ನೋಂದಣಿ',
        'Dashboard': 'ಡ್ಯಾಶ್‌ಬೋರ್ಡ್',
        'Submit Complaint': 'ದೂರು ಸಲ್ಲಿಸಿ',
        'My Complaints': 'ನನ್ನ ದೂರುಗಳು',
        'Analytics': 'ವಿಶ್ಲೇಷಣೆ',
        'Voice Reporting': 'ಧ್ವನಿ ವರದಿ',
        'Logout': 'ಲಾಗ್ಔಟ್',
        'File Complaint': 'ದೂರು ದಾಖಲಿಸಿ',
        'View Dashboard': 'ಡ್ಯಾಶ್‌ಬೋರ್ಡ್ ವೀಕ್ಷಿಸಿ',
        'Fast Reporting': 'ತ್ವರಿತ ವರದಿ',
        'Live Tracking': 'ನೈಜ-ಸಮಯದ ಪ್ರಗತಿ',
        'Admin Oversight': 'ಪ್ರಾಧಿಕಾರದ ಮೇಲ್ವಿಚಾರಣೆ',
        'Create Account': 'ಖಾತೆ ತೆರೆಯಿರಿ',
        'Email': 'ಇಮೇಲ್',
        'Password': 'ಪಾಸ್‌ವರ್ಡ್',
        'Phone Number': 'ಮೊಬೈಲ್ ಸಂಖ್ಯೆ',
        'Full Name': 'ಪೂರ್ಣ ಹೆಸರು',
        'Enter your full name': 'ನಿಮ್ಮ ಪೂರ್ಣ ಹೆಸರನ್ನು ನಮೂದಿಸಿ',
        'Enter your email': 'ನಿಮ್ಮ ಇಮೇಲ್ ನಮೂದಿಸಿ',
        'Enter your phone number': 'ನಿಮ್ಮ ಮೊಬೈಲ್ ಸಂಖ್ಯೆ ನಮೂದಿಸಿ',
        'Create a password': 'ಪಾಸ್‌ವರ್ಡ್ ರಚಿಸಿ',
        'Enter your password': 'ನಿಮ್ಮ ಪಾಸ್‌ವರ್ಡ್ ನಮೂದಿಸಿ',
        'Citizen Login': 'ನಾಗರಿಕ ಲಾಗಿನ್',
        'Admin Login': 'ಅಧಿಕಾರಿ ಲಾಗಿನ್',
        'Master Admin Login': 'ಮುಖ್ಯ ಅಡ್ಮಿನ್ ಲಾಗಿನ್',
        'Authority Login': 'ಪ್ರಾಧಿಕಾರ ಲಾಗಿನ್',
        'Send OTP': 'ಒಟಿಪಿ ಕಳುಹಿಸಿ',
        'Verify OTP': 'ಒಟಿಪಿ ಪರಿಶೀಲಿಸಿ',
        'Enter the 6-digit OTP sent to your phone': 'ನಿಮ್ಮ ಫೋನ್‌ಗೆ ಕಳುಹಿಸಲಾದ 6 ಅಂಕಿಯ ಒಟಿಪಿಯನ್ನು ನಮೂದಿಸಿ',
        'OTP Code': 'ಒಟಿಪಿ ಕೋಡ್',
        'Resend OTP': 'ಒಟಿಪಿ ಮರುಕಳುಹಿಸಿ',
        'Use different number': 'ಬೇರೆ ಸಂಖ್ಯೆ ಬಳಸಿ',
        'All Complaints': 'ಎಲ್ಲಾ ದೂರುಗಳು',
        'Latest': 'ಇತ್ತೀಚಿನವು',
        'By Priority': 'ಆದ್ಯತೆ ಪ್ರಕಾರ',
        'By Status': 'ಸ್ಥಿತಿ ಪ್ರಕಾರ',
        'Title': 'ಶೀರ್ಷಿಕೆ',
        'Category': 'ವರ್ಗ',
        'Department': 'ಇಲಾಖೆ',
        'Priority': 'ಆದ್ಯತೆ',
        'Status': 'ಸ್ಥಿತಿ',
        'Action': 'ಕ್ರಮ',
        'Details': 'ವಿವರಗಳು',
        'No complaints available.': 'ಯಾವುದೇ ದೂರುಗಳು ಲಭ್ಯವಿಲ್ಲ.',
        'Complaint Title': 'ದೂರಿನ ಶೀರ್ಷಿಕೆ',
        'Brief title of your complaint': 'ದೂರಿನ ಸಂಕ್ಷಿಪ್ತ ಶೀರ್ಷಿಕೆ',
        'Where did this issue occur?': 'ಈ ಸಮಸ್ಯೆ ಎಲ್ಲಿ ಸಂಭವಿಸಿದೆ?',
        'Describe the issue in detail...': 'ಸಮಸ್ಯೆಯನ್ನು ವಿವರವಾಗಿ ವಿವರಿಸಿ...',
        'Location': 'ಸ್ಥಳ',
        'Get Current Location': 'ಪ್ರಸ್ತುತ ಸ್ಥಳವನ್ನು ಪಡೆಯಿರಿ',
        'AI Analysis': 'AI ವಿಶ್ಲೇಷಣೆ',
        'Category:': 'ವರ್ಗ:',
        'Department:': 'ಇಲಾಖೆ:',
        'Priority Level:': 'ಆದ್ಯತೆಯ ಮಟ್ಟ:',
        'Confidence:': 'ವಿಶ್ವಾಸಾರ್ಹತೆ:',
        'Attach Image (optional)': 'ಚಿತ್ರ ಲಗತ್ತಿಸಿ (ಐಚ್ಛಿಕ)',
        'Language': 'ಭಾಷೆ',
        'English': 'English',
        'ಕನ್ನಡ': 'ಕನ್ನಡ',
        'Submit': 'ಸಲ್ಲಿಸಿ',
        'Cancel': 'ರದ್ದುಮಾಡಿ',
        'Close': 'ಮುಚ್ಚಿ',
        'Pending': 'ಬಾಕಿ ಇದೆ',
        'In Progress': 'ಪ್ರಗತಿಯಲ್ಲಿದೆ',
        'Resolved': 'ಪರಿಹರಿಸಲಾಗಿದೆ',
        'Submitted': 'ಸಲ್ಲಿಸಲಾಗಿದೆ',
        'Under Review': 'ಪರಿಶೀಲನೆಯಲ್ಲಿದೆ',
        'High Priority': 'ಅತ್ಯಂತ ತುರ್ತು',
        'Medium Priority': 'ಮಧ್ಯಮ ಆದ್ಯತೆ',
        'Low Priority': 'ಕಡಿಮೆ ಆದ್ಯತೆ',
        'Voice Report': 'ಧ್ವನಿ ವರದಿ',
        'Use Voice': 'ಧ್ವನಿ ಬಳಸಿ',
        'AI civic platform': 'AI ನಾಗರಿಕ ವೇದಿಕೆ',
        'Public service overview and issue monitoring': 'ಸಾರ್ವಜನಿಕ ಸೇವಾ ಅವಲೋಕನ ಮತ್ತು ನಿಗಾ',
        'Search issues': 'ಸಮಸ್ಯೆ ಹುಡುಕಿ',
        'Notifications': 'ಸೂಚನೆಗಳು',
        'Citizen': 'ನಾಗರಿಕ',
        'User': 'ಬಳಕೆದಾರ',
        'Total Complaints': 'ಒಟ್ಟು ದೂರುಗಳು',
        'Needs review': 'ಪರಿಶೀಲನೆ ಅಗತ್ಯವಿದೆ',
        'Assigned': 'ನಿಯೋಜಿಸಲಾಗಿದೆ',
        'Completed': 'ಪೂರ್ಣಗೊಂಡಿದೆ',
        'Urgent': 'ತುರ್ತು',
        'Live feed': 'ಲೈವ್ ಫೀಡ್',
        'Analytics Overview': 'ವಿಶ್ಲೇಷಣೆ ಅವಲೋಕನ',
        'Clear Filters': 'ಫಿಲ್ಟರ್ ತೆರವುಗೊಳಿಸಿ',
        'All': 'ಎಲ್ಲಾ',
        'Voice': 'ಧ್ವನಿ',
        'Recent Grievances': 'ಇತ್ತೀಚಿನ ದೂರುಗಳು',
        'View all': 'ಎಲ್ಲವನ್ನೂ ವೀಕ್ಷಿಸಿ',
        'Date': 'ದಿನಾಂಕ',
        'Submitted by': 'ದಾಖಲಿಸಿದವರು',
        'Complaint ID': 'ದೂರಿನ ಸಂಖ್ಯೆ',
        'High': 'ಅತ್ಯಂತ ತುರ್ತು',
        'Medium': 'ಮಧ್ಯಮ',
        'Low': 'ಸಾಮಾನ್ಯ',
        'Description': 'ವಿವರಣೆ',
        'Status:': 'ಸ್ಥಿತಿ:',
        'Language:': 'ಭಾಷೆ:',
        'Kannada': 'ಕನ್ನಡ',
        'Step 1: Describe the Civic Issue': 'ಹಂತ 1: ಸಾರ್ವಜನಿಕ ಸಮಸ್ಯೆಯನ್ನು ವಿವರಿಸಿ',
        'Step 2: Voice Input (Natural Auto-Stop)': 'ಹಂತ 2: ಧ್ವನಿ ಮೂಲಕ ದೂರು (ಸ್ವಯಂಚಾಲಿತ ನಿಲುಗಡೆ)',
        'Step 3: Location Details (GPS or Manual)': 'ಹಂತ 3: ಸ್ಥಳದ ವಿವರಗಳು (ಜಿಪಿಎಸ್ ಅಥವಾ ಹಸ್ತಚಾಲಿತ)',
        'Step 4: AI Classification & Authority Routing Preview': 'ಹಂತ 4: AI ವರ್ಗೀಕರಣ ಮತ್ತು ಇಲಾಖಾ ನಿಯೋಜನೆ',
        'Step 5: Evidence Photo (Optional)': 'ಹಂತ 5: ಸಾಕ್ಷ್ಯಚಿತ್ರ (ಐಚ್ಛಿಕ)',
        'Submit Grievance to Authority': 'ಪ್ರಾಧಿಕಾರಕ್ಕೆ ದೂರು ಸಲ್ಲಿಸಿ',
        'START VOICE COMPLAINT': 'ಧ್ವನಿ ದೂರು ಪ್ರಾರಂಭಿಸಿ',
        'Stop Recording': 'ರೆಕಾರ್ಡಿಂಗ್ ನಿಲ್ಲಿಸಿ',
        'Listening... Speak naturally': 'ಆಲಿಸುತ್ತಿದೆ... ಮುಕ್ತವಾಗಿ ಮಾತನಾಡಿ',
        'Use Current GPS Location': 'ಪ್ರಸ್ತುತ ಜಿಪಿಎಸ್ ಸ್ಥಳ ಬಳಸಿ',
        'Or Enter Location Manually': 'ಅಥವಾ ಸ್ಥಳವನ್ನು ನೇರವಾಗಿ ನಮೂದಿಸಿ',
        'Detecting GPS location...': 'ಜಿಪಿಎಸ್ ಸ್ಥಳ ಪತ್ತೆಹಚ್ಚಲಾಗುತ್ತಿದೆ...',
        'GPS Location Captured': 'ಜಿಪಿಎಸ್ ಸ್ಥಳ ದಾಖಲಾಗಿದೆ',
        'GPS Coordinates Verified': 'ಜಿಪಿಎಸ್ ನಿರ್ದೇಶಾಂಕಗಳು ದೃಢೀಕರಿಸಲ್ಪಟ್ಟಿವೆ',
        'Electricity / Power Supply': 'ವಿದ್ಯುತ್ / ವಿದ್ಯುತ್ ಸರಬರಾಜು',
        'Streetlight': 'ಬೀದಿ ದೀಪ',
        'Road Damage': 'ರಸ್ತೆ ಹಾನಿ',
        'Drainage / Public Infrastructure': 'ಚರಂಡಿ / ಸಾರ್ವಜನಿಕ ಮೂಲಸೌಕರ್ಯ',
        'Water Supply': 'ಕುಡಿಯುವ ನೀರು ಸರಬರಾಜು',
        'Water Leakage / Pipeline': 'ನೀರು ಸೋರಿಕೆ / ಪೈಪ್‌ಲೈನ್',
        'Water Quality / Contamination': 'ನೀರಿನ ಗುಣಮಟ್ಟ / ಮಾಲಿನ್ಯ',
        'Other PWD / Public Infrastructure': 'ಇತರ ಲೋಕೋಪಯೋಗಿ ಮೂಲಸೌಕರ್ಯ',
        'ELECTRICITY': 'ವಿದ್ಯುತ್ ಇಲಾಖೆ',
        'PWD': 'ಲೋಕೋಪಯೋಗಿ ಇಲಾಖೆ (PWD)',
        'WATER': 'ಜಲಮಂಡಳಿ ಮತ್ತು ನೈರ್ಮಲ್ಯ',
        'ELECTRICITY DEPARTMENT': 'ವಿದ್ಯುತ್ ಇಲಾಖೆ',
        'PWD INFRASTRUCTURE': 'ಲೋಕೋಪಯೋಗಿ ಇಲಾಖೆ (PWD)',
        'WATER & SANITATION': 'ಜಲಮಂಡಳಿ ಮತ್ತು ನೈರ್ಮಲ್ಯ',
        'Electricity Department Portal': 'ವಿದ್ಯುತ್ ಇಲಾಖೆ ಪೋರ್ಟಲ್',
        'Public Works Department (PWD) Portal': 'ಲೋಕೋಪಯೋಗಿ ಇಲಾಖೆ (PWD) ಪೋರ್ಟಲ್',
        'Water & Sanitation Authority Portal': 'ಜಲಮಂಡಳಿ ಮತ್ತು ನೈರ್ಮಲ್ಯ ಇಲಾಖೆ ಪೋರ್ಟಲ್',
        'Electricity Department Authority Login': 'ವಿದ್ಯುತ್ ಇಲಾಖಾ ಪ್ರಾಧಿಕಾರದ ಲಾಗಿನ್',
        'PWD Infrastructure Authority Login': 'ಲೋಕೋಪಯೋಗಿ ಇಲಾಖಾ ಪ್ರಾಧಿಕಾರದ ಲಾಗಿನ್',
        'Water & Sanitation Authority Login': 'ಜಲಮಂಡಳಿ ಪ್ರಾಧಿಕಾರದ ಲಾಗಿನ್',
        'Authorized Personnel Only': 'ಅಧಿಕೃತ ಸಿಬ್ಬಂದಿಗೆ ಮಾತ್ರ ಪ್ರವೇಶ',
        'Department Authority Email': 'ಇಲಾಖಾ ಪ್ರಾಧಿಕಾರದ ಇಮೇಲ್',
        'Authority Password': 'ಪ್ರಾಧಿಕಾರದ ಪಾಸ್‌ವರ್ಡ್',
        'Demonstration Authority Access:': 'ಪ್ರದರ್ಶನ ಪ್ರಾಧಿಕಾರದ ಪ್ರವೇಶ ವಿವರಗಳು:',
        'Officer Email:': 'ಅಧಿಕಾರಿಯ ಇಮೇಲ್:',
        'Default Password:': 'ಪಾಸ್‌ವರ್ಡ್:',
        'HIGH': 'ಅತ್ಯಂತ ತುರ್ತು (High)',
        'MEDIUM': 'ಮಧ್ಯಮ (Medium)',
        'LOW': 'ಸಾಮಾನ್ಯ (Low)',
        'HIGH HAZARD': 'ಅತ್ಯಂತ ತುರ್ತು ಅಪಾಯ',
        'Direct Citizen Filing': 'ನೇರ ನಾಗರಿಕ ಸಲ್ಲಿಕೆ',
        'File Grievance': 'ದೂರು ದಾಖಲಿಸಿ',
        'Instant Citizen Report': 'ತಕ್ಷಣದ ನಾಗರಿಕ ವರದಿ',
        'Skip Login / Continue': 'ಲಾಗಿನ್ ಬಿಟ್ಟು ಮುಂದುವರಿಯಿರಿ',
        'Open Electricity Portal': 'ವಿದ್ಯುತ್ ಪೋರ್ಟಲ್ ತೆರೆಯಿರಿ',
        'Open PWD Portal': 'ಲೋಕೋಪಯೋಗಿ ಪೋರ್ಟಲ್ ತೆರೆಯಿರಿ',
        'Open Water Portal': 'ಜಲಮಂಡಳಿ ಪೋರ್ಟಲ್ ತೆರೆಯಿರಿ',
        'Master Overview': 'ಮುಖ್ಯ ಅವಲೋಕನ',
        'Authority Login': 'ಅಧಿಕಾರಿ ಲಾಗಿನ್',
        'Close & Modify Grievance': 'ಮುಚ್ಚಿ ಮತ್ತು ದೂರು ತಿದ್ದಿ',
        'Understood': 'ಅರ್ಥವಾಯಿತು',
        'Pending Review': 'ಪರಿಶೀಲನೆ ಬಾಕಿ',
        'Pending Action': 'ಕ್ರಮ ಬಾಕಿ',
        'High Priority Hazards': 'ಅತ್ಯಂತ ತುರ್ತು ಅಪಾಯಗಳು',
        'High Priority': 'ಅತ್ಯಂತ ತುರ್ತು',
        'Department Redressal Cell': 'ಇಲಾಖಾ ಪರಿಹಾರ ಕೋಶ',
        'Authority Governance Portal': 'ಪ್ರಾಧಿಕಾರ ಆಡಳಿತ ಪೋರ್ಟಲ್',
        'Karnataka Panchayat Raj & Rural Development': 'ಕರ್ನಾಟಕ ಪಂಚಾಯತ್ ರಾಜ್ ಮತ್ತು ಗ್ರಾಮೀಣಾಭಿವೃದ್ಧಿ',
        'District Grievance Redressal Authority | Officer Command Center': 'ಜಿಲ್ಲಾ ಕುಂದುಕೊರತೆ ನಿವಾರಣಾ ಪ್ರಾಧಿಕಾರ | ಕಮಾಂಡ್ ಸೆಂಟರ್',
        'Rural Grievance Redressal Command Center': 'ಗ್ರಾಮೀಣ ಸಾರ್ವಜನಿಕ ಕುಂದುಕೊರತೆ ನಿವಾರಣಾ ಕಮಾಂಡ್ ಸೆಂಟರ್',
        'Geospatial Grievance GIS Map': 'ಭೌಗೋಳಿಕ ಜಿಐಎಸ್ ನಕ್ಷೆ',
        'Interactive spatial map plotting reported rural grievances across Karnataka Gram Panchayats': 'ಕರ್ನಾಟಕದ ಗ್ರಾಮ ಪಂಚಾಯಿತಿಗಳ ವ್ಯಾಪ್ತಿಯಲ್ಲಿ ವರದಿಯಾದ ಗ್ರಾಮೀಣ ದೂರುಗಳ ಸಂವಾದಾತ್ಮಕ ನಕ್ಷೆ',
        'System-Wide Grievances Registry (ಸಮಗ್ರ ದೂರುಗಳು)': 'ಸಮಗ್ರ ಸಾರ್ವಜನಿಕ ದೂರುಗಳ ನೋಂದಣಿ ಪುಸ್ತಕ',
        'Review, update resolution status, or inspect detailed evidence for every rural grievance.': 'ಪ್ರತಿಯೊಂದು ಗ್ರಾಮೀಣ ದೂರಿನ ವಿವರ ಪರಿಶೀಲಿಸಿ, ಪರಿಹಾರ ಸ್ಥಿತಿಯನ್ನು ನವೀಕರಿಸಿ.',
        'Complaint Details': 'ದೂರಿನ ವಿವರಗಳು',
        'Resolution Status': 'ಪರಿಹಾರ ಸ್ಥಿತಿ',
        'Update Status': 'ಸ್ಥಿತಿಯನ್ನು ನವೀಕರಿಸಿ',
        'Save': 'ಉಳಿಸಿ',
        'Update': 'ನವೀಕರಿಸಿ',
        'Details →': 'ವಿವರಗಳು →',
        'Details': 'ವಿವರಗಳು',
        'Assigned Categories:': 'ನಿಯೋಜಿತ ವರ್ಗಗಳು:',
        'Assigned Authority:': 'ನಿಯೋಜಿತ ಪ್ರಾಧಿಕಾರ:',
        'Assigned Department:': 'ನಿಯೋಜಿತ ಇಲಾಖೆ:',
        'Assigned Authority': 'ನಿಯೋಜಿತ ಪ್ರಾಧಿಕಾರ',
        'Assigned Department': 'ನಿಯೋಜಿತ ಇಲಾಖೆ',
        'Hazard Priority': 'ಅಪಾಯದ ಆದ್ಯತೆ',
        'Priority Hazard': 'ಆದ್ಯತೆಯ ಅಪಾಯ',
        'Department Complaints': 'ಇಲಾಖೆಯ ದೂರುಗಳು',
        'District Administrative Office': 'ಜಿಲ್ಲಾಡಳಿತ ಕಚೇರಿ',
        'Administrative Officer': 'ಆಡಳಿತಾಧಿಕಾರಿ',
        'AI-enabled Geospatial Public Grievance Redressal System for Rural Areas': 'ಗ್ರಾಮೀಣ ಪ್ರದೇಶಗಳಿಗಾಗಿ AI-ಆಧಾರಿತ ಭೌಗೋಳಿಕ ಸಾರ್ವಜನಿಕ ಕುಂದುಕೊರತೆ ನಿವಾರಣಾ ವ್ಯವಸ್ಥೆ',
        'Report civic issues via voice in Kannada or English, track real-time GIS status, and get automated department resolution across Karnataka rural panchayats.': 'ಕನ್ನಡ ಅಥವಾ ಇಂಗ್ಲಿಷ್‌ನಲ್ಲಿ ಧ್ವನಿಯ ಮೂಲಕ ನಾಗರಿಕ ಸಮಸ್ಯೆಗಳನ್ನು ವರದಿ ಮಾಡಿ, ನೈಜ-ಸಮಯದ ಜಿಐಎಸ್ ಸ್ಥಿತಿ ಗಮನಿಸಿ ಮತ್ತು ಇಲಾಖಾ ಪರಿಹಾರ ಪಡೆಯಿರಿ.',
        'Phone OTP Authentication': 'ಮೊಬೈಲ್ ಒಟಿಪಿ ಮೂಲಕ ಪ್ರವೇಶ',
        'District Admin & Officers': 'ಜಿಲ್ಲಾಡಳಿತ ಮತ್ತು ಅಧಿಕಾರಿಗಳು',
        'Simple & Transparent': 'ಸರಳ ಮತ್ತು ಪಾರದರ್ಶಕ',
        'How the Rural Grievance Redressal System Works': 'ಗ್ರಾಮೀಣ ದೂರು ನಿವಾರಣಾ ವ್ಯವಸ್ಥೆ ಹೇಗೆ ಕಾರ್ಯನಿರ್ವಹಿಸುತ್ತದೆ',
        'A step-by-step workflow designed for rural accessibility and immediate authority action.': 'ಗ್ರಾಮೀಣ ಜನರಿಗೆ ಸುಲಭವಾಗಿ ತಲುಪುವ ಮತ್ತು ತ್ವರಿತ ಕ್ರಮ ಕೈಗೊಳ್ಳುವ ಹಂತ-ಹಂತದ ಕಾರ್ಯವಿಧಾನ.',
        'Dedicated Portals': 'ಮೀಸಲಾದ ಪೋರ್ಟಲ್‌ಗಳು',
        'Three Core Authority Departments': 'ಮೂರು ಪ್ರಮುಖ ಪ್ರಾಧಿಕಾರ ಇಲಾಖೆಗಳು',
        'All 8 rural grievance categories are organized under 3 principal administrative portals for efficient governance.': 'ಎಲ್ಲಾ 8 ಗ್ರಾಮೀಣ ದೂರು ವರ್ಗಗಳನ್ನು ದಕ್ಷ ಆಡಳಿತಕ್ಕಾಗಿ 3 ಪ್ರಮುಖ ಪೋರ್ಟಲ್‌ಗಳ ಅಡಿಯಲ್ಲಿ ಸಂಘಟಿಸಲಾಗಿದೆ.',
        'Three Core Authority Department Portals': 'ಮೂರು ಪ್ರಮುಖ ಪ್ರಾಧಿಕಾರ ಇಲಾಖಾ ಪೋರ್ಟಲ್‌ಗಳು',
        'Direct Department Dispatch': 'ನೇರ ಇಲಾಖಾ ರವಾನೆ',
        'Click any department portal to access dedicated complaint lists, officer resolution tools, and specialized categories.': 'ಪ್ರತ್ಯೇಕ ದೂರು ಪಟ್ಟಿ, ಪರಿಹಾರ ಪರಿಕರಗಳು ಮತ್ತು ವರ್ಗಗಳನ್ನು ವೀಕ್ಷಿಸಲು ಇಲಾಖಾ ಪೋರ್ಟಲ್ ಆಯ್ಕೆಮಾಡಿ.',
        '← Back to Master Overview': '← ಮುಖ್ಯ ಅವಲೋಕನ',
        '← Back to Master Dashboard': '← ಮುಖ್ಯ ಡ್ಯಾಶ್‌ಬೋರ್ಡ್‌ಗೆ ಹಿಂತಿರುಗಿ',
        '← Back to Admin Command Center': '← ಅಡ್ಮಿನ್ ಕಮಾಂಡ್ ಸೆಂಟರ್‌ಗೆ ಹಿಂತಿರುಗಿ',
        '← Back to Dashboard': '← ಡ್ಯಾಶ್‌ಬೋರ್ಡ್‌ಗೆ ಹಿಂತಿರುಗಿ',
        '← Return to GrievanceConnect Home': '← ಮುಖಪುಟಕ್ಕೆ ಹಿಂತಿರುಗಿ',
        'Back to Home': 'ಮುಖಪುಟಕ್ಕೆ ಹಿಂತಿರುಗಿ',
        '← Back to Home': '← ಮುಖಪುಟಕ್ಕೆ ಹಿಂತಿರುಗಿ',
        'Back to Dashboard': 'ಡ್ಯಾಶ್‌ಬೋರ್ಡ್‌ಗೆ ಹಿಂತಿರುಗಿ',
        'Citizen Login Portal': 'ನಾಗರಿಕ ಲಾಗಿನ್ ಪೋರ್ಟಲ್',
        'Citizen Registration': 'ನಾಗರಿಕ ನೋಂದಣಿ',
        'Sign in to track and submit your grievances': 'ನಿಮ್ಮ ದೂರುಗಳನ್ನು ಸಲ್ಲಿಸಲು ಮತ್ತು ಸ್ಥಿತಿ ಪರಿಶೀಲಿಸಲು ಲಾಗಿನ್ ಮಾಡಿ',
        'Email Address': 'ಇಮೇಲ್ ವಿಳಾಸ',
        'Enter your registered email': 'ನಿಮ್ಮ ನೋಂದಾಯಿತ ಇಮೇಲ್ ನಮೂದಿಸಿ',
        'Enter your password': 'ನಿಮ್ಮ ಪಾಸ್‌ವರ್ಡ್ ನಮೂದಿಸಿ',
        'Sign In': 'ಸೈನ್ ಇನ್',
        'Sign In →': 'ಸೈನ್ ಇನ್ →',
        "Don't have an account?": 'ಖಾತೆ ಇಲ್ಲವೇ?',
        'Create Account →': 'ಖಾತೆ ರಚಿಸಿ →',
        'Login with Phone Number (OTP)': 'ದೂರವಾಣಿ ಸಂಖ್ಯೆಯೊಂದಿಗೆ ಲಾಗಿನ್ ಮಾಡಿ (OTP)',
        'Register to file and track your village grievances': 'ನಿಮ್ಮ ಗ್ರಾಮದ ದೂರುಗಳನ್ನು ದಾಖಲಿಸಲು ನೋಂದಣಿ ಮಾಡಿ',
        'Create a strong password': 'ಬಲವಾದ ಪಾಸ್‌ವರ್ಡ್ ರಚಿಸಿ',
        'Enter your phone number (optional)': 'ದೂರವಾಣಿ ಸಂಖ್ಯೆ ನಮೂದಿಸಿ (ಐಚ್ಛಿಕ)',
        'Quick Portals': 'ತ್ವರಿತ ಪೋರ್ಟಲ್‌ಗಳು',
        'Government Grievance System': 'ಸರ್ಕಾರಿ ಕುಂದುಕೊರತೆ ನಿವಾರಣಾ ವ್ಯವಸ್ಥೆ',
        'Designed & deployed for rural Karnataka Gram Panchayats with AI and GIS mapping': 'AI ಮತ್ತು GIS ನಕ್ಷೆಯೊಂದಿಗೆ ಕರ್ನಾಟಕದ ಗ್ರಾಮೀಣ ಪಂಚಾಯಿತಿಗಳಿಗಾಗಿ ರೂಪಿಸಲಾಗಿದೆ',
        'Unsupported Grievance Notice': 'ಬೆಂಬಲಿಸದ ದೂರಿನ ಸೂಚನೆ',
        'Outside Civic Scope': 'ನಾಗರಿಕ ವ್ಯಾಪ್ತಿಯಿಂದ ಹೊರಗಿದೆ',
        'Sorry, this grievance is outside the supported civic categories of this portal. Please contact the appropriate emergency or concerned authority for assistance.': 'ಕ್ಷಮಿಸಿ, ಈ ದೂರು ಈ ಪೋರ್ಟಲ್‌ನ ಬೆಂಬಲಿತ ನಾಗರಿಕ ವರ್ಗಗಳ ವ್ಯಾಪ್ತಿಯಿಂದ ಹೊರಗಿದೆ. ದಯವಿಟ್ಟು ಸಹಾಯಕ್ಕಾಗಿ ಸೂಕ್ತ ತುರ್ತು ಅಥವಾ ಸಂಬಂಧಿತ ಪ್ರಾಧಿಕಾರವನ್ನು ಸಂಪರ್ಕಿಸಿ.',
        'Uploaded Image': 'ಅಪ್ಲೋಡ್ ಮಾಡಿದ ಚಿತ್ರ',
        'Original voice recording for this complaint': 'ಈ ದೂರಿಗೆ ಸಂಬಂಧಿಸಿದ ಮೂಲ ಧ್ವನಿ ರೆಕಾರ್ಡಿಂಗ್',
        'Voice Based': 'ಧ್ವನಿ ಆಧಾರಿತ',
        'Text Based': 'ಪಠ್ಯ ಆಧಾರಿತ',
        'Location:': 'ಸ್ಥಳ:',
        'By:': 'ದಾಖಲಿಸಿದವರು:',
        'Recent': 'ಇತ್ತೀಚಿನದು',
        'No Grievances Found': 'ಯಾವುದೇ ದೂರುಗಳು ಕಂಡುಬಂದಿಲ್ಲ',
        'All grievances for this department have either been resolved or no new reports have been filed.': 'ಈ ಇಲಾಖೆಯ ಎಲ್ಲಾ ದೂರುಗಳನ್ನು ಪರಿಹರಿಸಲಾಗಿದೆ ಅಥವಾ ಹೊಸ ವರದಿಗಳು ಬಂದಿಲ್ಲ.',
        'Report with Voice or Text': 'ಧ್ವನಿ ಅಥವಾ ಪಠ್ಯದ ಮೂಲಕ ವರದಿ ಮಾಡಿ',
        'Citizens can speak in Kannada or English using natural voice recognition or type their problem description with photos.': 'ನಾಗರಿಕರು ನೈಸರ್ಗಿಕ ಧ್ವನಿ ಗುರುತಿಸುವಿಕೆಯನ್ನು ಬಳಸಿ ಕನ್ನಡ ಅಥವಾ ಇಂಗ್ಲಿಷ್‌ನಲ್ಲಿ ಮಾತನಾಡಬಹುದು ಅಥವಾ ಫೋಟೋಗಳೊಂದಿಗೆ ವಿವರ ಟೈಪ್ ಮಾಡಬಹುದು.',
        'Automated AI Classification': 'ಸ್ವಯಂಚಾಲಿತ AI ವರ್ಗೀಕರಣ',
        'The system evaluates the complaint into one of 8 rural categories and assesses priority (HIGH, MEDIUM, LOW) based on safety hazards.': 'ವ್ಯವಸ್ಥೆಯು ದೂರುಗಳನ್ನು 8 ಗ್ರಾಮೀಣ ವರ್ಗಗಳಲ್ಲಿ ಒಂದಕ್ಕೆ ವರ್ಗೀಕರಿಸುತ್ತದೆ ಮತ್ತು ಸುರಕ್ಷತೆಯ ಅಪಾಯಗಳ ಆಧಾರದ ಮೇಲೆ ಆದ್ಯತೆಯನ್ನು ನಿಗದಿಪಡಿಸುತ್ತದೆ.',
        'Geospatial Location Tagging': 'ಭೌಗೋಳಿಕ ಸ್ಥಳ ಗುರುತಿಸುವಿಕೆ',
        'Captures exact GPS coordinates and reverse-geocodes village/town names, pinpointing the problem on an interactive GIS map.': 'ಖಚಿತವಾದ ಜಿಪಿಎಸ್ ನಿರ್ದೇಶಾಂಕಗಳನ್ನು ಪಡೆದು ಗ್ರಾಮ/ಪಟ್ಟಣದ ಹೆಸರನ್ನು ಗುರುತಿಸಿ ಜಿಐಎಸ್ ನಕ್ಷೆಯಲ್ಲಿ ಪ್ರದರ್ಶಿಸುತ್ತದೆ.',
        'Targeted Department Action': 'ಉದ್ದೇಶಿತ ಇಲಾಖಾ ಕ್ರಮ',
        'Directly dispatched to Electricity, PWD, or Water authorities with real-time status updates from Pending to Resolved.': 'ಬಾಕಿಯಿಂದ ಪರಿಹಾರದವರೆಗೆ ನೈಜ-ಸಮಯದ ಸ್ಥಿತಿ ನವೀಕರಣಗಳೊಂದಿಗೆ ವಿದ್ಯುತ್, ಲೋಕೋಪಯೋಗಿ ಅಥವಾ ಜಲಮಂಡಳಿ ಪ್ರಾಧಿಕಾರಕ್ಕೆ ನೇರವಾಗಿ ರವಾನೆಯಾಗುತ್ತದೆ.',
        'Select Recording Language:': 'ರೆಕಾರ್ಡಿಂಗ್ ಭಾಷೆಯನ್ನು ಆರಿಸಿ:',
        'Speak in Kannada (ಕನ್ನಡ)': 'ಕನ್ನಡದಲ್ಲಿ ಮಾತನಾಡಿ (ಕನ್ನಡ)',
        'Speak in English': 'ಇಂಗ್ಲಿಷ್‌ನಲ್ಲಿ ಮಾತನಾಡಿ (English)',
        'Enter Location Manually (Village / Town / Landmark)': 'ಸ್ಥಳವನ್ನು ನೇರವಾಗಿ ನಮೂದಿಸಿ (ಗ್ರಾಮ / ಪಟ್ಟಣ / ಹೆಗ್ಗುರುತು)',
        'Select Image File (Max 50MB)': 'ಚಿತ್ರ ಫೈಲ್ ಆಯ್ಕೆಮಾಡಿ (ಗರಿಷ್ಠ 50MB)',
        'Attach a photo of the road damage, water leakage, pole hazard or streetlight issue for quicker resolution.': 'ತ್ವರಿತ ಪರಿಹಾರಕ್ಕಾಗಿ ರಸ್ತೆ ಹಾನಿ, ನೀರು ಸೋರಿಕೆ, ಕಂಬದ ಅಪಾಯ ಅಥವಾ ಬೀದಿ ದೀಪದ ಸಮಸ್ಯೆಯ ಫೋಟೋ ಲಗತ್ತಿಸಿ.',
        'AI Live Evaluation': 'AI ನೈಜ-ಸಮಯದ ಮೌಲ್ಯಮಾಪನ',
        'Active Scope:': 'ಸಕ್ರಿಯ ವ್ಯಾಪ್ತಿ:',
        'Valid Civic Grievance': 'ಮಾನ್ಯವಾದ ನಾಗರಿಕ ದೂರು',
        'Predicted Category': 'ಗುರುತಿಸಲಾದ ವರ್ಗ',
        'Assigned Department': 'ನಿಯೋಜಿತ ಇಲಾಖೆ',
        'Safety Hazard Priority': 'ಸುರಕ್ಷತಾ ಅಪಾಯದ ಆದ್ಯತೆ',
        'Confidence Score': 'ವಿಶ್ವಾಸಾರ್ಹತೆ ಸ್ಕೋರ್',
        'Evaluating civic issue details in real-time...': 'ಸಾರ್ವಜನಿಕ ಸಮಸ್ಯೆಯ ವಿವರಗಳನ್ನು ನೈಜ ಸಮಯದಲ್ಲಿ ಮೌಲ್ಯಮಾಪನ ಮಾಡಲಾಗುತ್ತಿದೆ...',
        'Voice recording captured. You can submit now.': 'ಧ್ವನಿ ರೆಕಾರ್ಡಿಂಗ್ ಪೂರ್ಣಗೊಂಡಿದೆ. ಈಗ ನೀವು ಸಲ್ಲಿಸಬಹುದು.',
        'Verified Rural Citizen': 'ದೃಢೀಕೃತ ಗ್ರಾಮೀಣ ನಾಗರಿಕ',
        'Welcome': 'ಸ್ವಾಗತ',
        'Citizen Dashboard': 'ನಾಗರಿಕ ಡ್ಯಾಶ್‌ಬೋರ್ಡ್',
        'Track the resolution status of all your submitted village grievances across Electricity, PWD, and Water departments.': 'ವಿದ್ಯುತ್, ಲೋಕೋಪಯೋಗಿ ಮತ್ತು ಜಲಮಂಡಳಿ ಇಲಾಖೆಗಳಲ್ಲಿ ನೀವು ಸಲ್ಲಿಸಿದ ಎಲ್ಲಾ ಗ್ರಾಮೀಣ ದೂರುಗಳ ಪರಿಹಾರ ಸ್ಥಿತಿಯನ್ನು ಗಮನಿಸಿ.',
        'File New Complaint': 'ಹೊಸ ದೂರು ದಾಖಲಿಸಿ',
        'Voice Report': 'ಧ್ವನಿ ವರದಿ',
        'All registered issues': 'ಎಲ್ಲಾ ದಾಖಲಾದ ಸಮಸ್ಯೆಗಳು',
        'Pending Review': 'ಪರಿಶೀಲನೆ ಬಾಕಿ',
        'Awaiting officer action': 'ಅಧಿಕಾರಿಗಳ ಕ್ರಮಕ್ಕೆ ಕಾಯಲಾಗುತ್ತಿದೆ',
        'Work currently active': 'ಕಾಮಗಾರಿ ಪ್ರಗತಿಯಲ್ಲಿದೆ',
        'Successfully closed': 'ಯಶಸ್ವಿಯಾಗಿ ಮುಕ್ತಾಯಗೊಂಡಿದೆ',
        'My Registered Complaints': 'ನನ್ನ ನೋಂದಾಯಿತ ದೂರುಗಳು',
        'My Registered Complaints (ನನ್ನ ದೂರುಗಳು)': 'ನನ್ನ ನೋಂದಾಯಿತ ದೂರುಗಳು',
        'View and inspect the latest status, department routing, and AI hazard assessment for your reports.': 'ನಿಮ್ಮ ವರದಿಗಳ ಇತ್ತೀಚಿನ ಸ್ಥಿತಿ, ಇಲಾಖಾ ನಿಯೋಜನೆ ಮತ್ತು AI ಅಪಾಯದ ಮೌಲ್ಯಮಾಪನವನ್ನು ಪರಿಶೀಲಿಸಿ.',
        'ID': 'ಸಂಖ್ಯೆ',
        'Complaint Details': 'ದೂರಿನ ವಿವರಗಳು',
        'Category': 'ವರ್ಗ',
        'Department': 'ಇಲಾಖೆ',
        'Priority': 'ಆದ್ಯತೆ',
        'Location': 'ಸ್ಥಳ',
        'Status': 'ಸ್ಥಿತಿ',
        'Date': 'ದಿನಾಂಕ',
        'Action': 'ಕ್ರಮ',
        'Details': 'ವಿವರಗಳು',
        'Details →': 'ವಿವರಗಳು →',
        'No complaints filed yet': 'ಇನ್ನೂ ಯಾವುದೇ ದೂರುಗಳನ್ನು ದಾಖಲಿಸಿಲ್ಲ',
        "You haven't filed any grievances yet. If you have an electricity, water, or road issue in your village, report it now.": 'ನೀವು ಇನ್ನೂ ಯಾವುದೇ ದೂರುಗಳನ್ನು ದಾಖಲಿಸಿಲ್ಲ. ನಿಮ್ಮ ಗ್ರಾಮದಲ್ಲಿ ವಿದ್ಯುತ್, ನೀರು ಅಥವಾ ರಸ್ತೆ ಸಮಸ್ಯೆ ಇದ್ದರೆ ಈಗಲೇ ವರದಿ ಮಾಡಿ.',
        'File Your First Complaint': 'ನಿಮ್ಮ ಮೊದಲ ದೂರನ್ನು ದಾಖಲಿಸಿ',
        'Rejected/Cancelled': 'ತಿರಸ್ಕರಿಸಲಾಗಿದೆ/ರದ್ದುಗೊಳಿಸಲಾಗಿದೆ',
        'Government of Karnataka | Gram Panchayat Citizen Portal': 'ಕರ್ನಾಟಕ ಸರ್ಕಾರ | ಗ್ರಾಮ ಪಂಚಾಯತ್ ನಾಗರಿಕ ಪೋರ್ಟಲ್',
        'Government of Karnataka | Gram Panchayat Grievance Filing': 'ಕರ್ನಾಟಕ ಸರ್ಕಾರ | ಗ್ರಾಮ ಪಂಚಾಯತ್ ದೂರು ದಾಖಲಾತಿ',
        'Government of Karnataka | Gram Panchayat Rural Development Portal': 'ಕರ್ನಾಟಕ ಸರ್ಕಾರ | ಗ್ರಾಮ ಪಂಚಾಯತ್ ಗ್ರಾಮೀಣಾಭಿವೃದ್ಧಿ ಪೋರ್ಟಲ್',
        'Karnataka Panchayat Raj & Rural Development | Authority Portals': 'ಕರ್ನಾಟಕ ಪಂಚಾಯತ್ ರಾಜ್ ಮತ್ತು ಗ್ರಾಮೀಣಾಭಿವೃದ್ಧಿ | ಪ್ರಾಧಿಕಾರ ಪೋರ್ಟಲ್‌ಗಳು',
        'Citizen Portal & Grievance Tracking': 'ನಾಗರಿಕ ಪೋರ್ಟಲ್ ಮತ್ತು ದೂರು ಪರಿಶೀಲನೆ',
        'Citizen Grievance Submission': 'ನಾಗರಿಕ ದೂರು ಸಲ್ಲಿಕೆ',
        'Authority Governance Portals': 'ಪ್ರಾಧಿಕಾರ ಆಡಳಿತ ಪೋರ್ಟಲ್‌ಗಳು',
        'Select Your Authority Department': 'ಪ್ರಾಧಿಕಾರ ಇಲಾಖೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ',
        'Grievance Registered Successfully': 'ದೂರು ಯಶಸ್ವಿಯಾಗಿ ದಾಖಲಾಗಿದೆ',
        'Official Registration ID': 'ಅಧಿಕೃತ ನೋಂದಣಿ ಸಂಖ್ಯೆ',
        'AI Classified Category:': 'AI ಗುರುತಿಸಿದ ವರ್ಗ:',
        'Assigned Department:': 'ನಿಯೋಜಿತ ಇಲಾಖೆ:',
        'Assessed Hazard Priority:': 'ಅಪಾಯದ ಆದ್ಯತೆ:',
        'Registered Location:': 'ದಾಖಲಾದ ಸ್ಥಳ:',
        'Date & Time:': 'ದಿನಾಂಕ ಮತ್ತು ಸಮಯ:',
        'Current Resolution Status:': 'ಪ್ರಸ್ತುತ ಪರಿಹಾರ ಸ್ಥಿತಿ:',
        'Go to Citizen Dashboard →': 'ನಾಗರಿಕ ಡ್ಯಾಶ್‌ಬೋರ್ಡ್‌ಗೆ ಹೋಗಿ →',
        'View Complaint Details': 'ದೂರಿನ ವಿವರಗಳನ್ನು ವೀಕ್ಷಿಸಿ',
        '+ File Another': '+ ಇನ್ನೊಂದು ದೂರು ಸಲ್ಲಿಸಿ',
        'Classify & Submit Grievance / ದೂರು ಸಲ್ಲಿಸಿ': 'ದೂರು ವರ್ಗೀಕರಿಸಿ ಸಲ್ಲಿಸಿ',
        'Clear description': 'ವಿವರಣೆ ತೆರವುಗೊಳಿಸಿ',
        'Clear': 'ತೆರವುಗೊಳಿಸಿ',
    }
};

function getStoredLanguage() {
    try {
        const stored = localStorage.getItem(STORAGE_KEY);
        return stored === 'kn' ? 'kn' : 'en';
    } catch (error) {
        return 'en';
    }
}

function setStoredLanguage(lang) {
    try {
        localStorage.setItem(STORAGE_KEY, lang);
    } catch (error) {
        console.warn('Language persist failed:', error);
    }
}

function normalizeTranslationKey(value = '') {
    return value
        .replace(/[\u2600-\u27BF]/g, '')
        .replace(/[\u2000-\u206F]/g, '')
        .replace(/\s+/g, ' ')
        .trim();
}

/**
 * Strips known emojis/symbols/arrows from prefixes and suffixes,
 * matches the core text against dict, and reconstructs the string.
 */
function findTranslation(rawText, dict) {
    if (!rawText) return null;
    const trimmed = rawText.trim();
    if (!trimmed || trimmed.length < 2) return null;

    // 1. Direct exact match
    if (dict[trimmed]) return dict[trimmed];

    // 2. Separate leading prefix (emojis, icons, symbols, bullets, numbers)
    const prefixRegex = /^([⚡🏗💧🏛📋⏳✅⚙️✓🔴🟡🟢📍🎤🤖🛣🌊🚰🔧🧪⚠️•#*→←↓0-9\s|/:\\-]+)/u;
    let prefix = '';
    let core = trimmed;

    // Try matching if starts with non-letter
    const prefixMatch = trimmed.match(prefixRegex);
    if (prefixMatch && prefixMatch[0].length < trimmed.length) {
        prefix = prefixMatch[0];
        core = trimmed.slice(prefix.length).trim();
    }

    // Separate trailing suffix (e.g. " →", "...", ":", " (Optional)", etc.)
    const suffixRegex = /([\s→←↓✓•#:.]+|\s*\(Optional\)|\s*\(ಐಚ್ಛಿಕ\))$/u;
    let suffix = '';
    const suffixMatch = core.match(suffixRegex);
    if (suffixMatch && suffixMatch[0].length < core.length) {
        suffix = suffixMatch[0];
        core = core.slice(0, core.length - suffix.length).trim();
    }

    if (core && dict[core]) {
        return prefix + dict[core] + suffix;
    }

    // 3. Try with normalized core
    const normalized = normalizeTranslationKey(core);
    if (normalized && dict[normalized]) {
        return prefix + dict[normalized] + suffix;
    }

    // 4. Whole trimmed normalized match
    const fullNormalized = normalizeTranslationKey(trimmed);
    if (fullNormalized && dict[fullNormalized]) {
        return dict[fullNormalized];
    }

    return null;
}

/**
 * Safely translates all Text Nodes in the DOM tree using TreeWalker.
 * Preserves child elements, button handlers, icons, etc.
 */
function translateDOM(root, lang) {
    const dict = translations[lang] || {};

    // 1. Walk text nodes
    const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, null, false);
    let node;
    while ((node = walker.nextNode())) {
        const parent = node.parentElement;
        if (!parent) continue;
        const tag = parent.tagName;
        if (['SCRIPT', 'STYLE', 'CODE'].includes(tag)) continue;

        const val = node.nodeValue;
        if (!val || val.trim().length < 2) continue;

        // Cache original English text on the node
        if (!node.__grievanceOrigText) {
            node.__grievanceOrigText = node.nodeValue;
            node.__grievanceCleanText = val.trim();
        }

        if (lang === 'en') {
            node.nodeValue = node.__grievanceOrigText;
        } else {
            const clean = node.__grievanceCleanText;
            const translated = findTranslation(clean, dict);
            if (translated) {
                node.nodeValue = node.__grievanceOrigText.replace(clean, translated);
            }
        }
    }

    // 2. Translate Form Placeholders
    const inputs = root.querySelectorAll ? root.querySelectorAll('input[placeholder], textarea[placeholder]') : [];
    inputs.forEach(input => {
        if (!input.__grievanceOrigPlaceholder) {
            input.__grievanceOrigPlaceholder = input.getAttribute('placeholder');
        }
        if (lang === 'en') {
            input.setAttribute('placeholder', input.__grievanceOrigPlaceholder);
        } else {
            const tr = findTranslation(input.__grievanceOrigPlaceholder, dict);
            if (tr) input.setAttribute('placeholder', tr);
        }
    });

    // 3. Translate Submit / Button input values
    const btnInputs = root.querySelectorAll ? root.querySelectorAll('input[type="submit"], input[type="button"]') : [];
    btnInputs.forEach(btn => {
        if (!btn.__grievanceOrigValue) {
            btn.__grievanceOrigValue = btn.value;
        }
        if (lang === 'en') {
            btn.value = btn.__grievanceOrigValue;
        } else {
            const tr = findTranslation(btn.__grievanceOrigValue, dict);
            if (tr) btn.value = tr;
        }
    });
}

function applyLanguage(lang) {
    translateDOM(document.body, lang);

    // Update active state on any in-page language switcher pills
    document.querySelectorAll('.lang-pill').forEach(pill => {
        const text = (pill.textContent || '').trim().toLowerCase();
        if ((lang === 'en' && text.includes('english')) || (lang === 'kn' && text.includes('ಕನ್ನಡ'))) {
            pill.classList.add('active');
        } else {
            pill.classList.remove('active');
        }
    });

    setStoredLanguage(lang);
}

window.setLanguage = function(lang) {
    applyLanguage(lang);
};

window.translateElement = function(el) {
    if (!el) return;
    const lang = getStoredLanguage();
    if (lang === 'kn') {
        translateDOM(el, 'kn');
    }
};

function initLanguageToggle() {
    const stored = getStoredLanguage();
    if (stored === 'kn') {
        applyLanguage('kn');
    }
}

document.addEventListener('DOMContentLoaded', () => {
    initLanguageToggle();
});
