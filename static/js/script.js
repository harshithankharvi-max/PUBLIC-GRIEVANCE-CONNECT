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
        'Raise issues. Track progress. Build better communities.': 'Raise issues. Track progress. Build better communities.',
        'GrievanceConnect helps citizens report civic problems, monitor their status, and ensure faster responses from local authorities.': 'GrievanceConnect helps citizens report civic problems, monitor their status, and ensure faster responses from local authorities.',
        'Fast Reporting': 'Fast Reporting',
        'Submit complaints in a few steps with complete details and location.': 'Submit complaints in a few steps with complete details and location.',
        'Live Tracking': 'Live Tracking',
        'Monitor assigned work, issue steps, and progress updates in real time.': 'Monitor assigned work, issue steps, and progress updates in real time.',
        'Admin Oversight': 'Admin Oversight',
        'Authorities can review, resolve, and prioritize complaints efficiently.': 'Authorities can review, resolve, and prioritize complaints efficiently.',
        'Create Account': 'Create Account',
        'Email': 'Email',
        'Password': 'Password',
        'Phone Number': 'Phone Number',
        'Full Name': 'Full Name',
        'Enter your full name': 'Enter your full name',
        'Enter your email': 'Enter your email',
        'Enter your phone number': 'Enter your phone number',
        'Create a password': 'Create a password',
        'Citizen Login': 'Citizen Login',
        'Admin Login': 'Admin Login',
        'Send OTP': 'Send OTP',
        'Verify OTP': 'Verify OTP',
        'Enter the 6-digit OTP sent to your phone': 'Enter the 6-digit OTP sent to your phone',
        'Phone Number': 'Phone Number',
        'OTP Code': 'OTP Code',
        'Resend OTP': 'Resend OTP',
        'Use different number': 'Use different number',
        'All Complaints': 'All Complaints',
        'Latest': 'Latest',
        'By Priority': 'By Priority',
        'By Status': 'By Status',
        'Title': 'Title',
        'Category': 'Category',
        'Priority': 'Priority',
        'Status': 'Status',
        'Action': 'Action',
        'Details': 'Details',
        'No complaints available.': 'No complaints available.',
        'Complaint Title': 'Complaint Title',
        'Brief title of your complaint': 'Brief title of your complaint',
        'Where did this issue occur?': 'Where did this issue occur?',
        'Describe the issue in detail...': 'Describe the issue in detail...',
        'Location': 'Location',
        'Get Current Location': 'Get Current Location',
        'AI Analysis': 'AI Analysis',
        'Category:': 'Category:',
        'Priority Level:': 'Priority Level:',
        'Confidence:': 'Confidence:',
        'Attach Image (optional)': 'Attach Image (optional)',
        'Language': 'Language',
        'English': 'English',
        'ಕನ್ನಡ': 'ಕನ್ನಡ',
        'Submit': 'Submit',
        'Cancel': 'Cancel',
        'Pending': 'Pending',
        'In Progress': 'In Progress',
        'Resolved': 'Resolved',
        'High Priority': 'High Priority',
        'Voice Report': 'Voice Report',
        'Use Voice': 'Use Voice',
        'AI civic platform': 'AI civic platform',
        'Public service overview and issue monitoring': 'Public service overview and issue monitoring',
        'Search issues': 'Search issues',
        'Notifications': 'Notifications',
        'Citizen': 'Citizen',
        'User': 'User',
        'Total Complaints': 'Total Complaints',
        'Pending': 'Pending',
        'In Progress': 'In Progress',
        'Resolved': 'Resolved',
        'Needs review': 'Needs review',
        'Assigned': 'Assigned',
        'Completed': 'Completed',
        'Urgent': 'Urgent',
        'Live feed': 'Live feed',
        'Analytics Overview': 'Analytics Overview',
        'Clear Filters': 'Clear Filters',
        'All': 'All',
        'Voice': 'Voice',
        'Recent Grievances': 'Recent Grievances',
        'View all': 'View all',
        'Infrastructure': 'Infrastructure',
        'Water & Sanitation': 'Water & Sanitation',
        'Electricity': 'Electricity',
        'Public Health': 'Public Health',
        'Noise Pollution': 'Noise Pollution',
        'Air Quality': 'Air Quality',
        'Public Safety': 'Public Safety',
        'Traffic': 'Traffic',
        'Cleanliness': 'Cleanliness',
        'Let AI auto-detect': 'Let AI auto-detect',
        'Select category': 'Select category',
        '📍 Get Current Location': '📍 Get Current Location',
        '📝 Submit a Complaint': '📝 Submit a Complaint',
        '🎤 Use Voice': '🎤 Use Voice',
        '🎤 Voice Report': '🎤 Voice Report',
        '✍️ Text Report': '✍️ Text Report',
        'Start Recording': 'Start Recording',
        'Stop Recording': 'Stop Recording',
        'Submit Voice Complaint': 'Submit Voice Complaint',
        'Submit Text Complaint': 'Submit Text Complaint',
        'Reset Filters': 'Reset Filters',
        'No complaints submitted yet.': 'No complaints submitted yet.',
        'Report one now!': 'Report one now!',
        'Complaints by Category': 'Complaints by Category',
        'Complaints by Status': 'Complaints by Status',
        'Complaints Over Time': 'Complaints Over Time',
        'Complaints by Priority': 'Complaints by Priority',
        'Please enter your phone number': 'Please enter your phone number',
        'Please enter OTP': 'Please enter OTP',
        'Invalid email or password': 'Invalid email or password',
        'Email and password required': 'Email and password required',
        'All required fields must be filled': 'All required fields must be filled',
        'Email already exists': 'Email already exists',
        'Location and description are required': 'Location and description are required',
        'Admin Access': 'Admin Access',
        'Restricted to authorized administrators': 'Restricted to authorized administrators',
        'Login as Admin': 'Login as Admin',
        'This is a restricted area. Only authorized administrators can access this portal.': 'This is a restricted area. Only authorized administrators can access this portal.',
        'Back to Home': 'Back to Home',
        'Enter your mobile number to receive an OTP': 'Enter your mobile number to receive an OTP',
        'Include country code (e.g., +91 for India)': 'Include country code (e.g., +91 for India)',
        'Use different number': 'Use different number',
        'Complaint Details': 'Complaint Details',
        'Voice Based': 'Voice Based',
        'Text Based': 'Text Based',
        'Uploaded Image': 'Uploaded Image',
        'AI Classification & Analysis': 'AI Classification & Analysis',
        'Category': 'Category',
        'Priority Score': 'Priority Score',
        'Type': 'Type',
        'Location:': 'Location:',
        'Date': 'Date',
        'Submitted by': 'Submitted by',
        'Complaint ID': 'Complaint ID',
        'High': 'High',
        'Medium': 'Medium',
        'Low': 'Low',
        'Description': 'Description',
        'Status:': 'Status:',
        'Language:': 'Language:',
        'English':'English',
        'Kannada':'Kannada',
        'Brief title of your complaint': 'Brief title of your complaint',
        'Describe the issue in detail...': 'Describe the issue in detail...',
        'Attach Image (optional)': 'Attach Image (optional)',
        '📌 Location Details:': '📌 Location Details:',
        '🎙️ Voice-Based Complaint': '🎙️ Voice-Based Complaint',
        'Voice-Based Complaint': 'Voice-Based Complaint',
        'Step 1: Record Your Complaint': 'Step 1: Record Your Complaint',
        'Step 2: Review Transcription': 'Step 2: Review Transcription',
        'Step 3: Location': 'Step 3: Location',
        'Recording: ': 'Recording: ',
        '🎙️ Start Recording': '🎙️ Start Recording',
        '⏹️ Stop Recording': '⏹️ Stop Recording',
        'Edit or confirm the transcribed text...': 'Edit or confirm the transcribed text...',
        'Or enter location manually': 'Or enter location manually',
        'Category (Optional)': 'Category (Optional)',
        'Select category': 'Select category',
        '🤖 AI Classification:': '🤖 AI Classification:',
        'Transcription:': 'Transcription:',
        '🤖 AI Analysis:': '🤖 AI Analysis:',
        'Submit Voice Complaint': 'Submit Voice Complaint',
        'Submit Text Complaint': 'Submit Text Complaint',
        'Error accessing microphone: ': 'Error accessing microphone: ',
        'Transcription failed: ': 'Transcription failed: ',
        'Error transcribing audio: ': 'Error transcribing audio: ',
        'Please record your voice complaint or enter the transcribed text before submitting.': 'Please record your voice complaint or enter the transcribed text before submitting.',
        'Please add a location before submitting the complaint.': 'Please add a location before submitting the complaint.',
        'Submission failed: ': 'Submission failed: ',
        'Error submitting voice complaint: ': 'Error submitting voice complaint: ',
        'Detailed description of your complaint': 'Detailed description of your complaint',
        'Geolocation is not supported by this browser': 'Geolocation is not supported by this browser',
        'Error getting location: ': 'Error getting location: ',
        'Untitled Complaint': 'Untitled Complaint',
        'Citizen': 'Citizen',
        'Enter a valid name': 'Enter a valid name',
        'Choose file': 'Choose file',
        'No file chosen': 'No file chosen',
        'Browse files': 'Browse files',
        'File upload': 'File upload',
        'Image uploaded successfully': 'Image uploaded successfully',
        'Please select an image': 'Please select an image',
        'Image size exceeds limit': 'Image size exceeds limit',
        'Enter your password': 'Enter your password',
        'Enter your full name': 'Enter your full name'
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
        'File Complaint': 'ದೂರು ಸಲ್ಲಿಸಿ',
        'View Dashboard': 'ಡ್ಯಾಶ್‌ಬೋರ್ಡ್ ವೀಕ್ಷಿಸಿ',
        'Raise issues. Track progress. Build better communities.': 'ಸಮಸ್ಯೆಗಳನ್ನು ಹೇರಿಸಿ. ಪ್ರಗತಿ ಗಮನಿಸಿ. ಉತ್ತಮ ಸಮುದಾಯಗಳನ್ನು ನಿರ್ಮಿಸಿ.',
        'GrievanceConnect helps citizens report civic problems, monitor their status, and ensure faster responses from local authorities.': 'ಗ್ರಿವಾನ್ಸ್‌ಕನೆಕ್ಟ್ ನಾಗರಿಕರಿಗೆ ಜನಪ್ರಿಯ ಸಮಸ್ಯೆಗಳನ್ನು ವರದಿ ಮಾಡುವುದು, ಅವುಗಳ ಸ್ಥಿತಿಯನ್ನು ಗಮನಿಸುವುದು ಮತ್ತು ಸ್ಥಳೀಯ ಅಧಿಕಾರಗಳಿಂದ ವೇಗವಾಗಿ ಪ್ರತಿಕ್ರಿಯೆ ಪಡೆಯಲು ಸಹಾಯ ಮಾಡುತ್ತದೆ.',
        'Fast Reporting': 'ತ್ವರಿತ ವರದಿ',
        'Submit complaints in a few steps with complete details and location.': 'ಸಮಸ್ತ ವಿವರಗಳು ಮತ್ತು ಸ್ಥಳದ ಸಹಿತ ಸ್ವಲ್ಪ ಹಂತಗಳಲ್ಲಿ ದೂರು ಸಲ್ಲಿಸಿ.',
        'Live Tracking': 'ಲೈವ್ ಟ್ರ್ಯಾಕಿಂಗ್',
        'Monitor assigned work, issue steps, and progress updates in real time.': 'ನಿಯೋಜಿತ ಕೆಲಸ, ಸಮಸ್ಯೆ ಕ್ರಮಗಳು ಮತ್ತು ಪ್ರಗತಿ ಅಪ್‌ಡೇಟ್ಸ್‌ಗಳನ್ನು ನೇರವಾಗಿ ಗಮನಿಸಿ.',
        'Admin Oversight': 'ಆಡ್ಮಿನ್ ಮೇಲ್ವಿಚಾರಣೆ',
        'Authorities can review, resolve, and prioritize complaints efficiently.': 'ಅಧಿಕಾರಿಗಳು ದೂರುಗಳನ್ನು ಪರಿಣಾಮಕಾರಿಯಾಗಿ ಪರಿಶೀಲಿಸಿ, ತೀರ್ಮಾನಿಸಿ ಮತ್ತು ಆದ್ಯತೆ ನೀಡಬಹುದು.',
        'Create Account': 'ಖಾತೆ ರಚಿಸಿ',
        'Email': 'ಇಮೇಲ್',
        'Password': 'ಪಾಸ್ವರ್ಡ್',
        'Phone Number': 'ಫೋನ್ ಸಂಖ್ಯೆ',
        'Full Name': 'ಪೂರ್ಣ ಹೆಸರು',
        'Enter your full name': 'ನಿಮ್ಮ ಪೂರ್ಣ ಹೆಸರನ್ನು ನಮೂದಿಸಿ',
        'Enter your email': 'ನಿಮ್ಮ ಇಮೇಲ್ ನಮೂದಿಸಿ',
        'Enter your phone number': 'ನಿಮ್ಮ ಫೋನ್ ಸಂಖ್ಯೆ ನಮೂದಿಸಿ',
        'Create a password': 'ಪಾಸ್ವರ್ಡ್ ರಚಿಸಿ',
        'Citizen Login': 'ನಾಗರಿಕ ಲಾಗಿನ್',
        'Admin Login': 'ಆಡ್ಮಿನ್ ಲಾಗಿನ್',
        'Send OTP': 'OTP ಕಳುಹಿಸಿ',
        'Verify OTP': 'OTP ಪರಿಶೀಲಿಸಿ',
        'Enter the 6-digit OTP sent to your phone': 'ನಿಮ್ಮ ಫೋನ್‌ಗೆ ಕಳುಹಿಸಿದ 6-ಅಂಕಿಯ OTP ಅನ್ನು ನಮೂದಿಸಿ',
        'OTP Code': 'OTP ಕೋಡ್',
        'Resend OTP': 'OTP ಮರುಕಳುಹಿಸಿ',
        'Use different number': 'ಬೇರೆ ಸಂಖ್ಯೆ ಬಳಸಿ',
        'All Complaints': 'ಎಲ್ಲಾ ದೂರುಗಳು',
        'Latest': 'ಪೂರ್ವಕಾಲೀನ',
        'By Priority': 'ಆದ್ಯತೆಯ ಮೂಲಕ',
        'By Status': 'ಸ್ಥಿತಿಯ ಮೂಲಕ',
        'Title': 'ಶೀರ್ಷಿಕೆ',
        'Category': 'ವರ್ಗ',
        'Priority': 'ಆದ್ಯತೆ',
        'Status': 'ಸ್ಥಿತಿ',
        'Action': 'ಕ್ರಿಯೆ',
        'Details': 'ವಿವರಗಳು',
        'No complaints available.': 'ಯಾವುದೇ ದೂರುಗಳು ಲಭ್ಯವಿಲ್ಲ.',
        'Complaint Title': 'ದೂರು ಶೀರ್ಷಿಕೆ',
        'Brief title of your complaint': 'ನಿಮ್ಮ ದೂರುಗೆ ಸಂಕ್ಷಿಪ್ತ ಶೀರ್ಷಿಕೆ',
        'Where did this issue occur?': 'ಈ ಸಮಸ್ಯೆ ಎಲ್ಲಿ ಸಂಭವಿಸಿತು?',
        'Describe the issue in detail...': 'ಸಮಸ್ಯೆಯನ್ನು ವಿವರವಾಗಿ ವಿವರಿಸಿ...',
        'Location': 'ಸ್ಥಳ',
        'Get Current Location': 'ಪ್ರಸಕ್ತ ಸ್ಥಳ ಪಡೆಯಿರಿ',
        'AI Analysis': 'AI ವಿಶ್ಲೇಷಣೆ',
        'Category:': 'ವರ್ಗ:',
        'Priority Level:': 'ಆದ್ಯತೆ ಮಟ್ಟ:',
        'Confidence:': 'ಸುನಿಶ್ಚಿತತೆ:',
        'Attach Image (optional)': 'ಚಿತ್ರವನ್ನು ಸೇರಿಸಿ (ಐಚ್ಛಿಕ)',
        'Language': 'ಭಾಷೆ',
        'English': 'English',
        'ಕನ್ನಡ': 'ಕನ್ನಡ',
        'Submit': 'ಸಲ್ಲಿಸಿ',
        'Cancel': 'ರದ್ದುಮಾಡು',
        'Pending': 'ಬಾಕಿ',
        'In Progress': 'ಪ್ರಗತಿ ಹಾದಿಯಲ್ಲಿದೆ',
        'Resolved': 'ಪರಿಶೀಲನೆ ಮುಗಿದ',
        'High Priority': 'ಹೆಚ್ಚಿನ ಆದ್ಯತೆ',
        'Voice Report': 'ಧ್ವನಿ ವರದಿ',
        'Use Voice': 'ಧ್ವನಿಯನ್ನು ಬಳಸಿ',
        'AI civic platform': 'AI ನಾಗರಿಕ ಪ್ಲಾಟ್‌ಫಾರ್ಮ್',
        'Public service overview and issue monitoring': 'ಸಾರ್ವಜನಿಕ ಸೇವೆಗಳ ಅವಲೋಕನ ಮತ್ತು ಸಮಸ್ಯೆ ಮೇಲ್ವಿಚಾರಣೆ',
        'Search issues': 'ಸಮಸ್ಯೆ ಹುಡುಕಿ',
        'Notifications': 'ಅಧಿಸೂಚನೆಗಳು',
        'Citizen': 'ನಾಗರಿಕ',
        'User': 'ಬಳಕೆದಾರ',
        'Total Complaints': 'ಒಟ್ಟು ದೂರುಗಳು',
        'Needs review': 'ಪರಿಶೀಲನೆ ಬೇಕು',
        'Assigned': 'ನಿಯೋಜಿಸಲಾಗಿದೆ',
        'Completed': 'ಪೂರೈಸಲಾಗಿದೆ',
        'Urgent': 'ತುರ್ತು',
        'Live feed': 'ಲೈವ್ ಫೀಡ್',
        'Analytics Overview': 'ವಿಶ್ಲೇಷಣೆ ಅವಲೋಕನ',
        'Clear Filters': 'ಫಿಲ್ಟರ್‌ಗಳನ್ನು ತೆರವುಗೊಳಿಸಿ',
        'All': 'ಎಲ್ಲವೂ',
        'Voice': 'ಧ್ವನಿ',
        'Recent Grievances': 'ಇತ್ತಿಗೆ ಬರುವ ದೂರುಗಳು',
        'View all': 'ಎಲ್ಲವನ್ನೂ ವೀಕ್ಷಿಸಿ',
        'No complaints submitted yet.': 'ಇನ್ನೂ ಯಾವುದೇ ದೂರು ಸಲ್ಲಿಕೆ ಇಲ್ಲ.',
        'Report one now!': 'ಈಗ ಒಂದು ವರದಿ ಮಾಡಿ!',
        'Complaints by Category': 'ವರ್ಗದ ಮೂಲಕ ದೂರುಗಳು',
        'Complaints by Status': 'ಸ್ಥಿತಿಯ ಮೂಲಕ ದೂರುಗಳು',
        'Complaints Over Time': 'ಸಮಯದೊಂದಿಗೆ ದೂರುಗಳು',
        'Complaints by Priority': 'ಆದ್ಯತೆಯ ಮೂಲಕ ದೂರುಗಳು',
        'Infrastructure': 'ಸೌಲಭ್ಯ',
        'Water & Sanitation': 'ನೀರು ಮತ್ತು ಸ್ವಚ್ಛತೆ',
        'Electricity': 'ವಿದ್ಯುತ್',
        'Public Health': 'ಸಾರ್ವಜನಿಕ ಆರೋಗ್ಯ',
        'Noise Pollution': 'ಶಬ್ದ ಮಾಲಿನ್ಯ',
        'Air Quality': 'ಗಾಳಿಯ ಗುಣಮಟ್ಟ',
        'Public Safety': 'ಸಾರ್ವಜನಿಕ ಸುರಕ್ಷತೆ',
        'Traffic': 'ಟ್ರಾಫಿಕ್',
        'Cleanliness': 'ಸ್ವಚ್ಛತೆ',
        'Let AI auto-detect': 'AI ಸ್ವಯಂ-ಪತ್ತೆ ಮಾಡಿ',
        'Select category': 'ವರ್ಗವನ್ನು ಆಯ್ಕೆಮಾಡಿ',
        '📍 Get Current Location': '📍 ಪ್ರಸ್ತುತ ಸ್ಥಳ ಪಡೆಯಿರಿ',
        '📝 Submit a Complaint': '📝 ದೂರು ಸಲ್ಲಿಸಿ',
        '🎤 Use Voice': '🎤 ಧ್ವನಿ ಬಳಸಿ',
        '🎤 Voice Report': '🎤 ಧ್ವನಿ ವರದಿ',
        '✍️ Text Report': '✍️ ಪಠ್ಯ ವರದಿ',
        'Start Recording': 'ರೆಕಾರ್ಡಿಂಗ್ ಪ್ರಾರಂಭಿಸಿ',
        'Stop Recording': 'ರೆಕಾರ್ಡಿಂಗ್ ನಿಲ್ಲಿಸಿ',
        'Submit Voice Complaint': 'ಧ್ವನಿ ದೂರು ಸಲ್ಲಿಸಿ',
        'Submit Text Complaint': 'ಪಠ್ಯ ದೂರು ಸಲ್ಲಿಸಿ',
        'Reset Filters': 'ಫಿಲ್ಟರ್‌ಗಳನ್ನು ಮರುಹೊಂದಿಸಿ',
        'Please enter your phone number': 'ದಯವಿಟ್ಟು ಫೋನ್ ಸಂಖ್ಯೆಯನ್ನು ನಮೂದಿಸಿ',
        'Please enter OTP': 'ದಯವಿಟ್ಟು OTP ನಮೂದಿಸಿ',
        'Invalid email or password': 'ಅಮಾನ್ಯ ಇಮೇಲ್ ಅಥವಾ ಪಾಸ್ವರ್ಡ್',
        'Email and password required': 'ಇಮೇಲ್ ಮತ್ತು ಪಾಸ್ವರ್ಡ್ ಅಗತ್ಯ',
        'All required fields must be filled': 'ಎಲ್ಲ ಅಗತ್ಯ ಕ್ಷೇತ್ರಗಳನ್ನು ಭರ್ತಿ ಮಾಡಬೇಕು',
        'Email already exists': 'ಇಮೇಲ್ ಈಗಾಗಲೇ ಅಸ್ತಿತ್ವದಲ್ಲಿದೆ',
        'Location and description are required': 'ಸ್ಥಳ ಮತ್ತು ವಿವರಣೆ ಅಗತ್ಯ',
        'Admin Access': 'ಆಡ್ಮಿನ್ ಪ್ರವೇಶ',
        'Restricted to authorized administrators': 'ಅಧಿಕೃತ ಆಡ್ಮಿನ್‌ಗಳಿಗೆ ಮಾತ್ರ ಮಿತಿಯಿದೆ',
        'Login as Admin': 'ಆಡ್ಮಿನ್ ಆಗಿ ಲಾಗಿನ್',
        'This is a restricted area. Only authorized administrators can access this portal.': 'ಇದು ನಿರ್ಬಂಧಿತ ವಲಯವಾಗಿದೆ. ಅಧಿಕೃತ ಆಡ್ಮಿನ್‌ಗಳು ಮಾತ್ರ ಈ ಪೋರ್ಟಲ್ ಪ್ರವೇಶಿಸಬಹುದು.',
        'Back to Home': 'ಮುಖಪುಟಕ್ಕೆ ಹಿಂದಿರುಗಿ',
        'Enter your mobile number to receive an OTP': 'OTP ಪಡೆಯಲು ನಿಮ್ಮ ಮೊಬೈಲ್ ಸಂಖ್ಯೆಯನ್ನು ನೀಡಿ',
        'Include country code (e.g., +91 for India)': 'ದೆಸೆಯಲ್ಲಿ ದೇಶ ಕೋಡ್ ಸೇರಿಸಿ (ಉದಾಹರಣೆ: +91)',
        'Complaint Details': 'ದೂರು ವಿವರಗಳು',
        'Voice Based': 'ಧ್ವನಿ ಆಧಾರಿತ',
        'Text Based': 'ಟೆಕ್ಸ್ಟ್ ಆಧಾರಿತ',
        'Uploaded Image': 'ಅಪ್ಲೋಡ್ ಮಾಡಿದ ಚಿತ್ರ',
        'AI Classification & Analysis': 'AI ವರ್ಗೀಕರಣ ಮತ್ತು ವಿಶ್ಲೇಷಣೆ',
        'Priority Score': 'ಆದ್ಯತೆ ಅಂಕ',
        'Type': 'ಪ್ರಕಾರ',
        'Location:': 'ಸ್ಥಳ:',
        'Date': 'ದಿನಾಂಕ',
        'Submitted by': 'ಸಲ್ಲಿಸಿದವರು',
        'Complaint ID': 'ದೂರು ಐಡಿ',
        'High': 'ಹೆಚ್ಚಿನ',
        'Medium': 'ಮಧ್ಯಮ',
        'Low': 'ಕಡಿಮೆ',
        'Description': 'ವಿವರಣೆ',
        'Status:': 'ಸ್ಥಿತಿ:',
        'Language:': 'ಭಾಷೆ:',
        'Kannada': 'ಕನ್ನಡ',
        'Brief title of your complaint': 'ನಿಮ್ಮ ದೂರುಗೆ ಸಂಕ್ಷಿಪ್ತ ಶೀರ್ಷಿಕೆ',
        'Describe the issue in detail...': 'ಸಮಸ್ಯೆಯನ್ನು ವಿವರವಾಗಿ ವಿವರಿಸಿ...',
        'Attach Image (optional)': 'ಚಿತ್ರವನ್ನು ಸೇರಿಸಿ (ಐಚ್ಛಿಕ)',
        '📌 Location Details:': '📌 ಸ್ಥಳ ವಿವರಗಳು:',
        '🎙️ Voice-Based Complaint': '🎙️ ಧ್ವನಿ-ಆಧಾರಿತ ದೂರು',
        'Voice-Based Complaint': 'ಧ್ವನಿ-ಆಧಾರಿತ ದೂರು',
        'Step 1: Record Your Complaint': 'ಹಂತ 1: ನಿಮ್ಮ ದೂರು ರೆಕಾರ್ಡ್ ಮಾಡಿ',
        'Step 2: Review Transcription': 'ಹಂತ 2: ಟ್ರಾನ್ಸ್ಕ್ರಿಪ್ಶನ್ ಪರಿಶೀಲಿಸಿ',
        'Step 3: Location': 'ಹಂತ 3: ಸ್ಥಳ',
        'Recording: ': 'ರೆಕಾರ್ಡಿಂಗ್: ',
        '🎙️ Start Recording': '🎙️ ರೆಕಾರ್ಡಿಂಗ್ ಪ್ರಾರಂಭಿಸಿ',
        '⏹️ Stop Recording': '⏹️ ರೆಕಾರ್ಡಿಂಗ್ ನಿಲ್ಲಿಸಿ',
        'Edit or confirm the transcribed text...': 'ಟ್ರಾನ್ಸ್ಕ್ರೈಬ್ ಮಾಡಿದ ಪಠ್ಯವನ್ನು ತಿದ್ದಿ ಅಥವಾ ದೃಢೀಕರಿಸಿ...',
        'Or enter location manually': 'ಅಥವಾ ಸ್ಥಳವನ್ನು ಹೆಚ್ಚಿಕೆಯಾಗಿ ನಮೂದಿಸಿ',
        'Category (Optional)': 'ವರ್ಗ (ಐಚ್ಛಿಕ)',
        'Select category': 'ವರ್ಗವನ್ನು ಆಯ್ಕೆ ಮಾಡಿ',
        '🤖 AI Classification:': '🤖 AI ವರ್ಗೀಕರಣ:',
        'Transcription:': 'ಟ್ರಾನ್ಸ್ಕ್ರಿಪ್ಶನ್:',
        '🤖 AI Analysis:': '🤖 AI ವಿಶ್ಲೇಷಣೆ:',
        'Error accessing microphone: ': 'ಮೈಕ್ರೋಫೋನ್ ಪ್ರವೇಶದಲ್ಲಿ ದೋಷ: ',
        'Transcription failed: ': 'ಟ್ರಾನ್ಸ್ಕ್ರಿಪ್ಶನ್ ವಿಫಲವಾಗಿದೆ: ',
        'Error transcribing audio: ': 'ಆಡಿಯೋ ಟ್ರಾನ್ಸ್ಕ್ರೈಬ್ ಮಾಡುವಲ್ಲಿ ದೋಷ: ',
        'Please record your voice complaint or enter the transcribed text before submitting.': 'ಸಲ್ಲಿಸುವ ಮೊದಲು ದಯವಿಟ್ಟು ನಿಮ್ಮ ಧ್ವನಿ ದೂರು ರೆಕಾರ್ಡ್ ಮಾಡಿ ಅಥವಾ ಟ್ರಾನ್ಸ್ಕ್ರೈಬ್ಡ ಪಠ್ಯವನ್ನು ನಮೂದಿಸಿ.',
        'Please add a location before submitting the complaint.': 'ದೂರು ಸಲ್ಲಿಸುವ ಮೊದಲು ದಯವಿಟ್ಟು ಸ್ಥಳವನ್ನು ಸೇರಿಸಿ.',
        'Submission failed: ': 'ಸಮರ್ಪಣೆ ವಿಫಲವಾಗಿದೆ: ',
        'Error submitting voice complaint: ': 'ಧ್ವನಿ ದೂರು ಸಲ್ಲಿಸುವಲ್ಲಿ ದೋಷ: ',
        'Detailed description of your complaint': 'ನಿಮ್ಮ ದೂರುಗೆ ವಿವರವಾದ ವರ್ಣನೆ',
        'Geolocation is not supported by this browser': 'ಈ ಬ್ರೌಜರ್ ಜಿಯೋಲೋಕೇಶನ್ ಅನ್ನು ಬೆಂಬಲಿಸುವುದಿಲ್ಲ',
        'Error getting location: ': 'ಸ್ಥಳ ಪಡೆಯುವಲ್ಲಿ ದೋಷ: ',
        'Untitled Complaint': 'ಶೀರ್ಷಿಕೆ ರಹಿತ ದೂರು',
        'Enter a valid name': 'ಮಾನ್ಯ ಹೆಸರನ್ನು ನಮೂದಿಸಿ',
        'Choose file': 'ಫೈಲ್ ಆರಿಸಿ',
        'No file chosen': 'ಯಾವ ಫೈಲ್ ಆಯ್ಕೆ ಮಾಡಿಲ್ಲ',
        'Browse files': 'ಫೈಲ್‌ಗಳನ್ನು ಏರಳಿಸಿ',
        'File upload': 'ಫೈಲ್ ಅಪ್ಲೋಡ್',
        'Image uploaded successfully': 'ಚಿತ್ರವನ್ನು ಯಶಸ್ವಿಯಾಗಿ ಅಪ್ಲೋಡ್ ಮಾಡಲಾಗಿದೆ',
        'Please select an image': 'ದಯವಿಟ್ಟು ಚಿತ್ರವನ್ನು ಆರಿಸಿ',
        'Image size exceeds limit': 'ಚಿತ್ರ ಗಾತ್ರವು ಮಿತಿ ಮೀರಿದೆ',
        'Enter your password': 'ನಿಮ್ಮ ಪಾಸ್ವರ್ಡ್ ನಮೂದಿಸಿ',
        'Enter your full name': 'ನಿಮ್ಮ ಪೂರ್ಣ ಹೆಸರನ್ನು ನಮೂದಿಸಿ'
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

