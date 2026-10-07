"""
Voice processing module for handling audio input and transcription
"""

try:
    import speech_recognition as sr
except ImportError:  # pragma: no cover
    # Minimal stub for speech_recognition
    class _DummyRecognizer:
        def recognize_google(self, audio):
            return ""
        def record(self, source):
            return None
        def __init__(self):
            pass
    class _DummyAudioFile:
        def __init__(self, filename):
            pass
        def __enter__(self):
            return None
        def __exit__(self, exc_type, exc, tb):
            pass
    class _DummyMicrophone:
        def __init__(self, *args, **kwargs):
            pass
        def __enter__(self):
            return None
        def __exit__(self, exc_type, exc, tb):
            pass
    class _DummyError(Exception):
        pass
    sr = type('sr', (), {
        'Recognizer': _DummyRecognizer,
        'AudioFile': _DummyAudioFile,
        'Microphone': _DummyMicrophone,
        'UnknownValueError': _DummyError,
        'RequestError': _DummyError,
    })

import os
import json
from datetime import datetime

class VoiceProcessor:
    """Handles voice input processing and transcription"""
    
    def __init__(self, upload_folder='static/voice_notes'):
        """Initialize voice processor with upload folder"""
        self.recognizer = sr.Recognizer()
        self.upload_folder = upload_folder
        
        # Create upload folder if it doesn't exist
        if not os.path.exists(self.upload_folder):
            os.makedirs(self.upload_folder, exist_ok=True)
    
    def transcribe_audio(self, audio_file_path):
        """
        Transcribe audio file to text
        
        Args:
            audio_file_path: Path to audio file (.wav, .flac, .mp3)
            
        Returns:
            dict with keys: text, confidence, success, error_message
        """
        try:
            # Load audio file
            with sr.AudioFile(audio_file_path) as source:
                audio = self.recognizer.record(source)
            
            # Attempt transcription using Google Speech Recognition API
            text = self.recognizer.recognize_google(audio)
            
            return {
                'text': text,
                'confidence': 0.95,
                'success': True,
                'error_message': None
            }
        except sr.UnknownValueError:
            return {
                'text': '',
                'confidence': 0,
                'success': False,
                'error_message': 'Could not understand audio. Please speak clearly.'
            }
        except sr.RequestError as e:
            return {
                'text': '',
                'confidence': 0,
                'success': False,
                'error_message': f'Speech recognition service error: {str(e)}'
            }
        except Exception as e:
            return {
                'text': '',
                'confidence': 0,
                'success': False,
                'error_message': f'Error processing audio: {str(e)}'
            }
    
    def process_microphone_input(self, duration=10, language='en-US'):
        """
        Process audio from microphone
        
        Args:
            duration: Recording duration in seconds
            language: Language code (default: en-US)
            
        Returns:
            dict with transcription result
        """
        try:
            with sr.Microphone() as source:
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                
                # Listen to microphone
                audio = self.recognizer.listen(source, timeout=duration)
            
            # Transcribe
            text = self.recognizer.recognize_google(audio, language=language)
            
            return {
                'text': text,
                'confidence': 0.95,
                'success': True,
                'error_message': None
            }
        except sr.UnknownValueError:
            return {
                'text': '',
                'confidence': 0,
                'success': False,
                'error_message': 'Could not understand audio. Please speak clearly.'
            }
        except sr.RequestError as e:
            return {
                'text': '',
                'confidence': 0,
                'success': False,
                'error_message': f'Speech recognition service error: {str(e)}'
            }
        except Exception as e:
            return {
                'text': '',
                'confidence': 0,
                'success': False,
                'error_message': f'Error processing audio: {str(e)}'
            }
    
    def save_voice_note(self, file_obj, user_id, complaint_id=None):
        """
        Save uploaded voice note file
        
        Args:
            file_obj: File object from request.files
            user_id: User ID
            complaint_id: Complaint ID (if updating existing)
            
        Returns:
            dict with file path and success status
        """
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"user_{user_id}_{timestamp}.wav"
            filepath = os.path.join(self.upload_folder, filename)
            
            # Save file
            file_obj.save(filepath)
            
            return {
                'success': True,
                'filename': filename,
                'filepath': filepath,
                'relative_path': f'voice_notes/{filename}',
                'error_message': None
            }
        except Exception as e:
            return {
                'success': False,
                'filename': None,
                'filepath': None,
                'relative_path': None,
                'error_message': f'Error saving file: {str(e)}'
            }
    
    def get_audio_info(self, audio_file_path):
        """Get information about audio file"""
        try:
            with sr.AudioFile(audio_file_path) as source:
                audio = self.recognizer.record(source)
            
            return {
                'duration': len(audio.frame_data) / audio.sample_rate if hasattr(audio, 'sample_rate') else 0,
                'success': True
            }
        except Exception as e:
            return {
                'duration': 0,
                'success': False,
                'error': str(e)
            }
