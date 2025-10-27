# 📍 플러그인 API URL 설정 가이드

## ✅ 둘 다 가능합니다!

### Option 1: Render URL (https://prelaunch-all-in-one.onrender.com)
```
✅ 사용 가능
✅ 무료
✅ SSL 자동 설정
✅ 바로 사용 가능
```

### Option 2: 커스텀 도메인 (예: https://ramji.o-r.kr)
```
✅ 사용 가능
✅ 브랜드화
✅ 짧고 기억하기 쉬움
✅ 사용자에게 더 전문적으로 보임
```

---

## ⚠️ 중요사항

### 1. HTTPS 필수
```yaml
# ✅ 올바른 예
url: "https://ramji.o-r.kr"
url: "https://prelaunch-all-in-one.onrender.com"

# ❌ 잘못된 예 (HTTP)
url: "http://ramji.o-r.kr"  # 플러그인이 연결 안 될 수 있음
```

### 2. 슬래시(/) 제거
```yaml
# ✅ 올바른 예
url: "https://ramji.o-r.kr"

# ❌ 잘못된 예
url: "https://ramji.o-r.kr/"  # 끝에 / 없어야 함
```

### 3. 포트 번호 불필요
Render는 자동으로 443 포트로 HTTPS를 제공하므로 포트 번호 지정 불필요

```yaml
# ✅ 올바른 예
url: "https://ramji.o-r.kr"

# ❌ 불필요한 포트 지정
url: "https://ramji.o-r.kr:443"
```

---

## 🎯 권장 설정

### 커스텀 도메인 사용 (추천) ⭐
```yaml
api:
  url: "https://ramji.o-r.kr"  # 원하시는 도메인
  secret: "asas1212@@"
```

**장점:**
- 더 짧고 기억하기 쉬움
- 브랜드 통일성
- URL 변경에도 유연함
- 나중에 서버 주소 변경 시 유지보수 용이

---

## 🔄 도메인 설정 확인

커스텀 도메인을 Render에 연결하셨다면:

### 1. Render Dashboard 확인
- Settings → Custom Domain
- 도메인이 연결되어 있는지 확인
- SSL 인증서 상태: Active ✅

### 2. 테스트
```bash
# Health check
curl https://ramji.o-r.kr/api/health

# 빙고 아이템
curl https://ramji.o-r.kr/api/bingo/items
```

둘 다 정상 작동하면 설정 성공!

---

## 📝 최종 설정

### plugin/src/main/resources/config.yml:

```yaml
api:
  # 커스텀 도메인 사용 (권장)
  url: "https://ramji.o-r.kr"
  # 또는 Render URL 사용
  # url: "https://prelaunch-all-in-one.onrender.com"
  
  secret: "asas1212@@"

points:
  interval_minutes: 30
  enable_message: true
```

---

## ⚡ 빠른 선택 가이드

**커스텀 도메인이 SSL 인증서가 활성화되어 있다면:**
→ ✅ 커스텀 도메인 권장

**커스텀 도메인 설정이 복잡하다면:**
→ ✅ Render URL 사용 (https://prelaunch-all-in-one.onrender.com)

**어느 것을 써도 작동합니다!** 🎮

---

## 🔍 확인 방법

플러그인 설치 후 서버 로그에서 확인:

```
[PointsPlugin] API URL: https://ramji.o-r.kr
[PointsPlugin] 활성화됨!
```

이 메시지가 나오면 정상 연결된 것입니다!

