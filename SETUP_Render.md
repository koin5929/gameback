# 🚀 Render 설정 - 간단 가이드

## 1단계: 데이터베이스 추가

1. **Render Dashboard 접속**: https://dashboard.render.com
2. **New +** 버튼 클릭 → **Add PostgreSQL** (무료) 또는 **Add MySQL**
3. 데이터베이스 생성
4. **Internal Database URL** 복사

## 2단계: Web Service 환경변수 설정

**현재 실행 중인 Service 선택** → **Environment 탭**

### 필수 환경변수 추가:

```bash
# 데이터베이스 연결 (예시)
DATABASE_URL=mariadb+pymysql://user:pass@dpg-XXXX.oregon-postgres.render.com:5432/ramjwi_xxxx

# 또는 PostgreSQL 사용 시:
DATABASE_URL=postgresql://user:pass@dpg-XXXX.oregon-postgres.render.com:5432/ramjwi_xxxx

# 플러그인 인증용 (랜덤 문자열)
SHARED_SECRET=abcd1234efgh5678ijkl9012mnop3456

# Discord 봇 (기존 설정 유지)
DISCORD_BOT_TOKEN=your_token_here
ALLOWED_ORIGINS=*
RUN_DISCORD_BOT=true
```

## 3단계: Redeploy

Settings 탭 → **Manual Deploy** 또는 **Clear build cache & deploy**

## 4단계: 확인

Logs 탭에서 확인:
```
✅ Database connected successfully
```

---

## 💡 Tip

**MySQL을 사용하려면?**
- Internal URL을 받은 후
- `mysql://` → `mariadb+pymysql://` 로 변경

**PostgreSQL을 사용하려면?**
- 그대로 사용 (변경 없음)

## 📌 중요 사항

⚠️ **render.yaml 파일은 건드리지 마세요!** 
- Dashboard → Environment에서만 설정
- `sync: false` 유지 (보안을 위해)

