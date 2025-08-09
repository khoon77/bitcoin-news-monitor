# GitHub Actions로 무료 24시간 뉴스 모니터링 가이드

## GitHub Actions 장점

✅ **완전 무료** (월 2000분 제한, 하루 약 66분 사용 가능)  
✅ **컴퓨터 꺼도 작동** (GitHub 서버에서 실행)  
✅ **설정 한 번으로 자동 실행**  
✅ **안정적인 클라우드 환경**  

## 제약사항

⚠️ **최소 실행 간격**: 5분 (1분 간격 불가능)  
⚠️ **월 사용 한계**: 2000분 (하루 평균 66분)  
⚠️ **최대 실행 시간**: 6시간 (우리는 1분 내 완료)  

## 설정 방법

### 1단계: GitHub 저장소 생성
1. GitHub에서 새 저장소 생성 (예: `bitcoin-news-monitor`)
2. 이 프로젝트의 모든 파일을 업로드

### 2단계: GitHub Secrets 설정
1. 저장소 → **Settings** → **Secrets and variables** → **Actions**
2. **New repository secret** 클릭
3. 다음 두 개의 시크릿 추가:
   - **Name**: `TELEGRAM_BOT_TOKEN`  
     **Value**: `당신의_텔레그램_봇_토큰`
   - **Name**: `TELEGRAM_CHAT_ID`  
     **Value**: `당신의_채팅_ID`

### 3단계: GitHub Actions 활성화
1. 저장소 → **Actions** 탭 클릭
2. **Bitcoin News Monitor** 워크플로우 확인
3. **Enable workflow** 클릭 (필요시)

### 4단계: 수동 테스트 실행
1. **Actions** 탭 → **Bitcoin News Monitor** 클릭
2. **Run workflow** → **Run workflow** 클릭
3. 실행 결과 확인

## 실행 스케줄

```yaml
schedule:
  - cron: '*/5 * * * *'  # 매 5분마다 실행
```

**매일 실행 횟수**: 288회 (24시간 × 12회/시간)  
**월간 사용 시간**: 약 288분 (2000분 한도 내)  

## 비용 계산

| 항목 | GitHub Actions | Replit Always On |
|------|---------------|------------------|
| **월 비용** | 무료 | $7 |
| **실행 간격** | 5분 | 1분 |
| **사용 한도** | 2000분 | 무제한 |
| **설정 복잡도** | 중간 | 쉬움 |

## 모니터링 및 로그 확인

### GitHub Actions 로그 보기
1. **Actions** 탭 → 실행 기록 클릭
2. **monitor-news** 작업 클릭
3. 각 단계별 로그 확인

### 일반적인 로그 메시지
```
🚀 GitHub Actions Bitcoin News Monitor 시작
✅ 텔레그램 봇 연결 성공
📰 새로운 뉴스 확인 중...
🔥 새로운 기사 1개 발견!
✅ 텔레그램 알림 전송 완료
🎉 GitHub Actions 실행 완료
```

## 문제 해결

### 자주 발생하는 문제

**1. 텔레그램 설정 오류**
```
❌ 텔레그램 설정이 GitHub Secrets에 없습니다.
```
**해결**: GitHub Secrets에 `TELEGRAM_BOT_TOKEN`과 `TELEGRAM_CHAT_ID` 추가

**2. 사이트 접근 차단**
```
ERROR - 인베스팅닷컴 스크래핑 오류: 403 Client Error
```
**해결**: 정상적인 현상, 트레이딩뷰에서만 뉴스 수집

**3. 월 사용량 초과**
```
You have exceeded your usage limit for GitHub Actions
```
**해결**: 다음 달까지 대기하거나 유료 플랜 고려

## 실제 사용 예시

### GitHub Actions 실행 시 텔레그램 알림
```
🚨 새로운 비트코인 뉴스 1개 발견!

1. 📰 비트코인, 6만 달러 돌파 후 조정
   🌐 kr.tradingview.com
   🔗 기사 읽기

🤖 GitHub Actions에서 2025-08-09 10:43에 1개 뉴스 알림을 전송했습니다.
```

## 추천 사용 시나리오

**GitHub Actions 추천**: 
- 비용을 절약하고 싶은 경우
- 5분 간격으로도 충분한 경우
- 기술적 설정을 즐기는 경우

**Replit Always On 추천**:
- 1분 간격이 필요한 경우  
- 설정의 편리함을 원하는 경우
- 월 $7 비용이 부담되지 않는 경우

## 결론

GitHub Actions는 **무료**로 비트코인 뉴스 모니터링을 24시간 자동 실행할 수 있는 훌륭한 선택입니다. 5분 간격 제한이 있지만 대부분의 사용 사례에는 충분합니다.