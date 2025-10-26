# Render 설정 가이드

## 📋 Render Dashboard에서 해야 할 작업

### 1️⃣ MySQL 데이터베이스 추가 (유료 플랜 기준)

1. **Render Dashboard 접속**
   - https://dashboard.render.com 접속

2. **New + 버튼 클릭** → **Add Database** 선택

3. **MySQL 설정**
   ```
   Name: ramjwi-database (원하는 이름)
   Database: ramjwi (DB 이름)
   User: admin (또는 원하는 사용자명)
   Region: Singapore (가장 가까운 지역)
   ```

4. **생성 후 정보 확인**
   - Internal Database URL: `mysql://...` (이것을 복사!)

### 2️⃣ Web Service에 데이터베이스 연결

1. **현재 실행 중인 Web Service 클릭**

2. **Environment 탭 이동**

3. **DATABASE_URL 환경변수 설정**
   
   **방법 A: GUI에서 설정 (권장)**
   ```
   Key: DATABASE_URL
   Value: (MySQL 생성 후 받은 Internal URL)
   ```
   
   Internal URL 형식:
   ```
   mysql://user:password@hostname:3306/database_name
   ```
   
   **여기에 Python용 경로 변경 필요:**
   ```
   # mysql:// → mariadb+pymysql:// 로 변경
   mariadb+pymysql://user:password@hostname:3306/database_name
   ```

4. **다른 환경변수도 확인**
   - `SHARED_SECRET`: 플러그인 인증용 (랜덤 문자열)
   - `DISCORD_BOT_TOKEN`: Discord 봇 토큰
   - `ALLOWED_ORIGINS`: "*" (모든 도메인 허용)

### 3️⃣ Alternative: PostgreSQL 사용 (무료)

PostgreSQL을 사용하고 싶다면:

1. **New + 버튼** → **Add Database** → **PostgreSQL** 선택
2. Free 플랜 선택
3. Internal URL 복사
4. DATABASE_URL 설정:
   ```
   postgresql://user:password@hostname/database_name
   ```

## ⚙️ render.yaml 수정 안내

### Option 1: Render Dashboard에서 설정 (추천)
- render.yaml은 그대로 두고
- Dashboard → Environment에서 직접 설정

### Option 2: render.yaml에 하드코딩 (비권장)
```yaml
envVars:
  - key: DATABASE_URL
    value: "mariadb+pymysql://user:pass@hostname:3306/dbname"
```

⚠️ **보안상 추천하지 않습니다!** Dashboard에서만 관리하세요.

## 🔧 실제 설정 예시

### MySQL을 사용하는 경우:

**Render Dashboard → Environment:**
```
DATABASE_URL = mariadb+pymysql://admin:XXXXX@dpg-XXXXX.oregon-postgres.render.com:5432/ramjwi_XXXX
```

**파일 설정 (참고용, 실제로는 Dashboard에서 설정)**
```yaml
# render.yaml (선택사항)
envVars:
  - key: DATABASE_URL
    sync: false  # Dashboard에서 관리
```

### PostgreSQL을 사용하는 경우:

**Render Dashboard → Environment:**
```
DATABASE_URL = postgresql://user:pass@dpg-xxxxx.oregon-postgres.render.com:5432/ramjwi_xxxx
```

## 📝 체크리스트

- [ ] Render에서 MySQL 또는 PostgreSQL 추가
- [ ] Internal URL 복사
- [ ] `mariadb+pymysql://` 또는 `postgresql://` 형식으로 변경
- [ ] Web Service → Environment → DATABASE_URL 설정
- [ ] SHARED_SECRET 환경변수 설정 (랜덤 32자)
- [ ] Redeploy 실행
- [ ] 서버 로그 확인

## 🚨 주의사항

1. **Internal URL 사용**: External URL이 아닌 **Internal Database URL** 사용
2. **연결 형식**: MySQL은 `mariadb+pymysql://` 로 시작
3. **포트**: Render는 자동으로 포트 설정 (3306 MySQL, 5432 PostgreSQL)
4. **보안**: render.yaml에 직접 비밀번호 넣지 말고 sync: false 유지

## 🔄 배포 후 확인

서버 배포 후:
```bash
# Render Logs에서 확인
# 데이터베이스 연결 성공 여부 확인
```

## 📞 문제 해결

### "Can't connect to MySQL" 오류 시:
1. Internal URL 사용 확인
2. `mariadb+pymysql://` 형식 확인
3. Web Service와 DB가 같은 네트워크에 있는지 확인

### "ModuleNotFoundError: No module named 'pymysql'" 오류 시:
- requirements.txt에 PyMySQL 추가됨
- 다시 배포 필요

