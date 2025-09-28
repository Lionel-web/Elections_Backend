from fastapi import APIRouter, HTTPException
from app.schemas.user import LoginRequest
from app.core.db import db, pwd_context, get_db
from datetime import datetime, timedelta
from jose import jwt
import os

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

router = APIRouter(prefix="/auth", tags=["Authentication"])

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/login")
def login(data: LoginRequest):
    db = get_db()
    user = db.users.find_one({"email": data.email})

    if not user or not user.get("is_active", True):
        raise HTTPException(status_code=401, detail="Utilisateur non trouvé ou inactif")

    if user["role"] != data.role:
        raise HTTPException(status_code=403, detail="Accès refusé pour ce rôle")

    if user["role"] == "admin":
        if not data.password:
            raise HTTPException(status_code=400, detail="Mot de passe requis")
        password = str(data.password)[:72]
        # Truncate to 72 bytes for bcrypt
        if not pwd_context.verify(password, user.get("hashed_password", "")):
            raise HTTPException(status_code=401, detail="Mot de passe incorrect")

    elif user["role"] == "chef_bureau":
        if not data.code:
            raise HTTPException(status_code=400, detail="Code unique requis")
        if data.code != user.get("code_unique"):
            raise HTTPException(status_code=401, detail="Code unique incorrect")

    token = create_access_token({"sub": str(user["_id"]), "role": user["role"]})

    return {
        "message": f"Connexion réussie pour {user['role']}",
        "email": user["email"],
        "access_token": token,
        "token_type": "bearer",
        "role": user["role"]
    }
