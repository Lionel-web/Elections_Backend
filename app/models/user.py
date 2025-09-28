# app/models/user.py
from beanie import Document, Indexed
from pydantic import BaseModel, EmailStr
from typing import Literal
from datetime import datetime

class User(Document):
    email: EmailStr
    hashed_password: str = None   # Pour admin
    role: Literal["admin", "chef_bureau"]
    code_unique: str = None       # Pour chef_bureau
    is_active: bool = True
    created_at: datetime = datetime.utcnow()
    
    class Settings:
        name = "users"
    