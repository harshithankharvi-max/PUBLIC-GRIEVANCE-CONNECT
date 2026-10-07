"""
AI-based Complaint Classification and Prioritization Module
Classifies complaints into 8 specific civic categories and maps to 3 Authority Departments:
ELECTRICITY, PWD, and WATER.
Also evaluates explainable priority (HIGH, MEDIUM, LOW) and validates civic grievance scope.
"""

import json
import re
import os

# The 8 Supported Rural Civic Categories
CATEGORIES_8 = [
    'Electricity / Power Supply',
    'Streetlight',
    'Road Damage',
    'Drainage / Public Infrastructure',
    'Water Supply',
    'Water Leakage / Pipeline',
    'Water Quality / Contamination',
    'Other PWD / Public Infrastructure'
]

# Mapping of the 8 Categories into the 3 Authority Departments
CATEGORY_DEPARTMENT_MAP = {
    'Electricity / Power Supply': 'ELECTRICITY',
    'Streetlight': 'ELECTRICITY',
    'Road Damage': 'PWD',
    'Drainage / Public Infrastructure': 'PWD',
    'Other PWD / Public Infrastructure': 'PWD',
    'Water Supply': 'WATER',
    'Water Leakage / Pipeline': 'WATER',
    'Water Quality / Contamination': 'WATER',
}

# The 3 Supported Authority Departments
DEPARTMENTS = ['ELECTRICITY', 'PWD', 'WATER']

REJECTION_MESSAGE = (
    "Sorry, this grievance is outside the supported civic categories of this portal. "
    "Please contact the appropriate emergency or concerned authority for assistance."
)


