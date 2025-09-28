from pymongo import MongoClient
import os
from dotenv import load_dotenv
from passlib.context import CryptContext
from datetime import datetime

load_dotenv()

client = None
db = None
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def init_db():
    global client, db
    client = MongoClient(os.getenv("MONGODB_URI"))
    db_name = os.getenv("DB_NAME")
    db = client[db_name]
    print(f"✅ Connecté à MongoDB Atlas : {db_name}")

    # Créer admin par défaut si inexistant
    create_default_admin()
# app/core/db.py
def get_db():
    if db is None:
        raise RuntimeError("DB not initialized")
    return db


def create_default_admin():
    admin_email = os.getenv("ADMIN_EMAIL")
    admin_password = os.getenv("ADMIN_PASSWORD")

    if not admin_password:
        print("⚠️ Aucun mot de passe admin défini")
        return

    # Tronquer à 72 caractères pour bcrypt
    admin_password = admin_password[:72]

    if db.users.find_one({"email": admin_email, "role": "admin"}) is None:
        hashed_password = pwd_context.hash(admin_password)
        db.users.insert_one({
            "email": admin_email,
            "hashed_password": hashed_password,
            "role": "admin",
            "is_active": True,
            "created_at": datetime.utcnow()
        })
        print(f"✅ Admin par défaut créé : {admin_email}")
    else:
        print("ℹ️ Admin par défaut déjà présent")
