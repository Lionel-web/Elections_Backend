from pydantic import BaseModel, EmailStr
from typing import Literal, Optional

class UserCreate(BaseModel):
    email: EmailStr
    role: Literal["admin", "chef_bureau"]
    password: Optional[str] = None       # pour admin
    code_unique: Optional[str] = None    # pour chef_bureau

class LoginRequest(BaseModel):
    email: EmailStr
    role: Literal["admin", "chef_bureau"]
    password: Optional[str] = None       # requis pour admin
    code: Optional[str] = None        