function ensureOriginalText(value) {
    if (!value) return value;
    return value.replace(/\s+/g, ' ').trim();
}

function getNodeOriginalText(node) {
    if (!node || !node.nodeValue) return '';
    const raw = ensureOriginalText(node.nodeValue);
    if (!raw) return '';
    if (!node.__grievanceOriginalText) {
        node.__grievanceOriginalText = raw;
    }
    return node.__grievanceOriginalText;
}

function getElementOriginalText(el) {
    if (!el) return '';
    const raw = ensureOriginalText(el.textContent || '');
    if (!raw) return '';
    if (!el.__grievanceOriginalText) {
        el.__grievanceOriginalText = raw;
    }
    return el.__grievanceOriginalText;
}

function getPlaceholderOriginalText(el) {
    if (!el) return '';
    const raw = ensureOriginalText(el.getAttribute('placeholder') || '');
    if (!raw) return '';
    if (!el.__grievancePlaceholderOriginal) {
        el.__grievancePlaceholderOriginal = raw;
    }
    return el.__grievancePlaceholderOriginal;
}

function createLanguageToggle() {
    // If navigation bar already has the civic topbar language switcher, do not create floating button
    if (document.querySelector('.lang-switcher-nav')) {
        return;
    }

    if (document.getElementById('global-language-toggle')) {
        return;
    }

    const toggle = document.createElement('button');
    toggle.id = 'global-language-toggle';
    toggle.type = 'button';
    toggle.setAttribute('aria-label', 'Switch language');
    toggle.innerHTML = 'English / ಕನ್ನಡ';
    toggle.style.position = 'fixed';
    toggle.style.top = '18px';
    toggle.style.right = '18px';
    toggle.style.zIndex = '9999';
    toggle.style.border = '1px solid rgba(102,126,234,0.35)';
    toggle.style.background = '#fff';
    toggle.style.color = '#234';
    toggle.style.padding = '8px 14px';
    toggle.style.borderRadius = '999px';
    toggle.style.fontSize = '12px';
    toggle.style.fontWeight = '700';
    toggle.style.boxShadow = '0 8px 20px rgba(0,0,0,0.12)';
    toggle.style.cursor = 'pointer';
    toggle.addEventListener('click', () => {
        const current = getStoredLanguage();
        const newLang = current === 'en' ? 'kn' : 'en';
        applyLanguage(newLang);
    });
    document.body.appendChild(toggle);
}

