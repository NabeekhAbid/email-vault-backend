# app/routes/user.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..models import User, EmailVerification, PasswordReset, FailedLogin
from ..schemas import UserCreate,UserLogin, UserVerifyEmail, UserResetPassword, UserEmail
from ..database import get_db
from app.services import UserService
from app.utils import Utils
from datetime import datetime, timedelta
from uuid import uuid4  # Correctly import uuid4

utils = Utils()
router = APIRouter()
@router.post("/login", status_code=status.HTTP_200_OK)
def login(user: UserLogin, db: Session = Depends(get_db)):
    # Check if user exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if not existing_user:
        # Log failed login attempt
        failed_login = FailedLogin(
            user_id=None,  # Assuming user_id is None if the user doesn't exist
            attempted_at=datetime.now()
        )
        db.add(failed_login)
        db.commit()
        
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )

    # Verify password
    if not utils.verify_password(user.password, existing_user.password_hash):
        # Log failed login attempt
        failed_login = FailedLogin(
            user_id=existing_user.id,
            attempted_at=datetime.now()
        )
        db.add(failed_login)
        db.commit()
        
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password."
        )

    # Optionally, you can return a token or user info here
    return {"message": "Login successful", "user": {"email": existing_user.email, "is_verified": existing_user.is_verified}}
@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered."
        )
    # Create new user
    new_user = User(
        firstName = user.firstName,
        lastName = user.lastName,
        companyName = user.companyName,
        email=user.email,
        password_hash=utils.hash_password(user.password)  # Hash the password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    # Send verification email
    user_service = UserService()
    
    user_service.send_verification_email(new_user)
    return {"message": "User created successfully, please verify your email."}
@router.post("/verify-email", status_code=status.HTTP_200_OK)
def verify_email(verification: UserVerifyEmail, db: Session = Depends(get_db)):
    # Check for the verification token
    email_verification = db.query(EmailVerification).filter(EmailVerification.token == verification.token).first()
    if not email_verification:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired verification token."
        )
    # Update user verification status
    user = db.query(User).filter(User.id == email_verification.user_id).first()
    if user:
        user.is_verified = True
        db.commit()
    return {"message": "Email verified successfully."}
@router.post("/reset-password", status_code=status.HTTP_200_OK)
def reset_password_request(reset_info: UserEmail, db: Session = Depends(get_db)):
    # Check if user exists
    user = db.query(User).filter(User.email == reset_info.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )

    # Create a password reset token
    password_reset_token = str(uuid4())
    expires_at = datetime.now() + timedelta(hours=1)  # Set expiration to 1 hour

    password_reset = PasswordReset(
        user_id=user.id,
        token=password_reset_token,
        created_at=datetime.now(),
        expires_at=expires_at
    )
    
    db.add(password_reset)
    db.commit()

    # Send password reset email
    user_service = UserService()
    user_service.send_password_reset_email(user.email, password_reset_token)

    return {"message": "Password reset link has been sent to your email."}


@router.post("/confirm-reset-password", status_code=status.HTTP_200_OK)
def confirm_reset_password(reset_info: UserResetPassword, db: Session = Depends(get_db)):
    # Verify the reset token
    password_reset = db.query(PasswordReset).filter(PasswordReset.token == reset_info.token).first()
    if not password_reset or password_reset.expires_at < datetime.now():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired password reset token."
        )

    # Update the user's password
    user = db.query(User).filter(User.id == password_reset.user_id).first()
    if user:
        user.password_hash = utils.hash_password(reset_info.new_password)  # Hash the new password
        db.commit()
        
        # Optionally, mark the reset token as used
        password_reset.used_at = datetime.now()
        db.commit()

    return {"message": "Password has been reset successfully."}
@router.post("/login-failed", status_code=status.HTTP_200_OK)
def log_failed_login(user_id: int, db: Session = Depends(get_db)):
    # Log failed login attempt
    failed_login = FailedLogin(
        user_id=user_id
    )
    db.add(failed_login)
    db.commit()
    return {"message": "Failed login attempt recorded."}