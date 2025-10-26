# 🚀 Velocity 환경 플러그인 설정 가이드

## ✅ Velocity 환경 호환성

### 현재 상황
- ✅ Velocity 프록시 서버 사용 중
- ✅ MariaDB로 데이터 연동 중
- ✅ 여러 서버 인스턴스 연동

### 호환성
- ✅ **문제 없습니다!** 플러그인은 각 서버에 설치하면 됩니다
- ✅ 같은 DB를 사용하므로 포인트는 전 서버 공유됩니다

---

## 🔧 설정 방법

### 1. 어떤 서버에 플러그인 설치?

**선택지:**
1. **모든 서버에 설치 (권장)** - 어떤 서버에서든 포인트 지급
2. **특정 서버에만 설치** - 해당 서버에서만 포인트 지급

### 2. 플러그인 빌드

```bash
cd plugin
mvn clean package
```

**생성되는 파일:**
```
plugin/target/pointsplugin-1.0.0.jar
```

### 3. 각 서버에 설치

```
lobby-server/plugins/
sub-server-1/plugins/
sub-server-2/plugins/
...
각 폴더에 pointsplugin-1.0.0.jar 복사
```

### 4. Config 설정

각 서버의 `plugins/PointsPlugin/config.yml`:

```yaml
api:
  # Render 홈페이지 API 주소
  url: "https://your-render-app.onrender.com"
  # Backend와 동일 (asas1212@@)
  secret: "asas1212@@"

points:
  interval_minutes: 30
  enable_message: true
```

**중요:** 
- `api.url`은 외부 접근 가능해야 합니다
- Render 주소는 외부에서 접근 가능해야 함

---

## 🎮 작동 방식

### 플레이어 시나리오:

1. 플레이어가 A 서버 접속
   - 플레이어가 30분 플레이
   - A 서버의 플러그인이 포인트 지급
   - DB(MariaDB)에 저장

2. 플레이어가 B 서버로 이동 (Velocity 덕분)
   - 동일한 DB를 참조하므로 포인트 유지됨
   - B 서버의 플러그인도 작동

3. 홈페이지에서 포인트 확인
   - DB에서 조회하여 표시

### 데이터 흐름:

```
플레이어 (A 서버)
    ↓ 30분 플레이
PointsPlugin (A 서버)
    ↓ API 호출
Render Backend
    ↓
MariaDB (공유 DB)
    ↓
홈페이지 (포인트 조회)
```

---

## ⚠️ 주의사항

### 1. API URL 설정

**각 서버의 플러그인 설정:**
- `api.url`은 **외부 접근 가능한 주소**여야 함
- Render는 외부 접근 가능
- 내부 IP (예: 192.168.x.x)는 안 됨

### 2. 중복 포인트 지급 방지

플러그인이 서버 재시작 후에도 포인트 중복 지급을 방지합니다:
- `last_earned` 시간 체크
- 30분 간격 체크

### 3. 보안

**현재 설정:**
- SHARED_SECRET: `asas1212@@`
- 프로덕션에서는 더 복잡한 값 사용 권장
- API는 외부에서 접근 가능하지만 Secret으로 보호됨

---

## 🧪 테스트 방법

### 1. 플러그인 설치 후

서버 콘솔 확인:
```
[PointsPlugin] API URL: https://...
[PointsPlugin] 활성화됨!
```

### 2. 플레이어 접속 후

서버 콘솔에서:
```
[PointsPlugin] PlayerName에게 포인트가 지급되었습니다.
```

플레이어에게:
```
§a[포인트] 30분 플레이 완료! 포인트 1개 획득!
```

### 3. 홈페이지 확인

- 빙고 포인트 섹션
- 마인크래프트 닉네임 입력
- 포인트 표시 확인
- 빙고 칸 선택 테스트

---

## 📊 서버 구조 예시

```
Velocity (프록시)
├── Lobby 서버 (lobby.ramji.o-r.kr:25565)
│   └── plugins/pointsplugin-1.0.0.jar ← 설치
├── Survival 서버 (survival.ramji.o-r.kr:25566)
│   └── plugins/pointsplugin-1.0.0.jar ← 설치
└── Creative 서버 (creative.ramji.o-r.kr:25567)
    └── plugins/pointsplugin-1.0.0.jar ← 설치

모든 서버 → 같은 MariaDB 접속 → 포인트 공유
```

---

## 🔄 만약 문제가 생긴다면

### "Can't connect to API" 오류

**확인사항:**
1. `config.yml`의 `api.url`이 올바른지
2. 인터넷 연결 상태 (서버가 외부 인터넷 접근 가능한지)
3. Render가 배포되었는지

### 포인트가 지급되지 않을 때

**확인사항:**
1. 서버 로그에 플러그인 활성화 메시지 있는지
2. 서버를 재시작했는지
3. 플레이어가 실제로 30분 플레이했는지 (테스트용으로 간격 조정 가능)

---

## ✅ 체크리스트

배포 전:
- [ ] MariaDB에 올바른 DB 접속 가능
- [ ] Render 환경변수 설정 완료

배포 후:
- [ ] Render 배포 성공 (Logs 확인)
- [ ] 빙고 아이템 초기화 완료
- [ ] 플러그인 빌드 완료
- [ ] 플러그인 각 서버에 설치
- [ ] Config 수정 (api.url)
- [ ] 서버 재시작
- [ ] 플러그인 로그 확인

---

**Velocity 환경에서도 완전히 작동합니다!** 🎮

