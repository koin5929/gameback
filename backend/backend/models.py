from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint, func
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
