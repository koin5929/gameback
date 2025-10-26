"""
빙고 아이템 관리 스크립트

사용법:
python manage_bingo.py init   # 빙고판 초기화
python manage_bingo.py list    # 빙고 아이템 목록
python manage_bingo.py add <position> <tier> <name> <command>  # 아이템 추가
"""

import os
import sys
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, UniqueConstraint, func
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./prelaunch.db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# BingoItem 모델
class BingoItem(Base):
    __tablename__ = "bingo_items"
    id = Column(Integer, primary_key=True, index=True)
    position = Column(Integer, nullable=False, unique=True)
    tier = Column(String(8), nullable=False)
    item_name = Column(String(128), nullable=False)
    item_command = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

def init_bingo():
    """빙고판 초기화 - 등급별 분포 설정"""
    db = SessionLocal()
    try:
        # 기존 아이템 확인
        existing = db.query(BingoItem).count()
        if existing > 0:
            print("⚠️ 이미 빙고 아이템이 존재합니다. 계속하시겠습니까? (y/n)")
            ans = input().lower()
            if ans != 'y':
                print("취소되었습니다.")
                return
            # 기존 아이템 삭제
            db.query(BingoItem).delete()
        
        # 등급별 포지션 정의
        positions = []
        
        # S+ 등급: 1개 (0번)
        positions.append((0, "S+", "최고급 보상", "give {player} diamond 64"))
        
        # S 등급: 3개
        for i in range(1, 4):
            positions.append((i, "S", f"S급 보상 {i}", f"give {{player}} emerald_block 32"))
        
        # A 등급: 6개
        for i in range(4, 10):
            positions.append((i, "A", f"A급 보상 {i-3}", f"give {{player}} gold_block 16"))
        
        # B 등급: 18개
        for i in range(10, 28):
            positions.append((i, "B", f"B급 보상 {i-9}", f"give {{player}} iron_block 8"))
        
        # C 등급: 27개
        for i in range(28, 55):
            positions.append((i, "C", f"C급 보상 {i-27}", f"give {{player}} coal_block 4"))
        
        # D 등급: 26개 (나머지)
        for i in range(55, 81):
            positions.append((i, "D", f"D급 보상 {i-54}", f"give {{player}} cobblestone 32"))
        
        # DB에 추가
        for pos, tier, name, cmd in positions:
            item = BingoItem(position=pos, tier=tier, item_name=name, item_command=cmd)
            db.add(item)
        
        db.commit()
        print(f"✅ 빙고판 81칸 초기화 완료!")
        print(f"   S+: 1개, S: 3개, A: 6개, B: 18개, C: 27개, D: 26개")
        
    except Exception as e:
        db.rollback()
        print(f"❌ 오류: {e}")
    finally:
        db.close()

def list_items():
    """빙고 아이템 목록 출력"""
    db = SessionLocal()
    try:
        items = db.query(BingoItem).order_by(BingoItem.position).all()
        
        print("\n빙고 아이템 목록 (총", len(items), "개):\n")
        for item in items:
            print(f"  [{item.position:02d}] {item.tier:2s} | {item.item_name}")
    except Exception as e:
        print(f"❌ 오류: {e}")
    finally:
        db.close()

def add_item(position, tier, name, command):
    """빙고 아이템 추가"""
    db = SessionLocal()
    try:
        # 이미 존재하는지 확인
        existing = db.query(BingoItem).filter(BingoItem.position == int(position)).first()
        if existing:
            print(f"❌ Position {position}에 이미 아이템이 존재합니다.")
            return
        
        if int(position) < 0 or int(position) > 80:
            print("❌ Position은 0-80 사이여야 합니다.")
            return
        
        item = BingoItem(
            position=int(position),
            tier=tier,
            item_name=name,
            item_command=command
        )
        db.add(item)
        db.commit()
        print(f"✅ 아이템 추가 완료!")
    except Exception as e:
        db.rollback()
        print(f"❌ 오류: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "init":
        init_bingo()
    elif cmd == "list":
        list_items()
    elif cmd == "add":
        if len(sys.argv) < 6:
            print("사용법: python manage_bingo.py add <position> <tier> <name> <command>")
            sys.exit(1)
        add_item(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    else:
        print(f"알 수 없는 명령어: {cmd}")
        print(__doc__)

