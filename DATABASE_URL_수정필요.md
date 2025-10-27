# 🔧 DATABASE_URL 수정 필요

## 🐛 문제
```
could not translate host name "dpg-d3vah2uuk2gs73eeb1jg-a" to address: Name or service not known
```

**호스트명만 있고 도메인이 없습니다!**

---

## ✅ 올바른 DATABASE_URL 형식

### 현재 (잘못됨):
```
postgresql://admin:GS47JSwa85XQUCIaNUOM7GbMv5UMcXZ7@dpg-d3vah2uuk2gs73eeb1jg-a/ramjwi
```

### 올바른 형식:
```
postgresql://admin:GS47JSwa85XQUCIaNUOM7GbMv5UMcXZ7@dpg-d3vah2uuk2gs73eeb1jg-a.oregon-postgres.render.com:5432/ramjwi
```

또는
```
postgresql://admin:GS47JSwa85XQUCIaNUOM7GbMv5UMcXZ7@dpg-d3vah2uuk2gs73eeb1jg-a.singapore-postgres.render.com:5432/ramjwi
```

---

## 🔍 해결 방법

### 1. Render Dashboard에서 전체 Internal URL 확인

1. **Render Dashboard** 접속
2. **PostgreSQL 데이터베이스** 클릭
3. **Connections** 탭
4. **Internal Database URL** 복사
5. 전체 URL 확인 (`.render.com` 포함되어야 함)

---

### 2. DATABASE_URL 수정

**Render Dashboard** → **Web Service** → **Environment**:

**Key**: `DATABASE_URL`

**Value**: 전체 URL 붙여넣기 (예시)
```
postgresql://admin:GS47JSwa85XQUCIaNUOM7GbMv5UMcXZ7@dpg-d3vah2uuk2gs73eeb1jg-a.oregon-postgres.render.com:5432/ramjwi
```

⚠️ **중요**: 
- 끝에 슬래시(/) 없음
- `.render.com` 포함 필수!
- 포트 `:5432` 포함

---

### 3. 배포

수정 후 **저장**하면 자동 재배포됩니다.

---

## 📋 체크리스트

- [ ] PostgreSQL 데이터베이스 클릭
- [ ] Connections 탭 확인
- [ ] Internal Database URL 복사
- [ ] 전체 URL 확인 (.render.com 포함)
- [ ] DATABASE_URL 환경변수 수정
- [ ] 저장
- [ ] 배포 대기
- [ ] Logs 확인

---

**DATABASE_URL만 수정하면 해결됩니다!** 🔧

