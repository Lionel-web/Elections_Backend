from fastapi import APIRouter, HTTPException, Depends
from app.schemas.user import UserCreate
from app.core.db import get_db 
from passlib.context import CryptContext
import secrets
from app.utils.dependencies import get_current_admin, get_current_user  # you'll need a dependency to check admin

router = APIRouter(prefix="/admin", tags=["Administration"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Example dependency to allow only admins
def admin_only(current_user=Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Accès réservé aux admins")
    return current_user

@router.post("/create-user")
def create_user(
    user_data: UserCreate,
    db = Depends(get_db),
    _: dict = Depends(get_current_admin)  # only admin can call
):
    # Check if email already exists
    if db.users.find_one({"email": user_data.email}):
        raise HTTPException(status_code=400, detail="Email déjà utilisé")

    user_dict = {
        "email": user_data.email,
        "role": user_data.role,
        "is_active": True
    }

    if user_data.role == "admin":
        if not user_data.password:
            raise HTTPException(status_code=400, detail="Mot de passe requis pour l'admin")
        user_dict["hashed_password"] = pwd_context.hash(user_data.password)
        user_dict["code_unique"] = None

    elif user_data.role == "chef_bureau":
        # Generate unique code
        code = user_data.code_unique or secrets.token_hex(4)
        while db.users.find_one({"code_unique": code}):
            code = secrets.token_hex(4)
        user_dict["code_unique"] = code
        user_dict["hashed_password"] = None

    result = db.users.insert_one(user_dict)

    return {
        "id": str(result.inserted_id),
        "email": user_dict["email"],
        "role": user_dict["role"],
        "code_unique": user_dict.get("code_unique")
    }