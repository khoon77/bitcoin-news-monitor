# Bitcoin News Monitor

GitHub Actions를 이용한 무료 24시간 비트코인 뉴스 모니터링 시스템

## 기능
- 트레이딩뷰 한국어 크립토 뉴스 실시간 모니터링
- 텔레그램 자동 알림
- GitHub Actions로 24시간 무료 실행
- 매 5분마다 자동 확인

## 설정 방법

### 1. GitHub 저장소 생성 후 파일 업로드
### 2. GitHub Secrets 설정
- `TELEGRAM_BOT_TOKEN`: 텔레그램 봇 토큰
- `TELEGRAM_CHAT_ID`: 채팅 ID

### 3. GitHub Actions 실행
매 5분마다 자동 실행되어 새 뉴스를 텔레그램으로 알림

## 파일 구조
```
├── config.json              # 설정 파일
├── main.py                  # 메인 실행 파일
├── news_monitor.py          # 뉴스 수집 모듈
├── telegram_bot.py          # 텔레그램 알림 모듈
├── utils.py                 # 유틸리티 함수
├── github_monitor.py        # GitHub Actions 실행 파일
└── .github/workflows/
    └── bitcoin-news-monitor.yml  # GitHub Actions 워크플로우
```