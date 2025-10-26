# 빙고 포인트 시스템 - 구조 설명

## 📋 전체 구조

```
마인크래프트 서버
    ↓ (30분 플레이)
PointsPlugin → API → MariaDB/PostgreSQL
    ↓
홈페이지 (Render) → DB에서 포인트 조회
    ↓
빙고판 UI (9x9 = 81칸)
    ↓
플레이어 선택 (1포인트 차감)
    ↓
서버에서 /bingo-claim 명령어로 보상 지급
```

## 🗂️ 파일 구조

```
홈페이지/
├── backend/
│   ├── backend/
│   │   ├── main.py          # API 엔드포인트 (포인트, 빙고)
│   │   ├── models.py        # DB 모델 (PlayerPoints, BingoItem, PlayerBingo)
│   │   └── database.py      # DB 연결 설정
│   ├── requirements.txt     # Python 의존성
│   └── manage_bingo.py      # 빙고 아이템 관리 스크립트
├── plugin/
│   ├── src/main/java/
│   │   └── PointsPlugin.java    # 마인크래프트 플러그인
│   ├── pom.xml              # Maven 빌드 설정
│   ├── plugin.yml           # 플러그인 설정
│   └── config.yml           # 플러그인 config
├── web/
│   ├── index.html           # 홈페이지 (빙고판 UI 추가 필요)
│   └── style.css
└── render.yaml              # Render 배포 설정

```

## 🗄️ 데이터베이스 구조

### 1. player_points 테이블
```sql
uuid VARCHAR(36) PRIMARY KEY
points INT DEFAULT 0
playtime_minutes INT DEFAULT 0
last_earned DATETIME
updated_at DATETIME
```

### 2. bingo_items 테이블
```sql
id INT PRIMARY KEY
position INT UNIQUE (0-80)
tier VARCHAR(8)     # S+, S, A, B, C, D
item_name VARCHAR(128)
item_command TEXT   # 플러그인 실행 명령어
created_at DATETIME
```

### 3. player_bingo 테이블
```sql
id INT PRIMARY KEY
uuid VARCHAR(36)
bingo_position INT
bingo_item_id INT
claimed BOOLEAN DEFAULT FALSE
claimed_at DATETIME
created_at DATETIME
UNIQUE(uuid, bingo_position)
```

## 🎮 사용 방법

### 1. Render 설정

#### MariaDB 사용 시:
```yaml
# render.yaml
envVars:
  - key: DATABASE_URL
    value: mariadb+pymysql://사용자:비밀번호@외부IP:3306/DB이름
```

#### PostgreSQL 사용 시:
```yaml
# render.yaml
envVars:
  - key: DATABASE_URL
    value: postgresql://사용자:비밀번호@호스트/DB이름
```

### 2. 빙고 아이템 초기화

```bash
cd backend
python manage_bingo.py init
```

등급 분포:
- **S+**: 1개 (position 0)
- **S**: 3개 (position 1-3)
- **A**: 6개 (position 4-9)
- **B**: 18개 (position 10-27)
- **C**: 27개 (position 28-54)
- **D**: 26개 (position 55-80)

### 3. 마인크래프트 플러그인 설치

```bash
cd plugin
mvn clean package
```

생성된 `target/pointsplugin-1.0.0.jar` 파일을 서버의 `plugins` 폴더에 복사

#### config.yml 설정:
```yaml
api:
  url: "https://your-render-app.onrender.com"
  secret: "YOUR_SHARED_SECRET"
```

### 4. API 엔드포인트

#### 플러그인용:
- `POST /api/plugin/add-points/{uuid}` - 30분마다 포인트 지급

#### 홈페이지용:
- `GET /api/points/{uuid}` - 플레이어 포인트 조회
- `GET /api/bingo/items` - 빙고 아이템 목록
- `GET /api/bingo/player/{uuid}` - 플레이어가 선택한 빙고 칸들
- `POST /api/bingo/select/{uuid}` - 빙고 칸 선택 (1포인트 차감)

## 🔄 시스템 작동 방식

### 1. 포인트 지급
1. 플레이어가 서버 접속
2. PointsPlugin이 1분마다 플레이타임 체크
3. 30분마다 API 호출 → DB에 포인트 추가
4. 플레이어에게 메시지 표시

### 2. 빙고판 선택
1. 홈페이지에서 로그인 (Microsoft OAuth 필요)
2. 보유 포인트 확인
3. 빙고판에서 칸 선택 (1포인트 차감)
4. 선택한 칸은 영구적으로 저장

### 3. 보상 지급
1. 플레이어가 서버에서 `/bingo-claim` 명령어 실행
2. 플러그인이 선택한 빙고 칸 확인
3. 각 칸의 `item_command` 실행
4. 보상 지급 완료

## ⚙️ 환경 변수

### Render 환경 변수:
- `DATABASE_URL` - MariaDB/PostgreSQL 연결 주소
- `SHARED_SECRET` - 플러그인 API 인증 키
- `ALLOWED_ORIGINS` - CORS 설정
- `DISCORD_BOT_TOKEN` - Discord 봇 토큰
- `RUN_DISCORD_BOT` - Discord 봇 실행 여부

### 플러그인 설정:
- `api.url` - 홈페이지 API URL
- `api.secret` - SHARED_SECRET과 동일

## 📝 TODO

- [ ] 홈페이지에 빙고판 UI 추가 (9x9 그리드)
- [ ] Microsoft OAuth 로그인 구현
- [ ] 포인트 조회 기능
- [ ] 빙고 보상 지급 시스템 완성

## 🚀 배포 순서

1. Render에서 MySQL/PostgreSQL 데이터베이스 추가
2. DATABASE_URL 환경변수 설정
3. Backend 배포
4. 빙고 아이템 초기화 (`python manage_bingo.py init`)
5. 마인크래프트 플러그인 빌드 및 설치
6. 홈페이지 UI 업데이트

