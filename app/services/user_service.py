from uuid import uuid4
import os
from dotenv import load_dotenv
from mailjet_rest import Client
from datetime import datetime, timedelta
from urllib.parse import urlencode
from ..models import User, EmailVerification
from app.database import SessionLocal 

load_dotenv()

class UserService:
    """Service for handling user operations."""
    
    def __init__(self):
        self.mailjet = Client(auth=(os.getenv('MAILJET_API_KEY_'), os.getenv('MAILJET_API_SECRET_')), version='v3.1')

    def send_verification_email(self, user: User) -> None:
        """Send a verification email to the user with a unique verification link."""
        
        verification_token = str(uuid4())
        expires_at = datetime.now() + timedelta(hours=24)
        
        email_verification = EmailVerification(
            user_id=user.id,
            token=verification_token,
            created_at=datetime.now(),
            expires_at=expires_at
        )
        
        db = SessionLocal()
        db.add(email_verification)
        db.commit()

        base_url = os.getenv('FRONT_END_BASE_URL')
        params = urlencode({"token": verification_token, "email": user.email})
        verification_link = f"{base_url}/verify-token?{params}"

        data = {
            'Messages': [
                {
                    "From": {
                        "Email": "hm.nabeekh@gmail.com",
                        "Name": "email-vault"
                    },
                    "To": [{"Email": user.email, "Name": "User"}],
                    "Subject": "Your Verification Email",
                    "HTMLPart": f"<h3>Dear {user.email},</h3><p>Click <a href='{verification_link}'>here</a> to verify your email.</p>"
                }
            ]
        }

        try:
            result = self.mailjet.send.create(data=data)
            if result.status_code == 200:
                print(f"Verification email sent to {user.email}")
            else:
                print(f"Failed to send email. Error: {result.status_code} - {result.json()}")
        except Exception as e:
            print(f"An error occurred while sending the email: {e}")

    def send_password_reset_email(self, email: str, token: str) -> None:
        """Send a password reset email to the user with a unique reset link."""
        
        base_url = os.getenv('FRONT_END_BASE_URL')
        if not base_url:
            raise EnvironmentError("FRONT_END_BASE_URL is not set in environment variables.")
        
        params = urlencode({"token": token, "email": email})
        reset_link = f"{base_url}/reset-password?{params}"

        data = {
            'Messages': [
                {
                    "From": {
                        "Email": "hm.nabeekh@gmail.com",
                        "Name": "email-vault"
                    },
                    "To": [{"Email": email, "Name": "User"}],
                    "Subject": "Password Reset Request",
                    "HTMLPart": f"<h3>Dear User,</h3><p>Click <a href='{reset_link}'>here</a> to reset your password.</p>"
                }
            ]
        }

        try:
            result = self.mailjet.send.create(data=data)
            if result.status_code == 200:
                print(f"Password reset email sent to {email}")
            else:
                print(f"Failed to send email. Error: {result.status_code} - {result.json()}")
        except Exception as e:
            print(f"An error occurred while sending the email: {e}")
