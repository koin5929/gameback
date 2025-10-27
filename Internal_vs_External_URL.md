# 🔍 Internal vs External URL 차이

## 📊 두 URL 비교

### Internal Database URL (현재 사용 중) ❌
```
postgresql://admin:GS47JSwa85XQUCIaNUOM7GbMv5UMcXZ7@dpg-d3vah2uuk2gs73eeb1jg-a/ramjwi
```
특징:
- 도메인 없음
- 포트 없음
- 같은 네트워크에서만 작동
- Render 내부에서만 접근 가능

**문제**: DNS 해석 실패!

### External Database URL (사용해야 함) ✅
```
postgresql://admin:GS47JSwa85XQUCIaNUOM7GbMv5UMcXZ7@dpg-d3vah2uuk2gs73eeb1jg-a.singapore-postgres.render.com:5432/ramjwi
```
특징:
- 도메인 있음 (`.singapore-postgres.render.com`)
- 포트 있음 (`:5432`)
- 외부 접근 가능
- Render Web Service에서 접근 가능

---

## ✅ 해결 방법

### 1. External Database URL 확인

Render Dashboard → PostgreSQL 데이터베이스 → **Connections** 탭:

**External Database URL** 전체 복사

### 2. DATABASE_URL 수정

Render Dashboard → Web Service → Environment:

**현재 값** (Internal URL):
```
postgresql://admin:GS47JSwa85XQUCIaNUOM7GbMv5UMcXZ7@dpg-d3vah2uuk2gs73eeb1jg-a/ramjwi
```

**새 값** (External URL로 변경):
```
postgresql://admin:GS47JSwa85XQUCIaNUOM7GbMv5UMcXZ7@dpg-d3vah2uuk2gs73eeb1jg-a.singapore-postgres.render.com:5432/ramjwi
```

---

## 📝 External URL 복사 방법

Connections 탭에서 **External Database URL** 보라색 버튼 클릭

전체 URL이 복사됩니다 (끝이 잘리지 않게!)

---

**External Database URL을 사용하시면 됩니다!** 🔧

