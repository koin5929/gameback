from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint, Boolean, Text, func
from .database import Base

class Reservation(Base):
    __tablename__ = "reservations"
    id = Column(Integer, primary_key=True, index=True)
    discord_id = Column(String(64), nullable=False)
    mc_uuid    = Column(String(36), nullable=False)
    mc_name    = Column(String(16), nullable=False)
    nickname   = Column(String(128), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    __table_args__ = (
        UniqueConstraint("discord_id", name="uq_resv_discord"),
        UniqueConstraint("mc_uuid",    name="uq_resv_mcuuid"),
    )

class PlayerPoints(Base):
    __tablename__ = "player_points"
    uuid = Column(String(36), primary_key=True, index=True)
    points = Column(Integer, default=0, nullable=False)
    last_earned = Column(DateTime(timezone=True), nullable=True)
    playtime_minutes = Column(Integer, default=0, nullable=False)  # 누적 플레이 시간 (분)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class BingoItem(Base):
    __tablename__ = "bingo_items"
    id = Column(Integer, primary_key=True, index=True)
    position = Column(Integer, nullable=False, unique=True)  # 0-80 (9x9 빙고판)
    tier = Column(String(8), nullable=False)  # S+, S, A, B, C, D
    item_name = Column(String(128), nullable=False)
    item_command = Column(Text, nullable=False)  # 플러그인에서 실행할 명령어
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class PlayerBingo(Base):
    __tablename__ = "player_bingo"
    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String(36), nullable=False, index=True)
    bingo_position = Column(Integer, nullable=False)
    bingo_item_id = Column(Integer, nullable=False)
    claimed = Column(Boolean, default=False, nullable=False)
    claimed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    __table_args__ = (
        UniqueConstraint("uuid", "bingo_position", name="uq_player_bingo"),
    )
