from fastapi import FastAPI
from app.routes import auth, admin
from app.core.db import init_db
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Système Électoral Camerounais")

origins = [
    "http://localhost:8080",  # your Vite frontend
    "https://elections-yaounde-6.onrender.com",  # add other allowed origins
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # allow all HTTP methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # allow all headers
)

@app.on_event("startup")
def startup_event():
    init_db()

# Include routers
app.include_router(auth.router)
app.include_router(admin.router)

@app.get("/")
async def root():
    return {"message": "API Décompte Électoral en ligne"}

from app.routes import test_db
app.include_router(test_db.router)
