# DATABASE_URL 설정 예시

## 사용자가 받은 URL
```
postgresql://admin:GS47JSwa85XQUCIaNUOM7GbMv5UMcXZ7@dpg-d3vah2uuk2gs73eeb1jg-a/ramjwi
```

## 완전한 형식 (추정)
```
postgresql://admin:GS47JSwa85XQUCIaNUOM7GbMv5UMcXZ7@dpg-d3vah2uuk2gs73eeb1jg-a.oregon-postgres.render.com:5432/ramjwi
```

## Render Dashboard에서 설정

### 1. 전체 URL 찾기
- PostgreSQL 데이터베이스 클릭
- **Connections** 탭 이동
- **Internal Connection String** 확인

전체 URL은 다음과 비슷하게 생겼을 것입니다:
```
postgresql://admin:GS47JSwa85XQUCIaNUOM7GbMv5UMcXZ7@dpg-d3vah2uuk2gs73eeb1jg-a.oregon-postgres.render.com:5432/ramjwi
```

### 2. Web Service → Environment에서 설정

**Key**: `DATABASE_URL`
**Value**: (위에서 복사한 전체 Internal URL)

```
postgresql://admin:GS47JSwa85XQUCIaNUOM7GbMv5UMcXZ7@dpg-d3vah2uuk2gs73eeb1jg-a.oregon-postgres.render.com:5432/ramjwi
```

### 3. 확인사항

✅ URL 시작: `postgresql://`
✅ 비밀번호 포함: `GS47JSwa85XQUCIaNUOM7GbMv5UMcXZ7`
✅ 호스트명: `.oregon-postgres.render.com` 포함
✅ 포트: `:5432` 포함
✅ DB 이름: `/ramjwi`

## 배포 및 확인

설정 후:
1. **Manual Deploy** 실행
2. **Logs** 탭에서 확인
3. 정상 연결 시: `✅ Database connected`

## 오류 발생 시

**"Can't connect to database" 오류:**
- URL 전체가 복사되었는지 확인
- 포트 번호 (5432) 포함 여부 확인
- 호스트명 끝에 `.render.com`이 있는지 확인

