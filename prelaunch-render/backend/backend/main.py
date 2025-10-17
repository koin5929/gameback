import os, re, httpx
from fastapi import FastAPI, Depends, HTTPException, Header, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, constr
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from dotenv import load_dotenv

from .database import Base, engine, SessionLocal
from .models import Reservation

load_dotenv()

ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*")
SHARED_SECRET = os.getenv("SHARED_SECRET", "CHANGE_ME_32CHARS")

app = FastAPI(title="Prelaunch API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGINS] if ALLOWED_ORIGINS != "*" else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class RegisterIn(BaseModel):
    discord_id: constr(strip_whitespace=True, min_length=1, max_length=64)
    nickname:   constr(strip_whitespace=True, min_length=1, max_length=128)
    mc_name:    constr(strip_whitespace=True, min_length=3, max_length=16)

class ReservationOut(BaseModel):
    id: int
    discord_id: str
    nickname: str
    created_at: str

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

def verify_secret(x_prelaunch_secret: str = Header(default="")):
    if SHARED_SECRET and x_prelaunch_secret != SHARED_SECRET:
        raise HTTPException(status_code=401, detail="Unauthorized")

UUID_RE = re.compile(r"^[0-9a-fA-F-]{32,36}$")
NAME_RE = re.compile(r"^[a-zA-Z0-9_]{3,16}$")

async def fetch_json(url, timeout=5.0):
    async with httpx.AsyncClient(timeout=timeout) as client:
        r = await client.get(url)
        if r.status_code == 204:
            return None
        r.raise_for_status()
        try:
            return r.json()
        except Exception:
            return None

async def resolve_uuid(name: str):
    if not NAME_RE.match(name):
        return None
    try:
        j = await fetch_json(f"https://api.mojang.com/users/profiles/minecraft/{name}", timeout=4.0)
        if j and "id" in j:
            raw = j["id"]
            uuid = f"{raw[0:8]}-{raw[8:12]}-{raw[12:16]}-{raw[16:20]}-{raw[20:32]}"
            return {"uuid": uuid.lower(), "name": j.get("name", name)}
    except Exception:
        pass
    try:
        j = await fetch_json(f"https://api.ashcon.app/mojang/v2/user/{name}", timeout=4.0)
        if j and "uuid" in j:
            return {"uuid": j["uuid"].lower(), "name": j.get("username", name)}
    except Exception:
        pass
    try:
        j = await fetch_json(f"https://api.minetools.eu/uuid/{name}", timeout=4.0)
        if j and j.get("status") == "OK" and "id" in j:
            raw = j["id"]
            uuid = f"{raw[0:8]}-{raw[8:12]}-{raw[12:16]}-{raw[16:20]}-{raw[20:32]}"
            return {"uuid": uuid.lower(), "name": name}
    except Exception:
        pass
    return None

class ValidateOut(BaseModel):
    ok: bool
    uuid: str | None = None
    name: str | None = None

@app.get("/api/validate-name", response_model=ValidateOut)
async def validate_name(name: str = Query(..., min_length=3, max_length=16)):
    data = await resolve_uuid(name)
    if not data:
        return ValidateOut(ok=False)
    return ValidateOut(ok=True, uuid=data["uuid"], name=data["name"])

@app.post("/api/register", dependencies=[Depends(verify_secret)], response_model=ReservationOut)
async def register(payload: RegisterIn, db: Session = Depends(get_db)):
    resolved = await resolve_uuid(payload.mc_name)
    if not resolved:
        raise HTTPException(status_code=422, detail="Invalid Minecraft name")
    entry = Reservation(
        discord_id=payload.discord_id,
        nickname=payload.nickname,
        mc_uuid=resolved["uuid"],
        mc_name=resolved["name"],
    )
    db.add(entry)
    try:
        db.commit()
        db.refresh(entry)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Already registered")
    return ReservationOut(
        id=entry.id,
        discord_id=entry.discord_id,
        nickname=entry.nickname,
        created_at=entry.created_at.isoformat() if entry.created_at else ""
    )

@app.get("/api/list")
def list_public(db: Session = Depends(get_db)):
    rows = db.query(Reservation).order_by(Reservation.created_at.asc()).all()
    return [{"nickname": r.nickname, "mc_name": r.mc_name, "created_at": r.created_at.isoformat()} for r in rows]

@app.get("/")
def index():
    return {"message": "Prelaunch API running. Use GET /api/list for public list."}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("backend.main:app", host="0.0.0.0", port=port, reload=False)
