import os, re, httpx, secrets
from fastapi import FastAPI, Depends, HTTPException, Header, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse
from pydantic import BaseModel, constr
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from dotenv import load_dotenv
from typing import Optional

from .database import Base, engine, SessionLocal
from .models import Reservation, PlayerPoints, BingoItem, PlayerBingo

# ----------------- 기본 설정 -----------------
load_dotenv()
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*")
SHARED_SECRET = os.getenv("SHARED_SECRET", "CHANGE_ME_32CHARS")

app = FastAPI(title="Prelaunch API", version="1.0.3")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGINS] if ALLOWED_ORIGINS != "*" else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------- DB -----------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ----------------- 모델 -----------------
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

# ----------------- 유틸 (UUID 조회) -----------------
NAME_RE = re.compile(r"^[a-zA-Z0-9_]{3,16}$")

async def fetch_json(url, timeout=5.0):
    async with httpx.AsyncClient(timeout=timeout) as client:
        r = await client.get(url)
        if r.status_code in (204, 404):
            return None
        try:
            return r.json()
        except Exception:
            return None

async def resolve_uuid(name: str):
    if not NAME_RE.match(name):
        return None
    try:
        # 1) Mojang
        j = await fetch_json(f"https://api.mojang.com/users/profiles/minecraft/{name}", 4.0)
        if j and "id" in j:
            raw = j["id"]
            uuid = f"{raw[0:8]}-{raw[8:12]}-{raw[12:16]}-{raw[16:20]}-{raw[20:32]}"
            return {"uuid": uuid.lower(), "name": j.get("name", name)}
    except Exception:
        pass
    try:
        # 2) Ashcon
        j = await fetch_json(f"https://api.ashcon.app/mojang/v2/user/{name}", 4.0)
        if j and "uuid" in j:
            return {"uuid": j["uuid"].lower(), "name": j.get("username", name)}
    except Exception:
        pass
    try:
        # 3) Minetools
        j = await fetch_json(f"https://api.minetools.eu/uuid/{name}", 4.0)
        if j and j.get("status") == "OK" and "id" in j:
            raw = j["id"]
            uuid = f"{raw[0:8]}-{raw[8:12]}-{raw[12:16]}-{raw[16:20]}-{raw[20:32]}"
            return {"uuid": uuid.lower(), "name": name}
    except Exception:
        pass
    return None

# ----------------- API 라우트 -----------------
class ValidateOut(BaseModel):
    ok: bool
    uuid: str | None = None
    name: str | None = None

@app.get("/api/health")
def health():
    return {"ok": True}

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
        created_at=entry.created_at.isoformat() if entry.created_at else "",
    )

@app.get("/api/list")
def list_public(db: Session = Depends(get_db)):
    rows = db.query(Reservation).order_by(Reservation.created_at.asc()).all()
    return [
        {"nickname": r.nickname, "mc_name": r.mc_name, "created_at": r.created_at.isoformat()}
        for r in rows
    ]

# ----------------- 포인트 & 빙고판 API -----------------
class PointsOut(BaseModel):
    uuid: str
    points: int
    playtime_minutes: int

@app.get("/api/points/{uuid}", response_model=PointsOut)
def get_points(uuid: str, db: Session = Depends(get_db)):
    player = db.query(PlayerPoints).filter(PlayerPoints.uuid == uuid).first()
    if not player:
        # 첫 접속 시 생성
        player = PlayerPoints(uuid=uuid, points=0, playtime_minutes=0)
        db.add(player)
        db.commit()
        db.refresh(player)
    return PointsOut(
        uuid=player.uuid,
        points=player.points,
        playtime_minutes=player.playtime_minutes
    )

class BingoItemOut(BaseModel):
    id: int
    position: int
    tier: str
    item_name: str

@app.get("/api/bingo/items")
def get_bingo_items(tier: str = None, db: Session = Depends(get_db)):
    query = db.query(BingoItem).order_by(BingoItem.position)
    if tier:
        items = query.filter(BingoItem.tier == tier).all()
    else:
        items = query.all()
    return [
        {
            "id": item.id,
            "position": item.position,
            "tier": item.tier,
            "item_name": item.item_name
        }
        for item in items
    ]

class PlayerBingoOut(BaseModel):
    position: int
    item_id: int
    claimed: bool

@app.get("/api/bingo/player/{uuid}")
def get_player_bingo(uuid: str, db: Session = Depends(get_db)):
    selections = db.query(PlayerBingo).filter(PlayerBingo.uuid == uuid).all()
    return [
        {
            "position": pb.bingo_position,
            "item_id": pb.bingo_item_id,
            "claimed": pb.claimed
        }
        for pb in selections
    ]

class SelectBingoIn(BaseModel):
    position: int
    item_id: int

