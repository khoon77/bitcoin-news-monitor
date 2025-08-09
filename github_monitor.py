#!/usr/bin/env python3
"""
GitHub Actions용 일회성 뉴스 모니터링 스크립트
"""

import os
import sys
import json
import logging
from datetime import datetime

# 로깅 설정
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main():
    """GitHub Actions에서 실행되는 메인 함수"""
    print("🚀 GitHub Actions Bitcoin News Monitor 시작")
    
    try:
        # 현재 디렉토리를 Python 경로에 추가
        sys.path.append('.')
        
        from news_monitor import NewsMonitor
        from telegram_bot import TelegramBot
        
        # 설정 파일 로드
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # 환경변수에서 텔레그램 설정 가져오기
        bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        chat_id = os.getenv('TELEGRAM_CHAT_ID')
        
        if not bot_token or not chat_id:
            print("❌ 텔레그램 설정이 GitHub Secrets에 없습니다.")
            print("GitHub 저장소 → Settings → Secrets and variables → Actions에서 설정하세요:")
            print("- TELEGRAM_BOT_TOKEN")
            print("- TELEGRAM_CHAT_ID")
            sys.exit(1)
        
        config['telegram']['bot_token'] = bot_token
        config['telegram']['chat_id'] = chat_id
        
        # 이전 처리된 기사 파일이 있으면 로드
        processed_file = 'processed_articles.json'
        if os.path.exists(processed_file):
            print("📂 이전 처리된 기사 목록을 로드했습니다.")
        
        # 모니터링 객체 생성
        news_monitor = NewsMonitor(config)
        telegram_bot = TelegramBot(config)
        
        # 텔레그램 봇 연결 테스트
        if not telegram_bot.test_connection():
            print("❌ 텔레그램 봇 연결 실패")
            sys.exit(1)
        
        print("✅ 텔레그램 봇 연결 성공")
        
        # 뉴스 모니터링 실행
        print("📰 새로운 뉴스 확인 중...")
        new_articles = news_monitor.get_new_articles()
        
        if new_articles:
            print(f"🔥 새로운 기사 {len(new_articles)}개 발견!")
            
            # 텔레그램 알림 전송
            success = telegram_bot.send_news_notification(new_articles)
            
            if success:
                # 처리된 기사로 마킹
                news_monitor.mark_articles_as_processed(new_articles)
                print("✅ 텔레그램 알림 전송 완료")
                
                # GitHub Actions 실행 알림
                github_msg = f"🤖 GitHub Actions에서 {datetime.now().strftime('%Y-%m-%d %H:%M')}에 {len(new_articles)}개 뉴스 알림을 전송했습니다."
                telegram_bot.send_message(github_msg)
            else:
                print("❌ 텔레그램 알림 전송 실패")
                sys.exit(1)
        else:
            print("📭 새로운 기사가 없습니다.")
        
        print("🎉 GitHub Actions 실행 완료")
        
    except Exception as e:
        error_msg = f"GitHub Actions 실행 중 오류 발생: {e}"
        print(f"❌ {error_msg}")
        
        # 오류를 텔레그램으로도 알림
        try:
            from telegram_bot import TelegramBot
            bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
            chat_id = os.getenv('TELEGRAM_CHAT_ID')
            if bot_token and chat_id:
                config = {'telegram': {'bot_token': bot_token, 'chat_id': chat_id}}
                bot = TelegramBot(config)
                bot.send_message(f"🚨 GitHub Actions 오류\n\n{error_msg}")
        except:
            pass
        
        sys.exit(1)

if __name__ == "__main__":
    main()