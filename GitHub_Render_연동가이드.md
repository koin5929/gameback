# 🚀 GitHub → Render 연동 가이드

## ✅ 순서

### 1. GitHub에 Push

```bash
# 현재 프로젝트 폴더에서
git add .
git commit -m "Add bingo points system with plugin"
git push origin main  # 또는 master
```

### 2. Render에서 레포지토리 연결

1. **Render Dashboard** 접속: https://dashboard.render.com
2. **New +** 버튼 클릭
3. **Web Service** 선택
4. **Connect a repository** 클릭
5. GitHub 레포지토리 검색 후 선택
6. **Connect** 클릭

### 3. Render 자동 설정

Render가 자동으로 감지:
- ✅ Python 프로젝트 감지
- ✅ `render.yaml` 파일 설정 적용
- ✅ 필요한 환경변수 자동 설정 (sync: false로 설정된 것들)

### 4. 환경변수 추가 확인

**Settings → Environment**에서 확인:

```bash
DATABASE_URL=postgresql://admin:GS47JSwa85XQUCIaNUOM7GbMv5UMcXZ7@dpg-d3vah2uuk2gs73eeb1jg-a/ramjwi
SHARED_SECRET=asas1212@@
DISCORD_BOT_TOKEN=(기존 값)
RUN_DISCORD_BOT=true
GUILD_ID=
```

⚠️ **중요**: `DATABASE_URL`과 `SHARED_SECRET`은 수동으로 추가해야 합니다!

### 5. Deploy!

**Settings** → **Manual Deploy** 버튼 클릭
- 또는 GitHub에 push하면 자동 배포 (autoDeploy: true)

---

## 🔍 배포 확인

### Logs 탭에서 확인:

```
✅ Database connected successfully
✅ Application startup complete
✅ Discord bot logged in as...
```

---

## 📋 배포 후 해야 할 작업

### 1. 빙고 아이템 초기화 (필수)

Render Shell 또는 로컬에서:

```bash
cd backend
export DATABASE_URL="postgresql://admin:GS47JSwa85XQUCIaNUOM7GbMv5UMcXZ7@dpg-d3vah2uuk2gs73eeb1jg-a/ramjwi"
python manage_bingo.py init
```

**예상 출력:**
```
✅ 빙고판 81칸 초기화 완료!
   S+: 1개, S: 3개, A: 6개, B: 18개, C: 27개, D: 26개
```

### 2. 플러그인 빌드 (필수)

```bash
cd plugin
mvn clean package
```

### 3. 플러그인 설정 (필수)

`plugin/src/main/resources/config.yml` 또는 서버의 `plugins/PointsPlugin/config.yml`:

```yaml
api:
  # ✅ 실제 Render URL로 변경 필수!
  url: "https://your-actual-render-url.onrender.com"
  secret: "asas1212@@"
```

### 4. 플러그인 설치 (필수)

- `plugin/target/pointsplugin-1.0.0.jar` 복사
- 마인크래프트 서버 `plugins/` 폴더에 붙여넣기
- 서버 재시작

---

## 🧪 테스트

### 1. 홈페이지 접속

```
https://your-render-url.onrender.com
```

**확인:**
- [ ] 빙고 포인트 섹션 표시
- [ ] 마인크래프트 닉네임 입력 가능
- [ ] 9x9 빙고판 표시

### 2. API 테스트

```bash
# Health check
curl https://your-render-url.onrender.com/api/health

# 빙고 아이템 (초기화 후)
curl https://your-render-url.onrender.com/api/bingo/items
```

### 3. 플러그인 테스트

- 서버 접속
- 30분 플레이 후 콘솔 확인
- 플레이어에게 메시지 확인

---

## ⚠️ 주의사항

### 1. render.yaml 확인

`plan: free`로 되어 있는지 확인

### 2. GitHub 레포지토리 구조

다음 파일들이 포함되어야 합니다:
- ✅ `render.yaml`
- ✅ `backend/requirements.txt`
- ✅ `backend/backend/main.py`
- ✅ `backend/backend/models.py`
- ✅ `web/index.html`
- ✅ `plugin/` (플러그인 소스)

### 3. .gitignore

필요 시 다음 추가:
```
backend/__pycache__/
*.pyc
*.db
*.jar
.DS_Store
```

---

## 🎯 체크리스트

배포 전:
- [ ] GitHub에 커밋 & 푸시
- [ ] 모든 변경사항 포함 확인

Render 설정:
- [ ] 레포지토리 연결
- [ ] DATABASE_URL 환경변수 추가
- [ ] SHARED_SECRET 환경변수 추가
- [ ] Manual Deploy 실행

배포 후:
- [ ] Logs 확인 (정상 작동 확인)
- [ ] 빙고 아이템 초기화
- [ ] 플러그인 빌드 및 설치
- [ ] 테스트

---

## 🚀 다음 단계

1. **GitHub Push** ← 지금 이 단계!
2. Render 연동
3. 환경변수 설정
4. 배포
5. 빙고 아이템 초기화
6. 플러그인 빌드 및 설치
7. 테스트

**준비되셨나요? GitHub에 push 하고 Render에 연결하면 자동으로 배포됩니다!** 🎉

