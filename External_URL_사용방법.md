# ✅ External Database URL 사용

## 📝 사용해야 하는 URL

### Internal URL (현재 사용 중) ❌
```
postgresql://admin:password@dpg-d3vah2uuk2gs73eeb1jg-a/ramjwi
```
문제: 도메인이 없어서 DNS 해석 실패

### External URL (권장) ✅
```
postgresql://admin:password@dpg-d3vah2uuk2gs73eeb1jg-a.singapore-postgres.render.com:5432/ramjwi
```
포함: 도메인, 포트

---

## 🔧 설정 방법

### 1. External Database URL 복사
이미지에서 **External Database URL** 전체 복사

### 2. Render Dashboard → Environment

**Key**: `DATABASE_URL`

**Value**: External Database URL 붙여넣기
```
postgresql://admin:GS47JSwa85XQUCIaNUOM7GbMv5UMcXZ7@dpg-d3vah2uuk2gs73eeb1jg-a.singapore-postgres.render.com:5432/ramjwi
```

⚠️ **중요**: 
- 전체 URL 복사 (truncate 안 되게)
- 끝에 슬래시 없음
- `.singapore-postgres.render.com` 포함
- `:5432` 포트 포함

---

## 📊 URL 비교

| 항목 | Internal URL | External URL |
|------|-------------|--------------|
| 호스트 | `dpg-d3vah2uuk2gs73eeb1jg-a` | `dpg-d3vah2uuk2gs73eeb1jg-a.singapore-postgres.render.com` |
| 포트 | 없음 | `:5432` |
| 작동 | ❌ DNS 실패 | ✅ 작동 |
| 사용 | 같은 네트워크 | 외부 접근 |

---

## ✅ 다음 단계

1. External Database URL 복사
2. DATABASE_URL 환경변수 수정
3. 저장
4. 자동 배포 대기
5. Logs 확인

**배포 후 `Application startup complete` 메시지가 보이면 성공!** 🎉

