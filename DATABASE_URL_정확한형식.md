# 🔍 DATABASE_URL 정확한 형식

## 현재 설정
```
postgresql://admin:GS47JSwa85XQUCIaNUOM7GbMv5UMcXZ7@dpg-d3vah2uuk2gs73eeb1jg-a/ramjwi
```

## 문제
❌ 포트 번호 없음 (`:5432` 빠짐)
❌ 도메인 없음 (`.render.com` 빠짐)

## 올바른 형식
```
postgresql://admin:GS47JSwa85XQUCIaNUOM7GbMv5UMcXZ7@dpg-d3vah2uuk2gs73eeb1jg-a.singapore-postgres.render.com:5432/ramjwi
                                                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^  ^^^^^
                                                    도메인 추가                    포트 추가
```

---

## 🔍 Render Dashboard에서 확인

### 1. PostgreSQL 데이터베이스 클릭

### 2. Connections 탭에서 확인:

**Internal Database URL** 전체를 복사하세요.

전체 URL은 다음과 같이 생겼을 것입니다:
```
postgresql://admin:GS47JSwa85XQUCIaNUOM7GbMv5UMcXZ7@dpg-d3vah2uuk2gs73eeb1jg-a.singapore-postgres.render.com:5432/ramjwi
```

또는 다른 지역일 수 있습니다:
- `.oregon-postgres.render.com`
- `.singapore-postgres.render.com`
- `.frankfurt-postgres.render.com`

---

## ✅ 수정 방법

Render Dashboard → Web Service → Environment:

**DATABASE_URL** 수정:

```
postgresql://admin:GS47JSwa85XQUCIaNUOM7GbMv5UMcXZ7@dpg-d3vah2uuk2gs73eeb1jg-a.singapore-postgres.render.com:5432/ramjwi
```

**Connections 탭의 전체 URL을 그대로 복사**해 붙여넣으세요!

---

## 📊 비교

| 항목 | 현재 | 올바른 형식 |
|------|------|------------|
| 호스트 | `dpg-d3vah2uuk2gs73eeb1jg-a` | `dpg-d3vah2uuk2gs73eeb1jg-a.singapore-postgres.render.com` |
| 포트 | 없음 | `:5432` |
| 전체 | 호스트만 있음 | 호스트 + 도메인 + 포트 |

---

**Connections 탭에서 전체 Internal Database URL을 복사해서 넣으시면 됩니다!** 🔧

