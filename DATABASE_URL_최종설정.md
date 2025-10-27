# ✅ DATABASE_URL 최종 설정

## 📋 설정할 값

```
postgresql://admin:GS47JSwa85XQUCIaNUOM7GbMv5UMcXZ7@dpg-d3vah2uuk2gs73eeb1jg-a.singapore-postgres.render.com:5432/ramjwi
```

**그대로 복사해서 붙여넣으세요!**

---

## 🔧 Render Dashboard에서 설정

### 1. Web Service 선택
- Render Dashboard → 현재 실행 중인 Web Service 클릭

### 2. Environment 탭 이동

### 3. DATABASE_URL 수정
- 기존 값 삭제
- 새 값 붙여넣기:
  ```
  postgresql://admin:GS47JSwa85XQUCIaNUOM7GbMv5UMcXZ7@dpg-d3vah2uuk2gs73eeb1jg-a.singapore-postgres.render.com:5432/ramjwi
  ```

### 4. 저장
- **Save Changes** 클릭

### 5. 자동 배포 대기
- 저장하면 자동으로 재배포됩니다
- Logs에서 확인

---

## ✅ 배포 확인

**성공 메시지:**
```
✅ Application startup complete
```

**실패 메시지가 보인다면:**
- DATABASE_URL 다시 확인
- 전체 URL 복사했는지 확인

---

## 📊 체크리스트

- [ ] External Database URL 복사
- [ ] DATABASE_URL 환경변수 수정
- [ ] 저장
- [ ] 배포 대기 (1-2분)
- [ ] Logs에서 "Application startup complete" 확인
- [ ] /api/health 테스트

---

**그대로 넣으시면 됩니다!** ✅