function normalizeTranslationKey(value = '') {
    return value
        .replace(/[\u2600-\u27BF]/g, '')
        .replace(/[\u2000-\u206F]/g, '')
        .replace(/\s+/g, ' ')
        .trim();
}

function translateValue(map, rawValue) {
    if (!rawValue) return rawValue;
    const trimmed = ensureOriginalText(rawValue);
    if (!trimmed) return rawValue;

    if (map[trimmed]) return map[trimmed];

    const normalized = normalizeTranslationKey(trimmed);
    if (map[normalized]) return map[normalized];

    return trimmed;
}

function setLanguage(lang) {
    applyLanguage(lang);
}
window.setLanguage = setLanguage;

function applyLanguage(lang) {
    const dict = translations[lang];
    if (!dict) return;

    // 1. Walk only leaf text nodes to avoid destroying child DOM trees/inputs/buttons
    try {
        const walker = document.createTreeWalker(
            document.body,
            NodeFilter.SHOW_TEXT,
            {
                acceptNode: function(node) {
                    const parent = node.parentElement;
                    if (!parent) return NodeFilter.FILTER_REJECT;
                    const tag = parent.tagName.toLowerCase();
                    if (['script', 'style', 'code', 'pre', 'textarea', 'svg'].includes(tag)) {
                        return NodeFilter.FILTER_REJECT;
                    }
                    if (node.nodeValue && node.nodeValue.trim().length > 0) {
                        return NodeFilter.FILTER_ACCEPT;
                    }
                    return NodeFilter.FILTER_SKIP;
                }
            },
            false
        );

        let textNode;
        while ((textNode = walker.nextNode())) {
            const originalText = getNodeOriginalText(textNode);
            if (originalText && dict[originalText]) {
                textNode.nodeValue = dict[originalText];
            }
        }
    } catch (e) {
        console.warn('Text node translation error:', e);
    }

    // 2. Safely translate input placeholders
    document.querySelectorAll('input[placeholder], textarea[placeholder]').forEach(el => {
        const placeholderText = getPlaceholderOriginalText(el);
        if (placeholderText && dict[placeholderText]) {
            el.setAttribute('placeholder', dict[placeholderText]);
        }
    });

    // 3. Translate select options without breaking select value
    document.querySelectorAll('select option').forEach(opt => {
        const orig = getElementOriginalText(opt);
        if (orig && dict[orig]) {
            opt.textContent = dict[orig];
        }
    });

    // 4. Update topbar language switcher pills
    document.querySelectorAll('.lang-pill').forEach(pill => {
        const onclickAttr = pill.getAttribute('onclick') || '';
        if (onclickAttr.includes(`'${lang}'`) || onclickAttr.includes(`"${lang}"`)) {
            pill.classList.add('active');
        } else {
            pill.classList.remove('active');
        }
    });

    // 5. Update floating toggle button if visible
    const toggleBtn = document.getElementById('global-language-toggle');
    if (toggleBtn) {
        toggleBtn.innerText = lang === 'en' ? 'ಕನ್ನಡ' : 'English';
    }

    // Persist choice
    setStoredLanguage(lang);
}

function initLanguageToggle() {
    createLanguageToggle();
    const stored = getStoredLanguage();
    if (stored && stored !== 'en') {
        applyLanguage(stored);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach((button) => {
        button.addEventListener('mouseenter', () => {
            button.style.opacity = '0.92';
        });

        button.addEventListener('mouseleave', () => {
            button.style.opacity = '1';
        });
    });

    initLanguageToggle();
});
