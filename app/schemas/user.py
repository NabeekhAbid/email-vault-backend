# app/schemas/user.py

from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
class UserCreate(BaseModel):
    email: EmailStr
    firstName: str
    lastName: str
    companyName: str
    password: str = Field(..., min_length=8)  # Enforce minimum password length

class UserVerifyEmail(BaseModel):
    token: str

class UserResetPassword(BaseModel):
    token: str
    new_password: str = Field(..., min_length=8)

class UserEmail(BaseModel):
    email: str = Field(..., min_length=8)
  

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    is_verified: bool

    class Config:
        orm_mode = True 