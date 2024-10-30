from typing import List, Dict, Any
from uuid import uuid4  # Correctly import uuid4
import os
from dotenv import load_dotenv
from mailjet_rest import Client
from datetime import datetime, timedelta
from urllib.parse import urlencode
from ..models import User, EmailVerification  # Import the EmailVerification model
from app.database import SessionLocal 
load_dotenv()
class UserService:
    """Service for handling user operations."""
    def __init__(self):
        self.mailjet = Client(auth=(os.getenv('MAILJET_API_KEY_'), os.getenv('MAILJET_API_SECRET_')), version='v3.1')

    def send_verification_email(self, user: User) -> None:
        """Send a verification email to the user with a unique verification link."""
        
        # Generate a unique token
        verification_token = str(uuid4())
        
        # Set token expiration (e.g., 24 hours from now)
        expires_at = datetime.now() + timedelta(hours=24)
        print(user)
        # Create a new EmailVerification entry
        email_verification = EmailVerification(
            user_id=user.id,
            token=verification_token,
            created_at=datetime.now(),
            expires_at=expires_at
        )
        
        # Assuming you have a function to get a session
        db = SessionLocal()
        db.add(email_verification)
        db.commit()  # Save the email verification entry

        # Construct the verification link with the token
        base_url = os.getenv('FRONT_END_BASE_URL')  
        print(base_url)
        params = urlencode({"token": verification_token, "email": user.email})
        verification_path = "/verify-token"  
        verification_link = f"{base_url}{verification_path}?{params}"
        print(verification_link)

        # Define email content
        data = {
            'Messages': [
                {
                    "From": {
                        "Email": "hm.nabeekh@gmail.com",
                        "Name": "email-vault"
                    },
                    "To": [
                        {
                            "Email": user.email,
                            "Name": "User"
                        }
                    ],
                    "Subject": "Your Verification Email",
                    "TextPart": "Please verify your email",
                    "HTMLPart": f"<h3>Dear {user.email},</h3>"
                                f"<p>Click the {verification_link} to verify your email.</p>"
                }
            ]
        }

        # Send the email
        try:
            result = self.mailjet.send.create(data=data)
            if result.status_code == 200:
                print(f"Verification email sent to {user.email}")
            else:
                print(f"Failed to send email to {user.email}. Error: {result.status_code} - {result.json()}")
        except Exception as e:
            print(f"An error occurred while sending the email: {e}")
    def send_password_reset_email(self, email: str, token: str) -> None:
        """Send a password reset email to the user with a unique reset link."""
        
        # Construct the password reset link
        base_url = os.getenv('FRONT_END_BASE_URL')  # Get the base URL from environment variables
        if not base_url:
            raise EnvironmentError("FRONT_END_BASE_URL is not set in environment variables.")
        
        reset_path = "/reset-password"  # Define the reset path
        params = urlencode({"token": token, "email": email})
        reset_link = f"{base_url}{reset_path}?{params}"

        # Define email content
        data = {
            'Messages': [
                {
                    "From": {
                        "Email": "hm.nabeekh@gmail.com",
                        "Name": "email-vault"
                    },
                    "To": [
                        {
                            "Email": email,
                            "Name": "User"
                        }
                    ],
                    "Subject": "Password Reset Request",
                    "TextPart": "Click the link to reset your password.",
                    "HTMLPart": f"<h3>Dear User,</h3>"
                                f"<p>Click the {reset_link} to reset your password.</p>"
                }
            ]
        }

        # Send the email
        try:
            result = self.mailjet.send.create(data=data)
            if result.status_code == 200:
                print(f"Password reset email sent to {email}")
            else:
                print(f"Failed to send email to {email}. Error: {result.status_code} - {result.json()}")
        except Exception as e:
            print(f"An error occurred while sending the email: {e}")