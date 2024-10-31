from pydantic import BaseModel, EmailStr, Field

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
class UserCreate(BaseModel):
    email: EmailStr
    firstName: str
    lastName: str
    companyName: str
    password: str = Field(..., min_length=8)

class UserVerifyEmail(BaseModel):
    token: str

class UserResetPassword(BaseModel):
    token: str
    new_password: str = Field(..., min_length=8)

class UserEmail(BaseModel):
    email: EmailStr

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    is_verified: bool

    class Config:
        orm_mode = True