@app.post("/api/bingo/select/{uuid}")
def select_bingo_slot(uuid: str, payload: SelectBingoIn, db: Session = Depends(get_db)):
    # 포인트 확인 (3 포인트 필요)
    player = db.query(PlayerPoints).filter(PlayerPoints.uuid == uuid).first()
    if not player or player.points < 3:
        raise HTTPException(status_code=400, detail="Insufficient points (need 3)")
    
    # 이미 선택했는지 확인
    existing = db.query(PlayerBingo).filter(
        PlayerBingo.uuid == uuid,
        PlayerBingo.bingo_position == payload.position
    ).first()
    
    if existing:
        raise HTTPException(status_code=409, detail="Already selected")
    
    # 포인트 차감 (3포인트)
    player.points -= 3
    db.add(player)
    
    # 빙고 선택 저장
    player_bingo = PlayerBingo(
        uuid=uuid,
        bingo_position=payload.position,
        bingo_item_id=payload.item_id,
        claimed=False
    )
    db.add(player_bingo)
    
    try:
        db.commit()
        db.refresh(player_bingo)
        return {"ok": True, "points_remaining": player.points}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to save selection")

# ----------------- 플러그인 API (암호화 필요) -----------------
class AddPointsIn(BaseModel):
    minutes: int

@app.post("/api/plugin/add-points/{uuid}", dependencies=[Depends(verify_secret)])
def add_points(uuid: str, payload: AddPointsIn, db: Session = Depends(get_db)):
    """플러그인에서 30분마다 1포인트 추가"""
    from datetime import datetime
    
    player = db.query(PlayerPoints).filter(PlayerPoints.uuid == uuid).first()
    if not player:
        # 첫 접속 시 생성
        player = PlayerPoints(
            uuid=uuid,
            points=1,  # 첫 포인트 지급
            playtime_minutes=payload.minutes,
            last_earned=datetime.now()
        )
        db.add(player)
    else:
        # 포인트 추가 및 플레이타임 업데이트
        player.points += 1
        player.playtime_minutes = payload.minutes
        player.last_earned = datetime.now()
    
    try:
        db.commit()
        db.refresh(player)
        return {"ok": True, "total_points": player.points, "total_minutes": player.playtime_minutes}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to add points: {str(e)}")

class ClaimRewardOut(BaseModel):
    position: int
    item_id: int
    item_name: str
    item_command: str

@app.get("/api/plugin/unclaimed-rewards/{uuid}", dependencies=[Depends(verify_secret)])
def get_unclaimed_rewards(uuid: str, db: Session = Depends(get_db)):
    """플러그인: 미지급 보상 목록 조회"""
    # 선택했지만 아직 지급 안 된 보상 조회
    selections = db.query(PlayerBingo).filter(
        PlayerBingo.uuid == uuid,
        PlayerBingo.claimed == False
    ).all()
    
    rewards = []
    for sel in selections:
        # 빙고 아이템 정보 가져오기
        item = db.query(BingoItem).filter(BingoItem.id == sel.bingo_item_id).first()
        if item:
            rewards.append({
                "position": sel.bingo_position,
                "item_id": item.id,
                "item_name": item.item_name,
                "item_command": item.item_command
            })
    
    return rewards

@app.post("/api/plugin/claim-reward/{uuid}/{position}", dependencies=[Depends(verify_secret)])
def claim_reward(uuid: str, position: int, db: Session = Depends(get_db)):
    """플러그인: 보상 지급 완료 처리"""
    from datetime import datetime
    
    # bingo_position으로 조회 (화면 위치)
    selection = db.query(PlayerBingo).filter(
        PlayerBingo.uuid == uuid,
        PlayerBingo.bingo_position == position
    ).first()
    
    if not selection:
        raise HTTPException(status_code=404, detail="Selection not found")
    
    if selection.claimed:
        raise HTTPException(status_code=400, detail="Already claimed")
    
    # claimed 플래그 설정
    selection.claimed = True
    selection.claimed_at = datetime.now()
    
    try:
        db.commit()
        return {"ok": True}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to claim reward: {str(e)}")

# ----------------- 정적 파일 & SPA -----------------
# ⚠️ 반드시 맨 마지막에 둬야 함
app.mount("/assets", StaticFiles(directory="web/assets"), name="assets")

@app.get("/style.css", include_in_schema=False)
def style_css():
    return FileResponse("web/style.css")

@app.get("/", include_in_schema=False)
def index_html():
    return FileResponse("web/index.html")

@app.get("/{path:path}", include_in_schema=False)
def spa_fallback(path: str):
    # api 요청은 무시 (404)
    if path.startswith("api/"):
        raise HTTPException(status_code=404)
    return FileResponse("web/index.html")