class ComplaintClassifier:
    """AI classifier for automatic complaint categorization and prioritization"""

    # Rich keyword vocabulary for the 8 supported categories in English & Kannada transliterations
    CATEGORY_KEYWORDS = {
        'Streetlight': [
            'streetlight', 'street light', 'streetlights', 'street lamp', 'pole light',
            'bulb', 'tube light', 'dark street', 'night light', 'light pole', 'lamp post',
            'ಬೀದಿ ದೀಪ', 'ದೀಪ', 'ಕಂಬದ ದೀಪ'
        ],
        'Electricity / Power Supply': [
            'electricity', 'power', 'power supply', 'power cut', 'blackout', 'outage',
            'current', 'voltage', 'transformer', 'electric pole', 'live wire', 'wire',
            'hanging wire', 'spark', 'electric shock', 'meter', 'load shedding', 'feeder',
            'substation', 'phase', 'no electricity', 'no power', 'ವಿದ್ಯುತ್', 'ಕರೆಂಟ್', 'ಟ್ರಾನ್ಸ್‌ಫಾರ್ಮರ್'
        ],
        'Road Damage': [
            'road', 'pothole', 'potholes', 'cracked road', 'mud road', 'road damaged',
            'damaged road', 'tar road', 'asphalt', 'pavement', 'gravel', 'bumpy road',
            'broken road', 'highway', 'street repair', 'road repair', 'gutter in road',
            'ರಸ್ತೆ', 'ಗುಂಡಿ', 'ಡಾಂಬರು'
        ],
        'Drainage / Public Infrastructure': [
            'drain', 'drainage', 'gutter', 'sewage', 'culvert', 'manhole', 'overflowing drain',
            'blocked drain', 'clogged drain', 'stormwater', 'canal', 'waste water', 'sewer',
            'ditch', 'open drain', 'choked drain', 'stagnant water', 'ಚರಂಡಿ', 'ಒಳಚರಂಡಿ'
        ],
        'Water Supply': [
            'water supply', 'drinking water', 'tap water', 'no water', 'water shortage',
            'dry tap', 'borewell', 'water tank', 'tanker', 'hand pump', 'well', 'water problem',
            'water timing', 'water pressure', 'supply water', 'water not coming',
            'ಕುಡಿಯುವ ನೀರು', 'ನೀರು ಸರಬರಾಜು', 'ಬೋರ್‌ವೆಲ್', 'ನಲ್ಲಿ ನೀರು'
        ],
        'Water Leakage / Pipeline': [
            'pipe', 'pipeline', 'leak', 'leakage', 'burst pipe', 'water pipe', 'broken pipe',
            'leaking pipe', 'valve', 'main line', 'water leaking', 'pipe damage', 'pipe burst',
            'wasting water', 'water gushing', 'ಪೈಪ್ ಲೈನ್', 'ಸೋರಿಕೆ', 'ಪೈಪು'
        ],
        'Water Quality / Contamination': [
            'water quality', 'contaminated water', 'contamination', 'dirty water', 'muddy water',
            'bad smell water', 'smelly water', 'yellow water', 'brown water', 'worms in water',
            'impure water', 'water sickness', 'water pollution', 'polluted water', 'chlorine',
            'unfit to drink', 'ಕಲುಷಿತ ನೀರು', 'ಕೆಟ್ಟ ನೀರು', 'ವಾಸನೆ ನೀರು'
        ],
        'Other PWD / Public Infrastructure': [
            'bridge', 'footpath', 'sidewalk', 'culvert', 'public building', 'community hall',
            'bus stop', 'bus shelter', 'public toilet', 'retaining wall', 'compound wall',
            'government building', 'panchayat building', 'public park', 'boundary wall',
            'ಸೇತುವೆ', 'ಫುಟ್‌ಪಾತ್', 'ಸಾರ್ವಜನಿಕ ಕಟ್ಟಡ'
        ]
    }

    # Off-topic / Non-Civic patterns that must be rejected
    UNSUPPORTED_PATTERNS = [
        r'\bchild is missing\b', r'\bmissing child\b', r'\bmissing person\b', r'\bkidnap\b',
        r'\bkidnapping\b', r'\btheft\b', r'\bstolen\b', r'\brobbery\b', r'\bmurder\b',
        r'\bassault\b', r'\bpolice\b', r'\bcrime\b', r'\bcheat\b', r'\bfraud\b',
        r'\bdivorce\b', r'\bdomestic\b', r'\bhusband\b', r'\bwife\b', r'\bloan\b',
        r'\bsalary\b', r'\bbank account\b', r'\bexam\b', r'\bcollege admission\b',
        r'\bjob application\b', r'\blost phone\b', r'\blost wallet\b'
    ]

    # Explicit HIGH priority hazard indicators
    HIGH_HAZARD_KEYWORDS = [
        'fallen pole', 'fallen electric pole', 'live wire', 'exposed wire', 'hanging wire',
        'electric shock', 'sparking', 'spark', 'transformer blast', 'transformer burst',
        'fire', 'smoke from wire', 'dangerous', 'danger', 'hazard', 'emergency', 'urgent',
        'critical', 'fatal', 'accident', 'life threatening', 'collapsed', 'collapse',
        'cave in', 'sinkhole', 'bridge collapse', 'landslide', 'poisonous', 'contaminated',
        'epidemic', 'disease', 'serious water contamination', 'no drinking water affecting',
        'entire village without water', 'since yesterday', 'no electricity since yesterday',
        'major electricity failure', 'immediate', 'asap'
    ]

    # MEDIUM priority indicators
    MEDIUM_KEYWORDS = [
        'broken', 'damaged', 'leak', 'leaking', 'pothole', 'potholes', 'not working',
        'dark street', 'overflowing', 'clogged', 'muddy', 'bad smell', 'low voltage',
        'irregular', 'continuing', 'needs repair', 'needs attention', 'problem', 'issue'
    ]

    def __init__(self):
        """Initialize the classifier"""
        self.is_trained = True

    def classify_complaint(self, title, description='', location=''):
        """
        Classify a complaint into one of 8 categories and 3 authority departments.
        Also evaluates explainable priority and checks if it's a valid civic complaint.
        """
        full_text = f"{title} {description} {location}".strip()
        text_lower = full_text.lower()

        # 1. Check for explicit unsupported/off-topic patterns
        for pattern in self.UNSUPPORTED_PATTERNS:
            if re.search(pattern, text_lower):
                return {
                    'is_supported': False,
                    'category': 'Unsupported',
                    'department': None,
                    'priority_level': 'LOW',
                    'priority': 2,
                    'confidence': 0.0,
                    'message': REJECTION_MESSAGE
                }

        # 2. Match scores across the 8 categories
        category_scores = {}
        matched_keywords_per_cat = {}

        for cat, keywords in self.CATEGORY_KEYWORDS.items():
            matches = []
            for kw in keywords:
                if kw in text_lower:
                    matches.append(kw)
            category_scores[cat] = len(matches)
            matched_keywords_per_cat[cat] = matches

        # Also handle specific compound phrase priorities (e.g. street light vs power supply)
        if any(kw in text_lower for kw in ['streetlight', 'street light', 'streetlights', 'street lamp', 'pole light', 'ಬೀದಿ ದೀಪ']):
            category_scores['Streetlight'] += 5

        if any(kw in text_lower for kw in ['dirty water', 'contaminated', 'muddy water', 'smelly water', 'yellow water', 'worms']):
            category_scores['Water Quality / Contamination'] += 4

        if any(kw in text_lower for kw in ['pipe leak', 'pipeline leak', 'pipe burst', 'leaking pipe', 'water leaking']):
            category_scores['Water Leakage / Pipeline'] += 4

        best_category = max(category_scores, key=category_scores.get)
        max_score = category_scores[best_category]

        # 3. Check if any civic category matched
        if max_score == 0:
            # No civic grievance keywords matched
            return {
                'is_supported': False,
                'category': 'Unsupported',
                'department': None,
                'priority_level': 'LOW',
                'priority': 2,
                'confidence': 0.0,
                'message': REJECTION_MESSAGE
            }

        # 4. Map to one of the 3 Authority Departments
        department = CATEGORY_DEPARTMENT_MAP.get(best_category, 'PWD')

        # 5. Evaluate explainable priority (HIGH, MEDIUM, LOW)
        priority_level, priority_score = self._evaluate_priority(text_lower, best_category)

        # 6. Confidence calculation
        confidence = min(0.98, max(0.65, 0.5 + (max_score * 0.15)))

        return {
            'is_supported': True,
            'category': best_category,
            'department': department,
            'priority_level': priority_level,
            'priority': priority_score,
            'confidence': round(confidence, 3),
            'message': None
        }

    def _evaluate_priority(self, text_lower, category):
        """
        Explainable priority calculation:
        HIGH: danger, life safety, hazardous wires/poles, health emergency, water contamination, major village blackout
        MEDIUM: broken streetlight, potholes, pipeline leakage, drainage overflow, regular supply failure
        LOW: minor maintenance, aesthetic, low urgency
        """
        # Check high hazard keywords
        for hk in self.HIGH_HAZARD_KEYWORDS:
            if hk in text_lower:
                return 'HIGH', 8

        # Category specific critical defaults
        if category == 'Water Quality / Contamination':
            if any(w in text_lower for w in ['poison', 'sick', 'disease', 'toxic', 'hospital', 'fever', 'severe']):
                return 'HIGH', 9
            return 'HIGH', 7

        if category == 'Electricity / Power Supply':
            if any(w in text_lower for w in ['pole', 'wire', 'shock', 'spark', 'transformer', 'blast', 'yesterday', 'whole village']):
                return 'HIGH', 8
            return 'MEDIUM', 6

        # Check medium indicators
        for mk in self.MEDIUM_KEYWORDS:
            if mk in text_lower:
                return 'MEDIUM', 5

        if category in ['Streetlight', 'Road Damage', 'Water Leakage / Pipeline', 'Drainage / Public Infrastructure']:
            return 'MEDIUM', 5

        return 'LOW', 3

    classify = classify_complaint


def get_department_for_category(category):
    """Safely map any category string (including legacy ones) to one of the 3 Departments"""
    if not category:
        return 'PWD'
    if category in CATEGORY_DEPARTMENT_MAP:
        return CATEGORY_DEPARTMENT_MAP[category]

    cat_lower = str(category).lower()
    if any(k in cat_lower for k in ['electric', 'power', 'light', 'bulb']):
        return 'ELECTRICITY'
    if any(k in cat_lower for k in ['water', 'drain', 'pipe', 'leak', 'sanit']):
        return 'WATER'
    return 'PWD'


def classify_complaint(title, description, location=''):
    """Convenience helper to classify complaints"""
    classifier = ComplaintClassifier()
    return classifier.classify_complaint(title, description, location)

