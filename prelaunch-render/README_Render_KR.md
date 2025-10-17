# LOSS ONLINE · 사전예약(Discord 버튼 + FastAPI) — Render 배포 가이드

## 구성
- Web(FastAPI): `/api/validate-name`, `/api/register`, `/api/list`
- Worker(Discord Bot): 버튼 + 모달
- Web page: `web/index.html`

## Render 배포
1) 이 폴더를 깃 저장소로 올립니다.
2) Render → New → Blueprint → 저장소 선택 → `render.yaml` 인식.
3) Web 서비스 환경변수
   - SHARED_SECRET: 랜덤 문자열 (봇과 동일)
   - DATABASE_URL: 기본 sqlite 사용(그대로), 필요한 경우 외부 DB
4) Worker 서비스 환경변수
   - DISCORD_BOT_TOKEN: 디스코드 봇 토큰
   - SHARED_SECRET: Web과 동일
   - API_BASE: Web 배포 URL (예: https://prelaunch-fastapi.onrender.com)
   - GUILD_ID: 선택
5) 디스코드에서 `/사전예약패널` 실행 → 패널 게시
