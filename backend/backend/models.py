from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint, func
from .database import Base

class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)
    discord_id = Column(String(64), nullable=False)            # 디스코드 계정
    mc_uuid    = Column(String(36), nullable=False)            # 하이픈 포함 UUID
    mc_name    = Column(String(16), nullable=False)            # 검증된 마지막 닉네임(표시용)
    nickname   = Column(String(128), nullable=False)           # 디스코드 표시명
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint("discord_id", name="uq_resv_discord"),
        UniqueConstraint("mc_uuid",    name="uq_resv_mcuuid"),
    )
