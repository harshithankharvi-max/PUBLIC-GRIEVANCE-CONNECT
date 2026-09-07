"""
AI-based Complaint Classification and Prioritization Module
Classifies complaints into categories and assigns priority scores
"""

import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import pickle
import os

class ComplaintClassifier:
    """AI classifier for automatic complaint categorization and prioritization"""
    
    # Predefined complaint categories with keywords
    CATEGORIES = {
        'Infrastructure': ['road', 'pothole', 'bridge', 'construction', 'highway', 'pavement', 'drainage', 'footpath', 'sidewalk', 'culvert'],
        'Water & Sanitation': ['water', 'sewage', 'drain', 'tap', 'sanitation', 'pipeline', 'waste', 'drinking water', 'borewell', 'leakage', 'tank'],
        'Electricity': ['power', 'electricity', 'blackout', 'streetlight', 'street light', 'street lights', 'streetlights', 'bulb', 'outage', 'voltage', 'light', 'lights', 'pole', 'transformer', 'wire', 'wiring', 'current'],
        'Public Health': ['hospital', 'clinic', 'disease', 'health', 'medical', 'sanitation', 'hygiene', 'doctor', 'medicine', 'ambulance', 'fever', 'dengue'],
        'Noise Pollution': ['noise', 'loud', 'sound', 'disturbance', 'music', 'speaker', 'loudspeaker'],
        'Air Quality': ['pollution', 'air', 'smoke', 'dust', 'emissions', 'factory', 'smell', 'odor'],
        'Public Safety': ['crime', 'theft', 'assault', 'accident', 'safety', 'security', 'danger', 'police'],
        'Traffic': ['traffic', 'congestion', 'parking', 'vehicle', 'crossing', 'jam', 'signal', 'bus'],
        'Cleanliness': ['garbage', 'waste', 'dirty', 'litter', 'sweeping', 'cleaning', 'trash', 'dump', 'dustbin'],
        'Other': []
    }
    
    # Priority keywords (higher priority if found in complaint)
    HIGH_PRIORITY_KEYWORDS = [
        'urgent', 'emergency', 'critical', 'dangerous', 'hazard', 'risk', 'injury', 
        'death', 'fatal', 'serious', 'severe', 'immediate', 'asap'
    ]
    
    MEDIUM_PRIORITY_KEYWORDS = [
        'problem', 'issue', 'complaint', 'concern', 'matter', 'needs', 'requires',
        'should', 'must', 'needs attention', 'important'
    ]
    
    def __init__(self):
        """Initialize the classifier"""
        self.model = None
        self.vectorizer = None
        self.is_trained = False
        
    def classify_complaint(self, title, description, location=''):
        """
        Classify a complaint based on title, description, and location
        
        Args:
            title: Complaint title
            description: Detailed description
            location: Location string
            
        Returns:
            dict with keys: category, confidence, priority_score
        """
        text = f"{title} {description} {location}".lower()
        
        # Classify into category
        category = self._classify_category(text)
        confidence = self._calculate_confidence(text, category)
        
        # Calculate priority score (0-10)
        priority = self._calculate_priority(text, category)
        
        return {
            'category': category,
            'confidence': round(confidence, 3),
            'priority': priority
        }
    
    def _classify_category(self, text):
        """Classify complaint into one of the predefined categories"""
        text_lower = text.lower()
        category_scores = {}
        
        for category, keywords in self.CATEGORIES.items():
            if category == 'Other':
                continue
            score = sum(1 for keyword in keywords if keyword in text_lower)
            category_scores[category] = score
        
        # Return category with highest score, default to 'Other'
        best_category = max(category_scores, key=category_scores.get)
        return best_category if category_scores[best_category] > 0 else 'Other'
    
    def _calculate_confidence(self, text, category):
        """
        Calculate confidence score for the classification
        Based on keyword matching strength
        """
        text_lower = text.lower()
        keywords = self.CATEGORIES.get(category, [])
        
        if not keywords:
            return 0.5
        
        matched = sum(1 for keyword in keywords if keyword in text_lower)
        confidence = min(1.0, (matched / len(keywords)) + 0.3)
        
        return confidence
    
    def _calculate_priority(self, text, category):
        """
        Calculate priority score from 0-10 based on content analysis
        """
        text_lower = text.lower()
        priority_score = 0.0
        
        # Check for high priority keywords (base 6-10)
        high_priority_count = sum(1 for keyword in self.HIGH_PRIORITY_KEYWORDS 
                                 if keyword in text_lower)
        if high_priority_count > 0:
            priority_score = 7 + (high_priority_count * 0.5)
        
        # Check for medium priority keywords (base 4-6)
        elif any(keyword in text_lower for keyword in self.MEDIUM_PRIORITY_KEYWORDS):
            priority_score = 5
        
        # Category-based default priorities
        category_defaults = {
            'Public Safety': 8,
            'Public Health': 7,
            'Electricity': 6,
            'Water & Sanitation': 6,
            'Infrastructure': 5,
            'Traffic': 4,
            'Noise Pollution': 3,
            'Air Quality': 4,
            'Cleanliness': 3,
            'Other': 2
        }
        
        if priority_score == 0:
            priority_score = category_defaults.get(category, 2)
        
        # Cap at 10
        return min(10, priority_score)
    
    def save_model(self, path):
        """Save trained model to disk"""
        if self.model:
            with open(path, 'wb') as f:
                pickle.dump({'model': self.model, 'vectorizer': self.vectorizer}, f)
    
    def load_model(self, path):
        """Load trained model from disk"""
        if os.path.exists(path):
            with open(path, 'rb') as f:
                data = pickle.load(f)
                self.model = data['model']
                self.vectorizer = data['vectorizer']
                self.is_trained = True


def classify_complaint(title, description, location=''):
    """
    Convenience function to classify a complaint
    
    Args:
        title: Complaint title
        description: Complaint description
        location: Complaint location
        
    Returns:
        dict with classification results
    """
    classifier = ComplaintClassifier()
    return classifier.classify_complaint(title, description, location)
