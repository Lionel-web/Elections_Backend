from fastapi import APIRouter
from app.core.db import get_db

router = APIRouter(prefix="/test")

@router.get("/db")
async def test_db():
    db = get_db()
    try:
        # Count documents in users collection
        user_count = db.users.count_documents({})
        return {"status": "DB connected ✅", "users_count": user_count}
    except Exception as e:
        return {"status": "DB connection failed ❌", "error": str(e)}
