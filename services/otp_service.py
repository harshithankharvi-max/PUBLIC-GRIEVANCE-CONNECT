"""
OTP Service for Phone-based Authentication
Handles OTP generation, sending via Twilio, and validation
"""

import os
import random
import sqlite3
from datetime import datetime, timedelta
from flask import g

class OTPService:
    """Manages OTP generation, storage, and validation"""
    
    def __init__(self):
        self.otp_length = 6
        self.expiry_minutes = int(os.getenv('OTP_EXPIRY_MINUTES', 10))
        self.max_attempts = int(os.getenv('OTP_MAX_ATTEMPTS', 3))
        self.resend_cooldown_seconds = int(os.getenv('OTP_RESEND_COOLDOWN_SECONDS', 60))
        
        # Check if Twilio is configured
        self.use_twilio = (
            os.getenv('TWILIO_ACCOUNT_SID') and 
            os.getenv('TWILIO_AUTH_TOKEN') and 
            os.getenv('TWILIO_VERIFY_SERVICE_SID')
        )
        
        if self.use_twilio:
            try:
                from twilio.rest import Client
                self.twilio_client = Client(
                    os.getenv('TWILIO_ACCOUNT_SID'),
                    os.getenv('TWILIO_AUTH_TOKEN')
                )
                self.verify_service_sid = os.getenv('TWILIO_VERIFY_SERVICE_SID')
            except ImportError:
                print("WARNING: Twilio not installed. Install with: pip install twilio")
                self.use_twilio = False
    
    def generate_otp(self, phone_number):
        """
        Generate and store OTP for a phone number
        
        Args:
            phone_number: Phone number (with country code, e.g., +919876543210)
            
        Returns:
            dict: {'success': bool, 'message': str, 'otp': str (for testing only)}
        """
        try:
            # Clean phone number
            phone = phone_number.strip().replace(' ', '')
            
            # Validate phone format (basic check)
            if not phone.startswith('+') or len(phone) < 10:
                return {'success': False, 'message': 'Invalid phone number format. Use +country code.'}
            
            db = g.get('db')
            if db is None:
                # If no g.db, we need to get it from app context
                from flask import current_app
                db = sqlite3.connect(current_app.config['DATABASE'])
                db.row_factory = sqlite3.Row
            
            # Check rate limiting: max 3 OTP requests per phone per hour
            hour_ago = datetime.now() - timedelta(hours=1)
            recent_requests = db.execute(
                '''
                SELECT COUNT(*) as count FROM otp_sessions 
                WHERE phone = ? AND created_at > ?
                ''',
                (phone, hour_ago.isoformat())
            ).fetchone()
            
            if recent_requests['count'] >= self.max_attempts:
                return {
                    'success': False, 
                    'message': f'Too many OTP requests. Try again in 1 hour.'
                }
            
            # Check resend cooldown: can't resend within 60 seconds
            recent = db.execute(
                '''
                SELECT created_at FROM otp_sessions 
                WHERE phone = ? 
                ORDER BY created_at DESC 
                LIMIT 1
                ''',
                (phone,)
            ).fetchone()
            
            if recent:
                created = datetime.fromisoformat(recent['created_at'])
                time_since = (datetime.now() - created).total_seconds()
                if time_since < self.resend_cooldown_seconds:
                    return {
                        'success': False,
                        'message': f'Please wait {self.resend_cooldown_seconds - int(time_since)} seconds before requesting another OTP.'
                    }
            
            # Generate 6-digit OTP
            otp_code = str(random.randint(100000, 999999))
            expiry_time = (datetime.now() + timedelta(minutes=self.expiry_minutes)).isoformat()
            
            # Store OTP in database
            db.execute(
                '''
                INSERT INTO otp_sessions (phone, otp_code, expires_at, attempts, verified, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                ''',
                (phone, otp_code, expiry_time, 0, 0, datetime.now().isoformat())
            )
            db.commit()
            
            # Send OTP via Twilio or return for testing
            if self.use_twilio:
                try:
                    verification = self.twilio_client.verify.v2.services(self.verify_service_sid).verifications.create(
                        to=phone,
                        channel='sms'
                    )
                    return {
                        'success': True,
                        'message': f'OTP sent to {phone}',
                        'verification_sid': verification.sid
                    }
                except Exception as e:
                    return {
                        'success': False,
                        'message': f'Failed to send OTP: {str(e)}'
                    }
            else:
                # Development mode: return OTP for testing
                print(f"[DEV MODE] OTP for {phone}: {otp_code}")
                return {
                    'success': True,
                    'message': f'OTP sent to {phone} (Dev Mode: {otp_code})',
                    'otp': otp_code  # Only in dev mode, never expose in production
                }
                
        except Exception as e:
            return {'success': False, 'message': f'Error generating OTP: {str(e)}'}
    
    def verify_otp(self, phone_number, otp_code):
        """
        Verify OTP for a phone number
        
        Args:
            phone_number: Phone number
            otp_code: OTP code entered by user
            
        Returns:
            dict: {'success': bool, 'message': str, 'user_id': int (if success)}
        """
        try:
            phone = phone_number.strip().replace(' ', '')
            
            db = g.get('db')
            if db is None:
                from flask import current_app
                db = sqlite3.connect(current_app.config['DATABASE'])
                db.row_factory = sqlite3.Row
            
            # Check OTP attempt limit
            otp_record = db.execute(
                '''
                SELECT * FROM otp_sessions 
                WHERE phone = ? AND verified = 0
                ORDER BY created_at DESC 
                LIMIT 1
                ''',
                (phone,)
            ).fetchone()
            
            if not otp_record:
                return {'success': False, 'message': 'No OTP request found for this phone. Please request a new OTP.'}
            
            # Check if OTP expired
            expiry_time = datetime.fromisoformat(otp_record['expires_at'])
            if datetime.now() > expiry_time:
                return {'success': False, 'message': 'OTP expired. Please request a new OTP.'}
            
            # Check attempt limit
            if otp_record['attempts'] >= self.max_attempts:
                return {'success': False, 'message': 'Too many failed attempts. Please request a new OTP.'}
            
            # Verify OTP
            if otp_record['otp_code'] == otp_code.strip():
                # Mark as verified
                db.execute(
                    '''
                    UPDATE otp_sessions 
                    SET verified = 1 
                    WHERE id = ?
                    ''',
                    (otp_record['id'],)
                )
                
                # Check if user exists; if not, create one
                user = db.execute(
                    'SELECT id FROM users WHERE phone = ?',
                    (phone,)
                ).fetchone()
                
                if not user:
                    # Create new citizen user
                    db.execute(
                        '''
                        INSERT INTO users (name, email, phone, password, role, phone_verified)
                        VALUES (?, ?, ?, ?, 'citizen', 1)
                        ''',
                        (f"Citizen {phone}", f"citizen_{phone}@grievanceconnect.local", phone, '')
                    )
                    user_id = db.execute('SELECT last_insert_rowid()').fetchone()[0]
                else:
                    user_id = user['id']
                    # Update phone_verified flag
                    db.execute(
                        'UPDATE users SET phone_verified = 1 WHERE id = ?',
                        (user_id,)
                    )
                
                db.commit()
                
                return {
                    'success': True,
                    'message': 'OTP verified successfully',
                    'user_id': user_id
                }
            else:
                # Increment attempts
                db.execute(
                    '''
                    UPDATE otp_sessions 
                    SET attempts = attempts + 1
                    WHERE id = ?
                    ''',
                    (otp_record['id'],)
                )
                db.commit()
                
                remaining = self.max_attempts - (otp_record['attempts'] + 1)
                if remaining > 0:
                    return {
                        'success': False,
                        'message': f'Invalid OTP. {remaining} attempt(s) remaining.'
                    }
                else:
                    return {
                        'success': False,
                        'message': 'Too many failed attempts. Please request a new OTP.'
                    }
                    
        except Exception as e:
            return {'success': False, 'message': f'Error verifying OTP: {str(e)}'}


# Initialize OTP Service
otp_service = OTPService()
