#!/usr/bin/env python3
"""
Bitcoin News Monitor - 비트코인 관련 뉴스 텔레그램 알림 시스템
"""

import os
import json
import logging
import time
import schedule
from datetime import datetime
from news_monitor import NewsMonitor
from telegram_bot import TelegramBot
from utils import setup_logging

def load_config():
    """설정 파일 로드"""
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # 환경변수에서 텔레그램 설정 가져오기
        config['telegram']['bot_token'] = os.getenv('TELEGRAM_BOT_TOKEN', config['telegram']['bot_token'])
        config['telegram']['chat_id'] = os.getenv('TELEGRAM_CHAT_ID', config['telegram']['chat_id'])
        
        return config
    except FileNotFoundError:
        logging.error("config.json 파일을 찾을 수 없습니다.")
        return None
    except json.JSONDecodeError:
        logging.error("config.json 파일 형식이 올바르지 않습니다.")
        return None

def validate_config(config):
    """설정 유효성 검사"""
    if not config['telegram']['bot_token']:
        logging.error("텔레그램 봇 토큰이 설정되지 않았습니다.")
        return False
    
    if not config['telegram']['chat_id']:
        logging.error("텔레그램 채팅 ID가 설정되지 않았습니다.")
        return False
    
    return True

def monitor_news():
    """뉴스 모니터링 메인 함수"""
    try:
        logging.info("뉴스 모니터링 시작...")
        
        # 새로운 뉴스 기사 수집
        new_articles = news_monitor.get_new_articles()
        
        if new_articles:
            logging.info(f"새로운 기사 {len(new_articles)}개 발견")
            
            # 텔레그램으로 알림 전송
            telegram_bot.send_news_notification(new_articles)
            
            # 처리된 기사 저장
            news_monitor.mark_articles_as_processed(new_articles)
        else:
            logging.info("새로운 기사가 없습니다.")
            
    except Exception as e:
        logging.error(f"뉴스 모니터링 중 오류 발생: {e}")

def main():
    """메인 실행 함수"""
    global news_monitor, telegram_bot
    
    print("🚀 Bitcoin News Monitor 시작")
    
    # 설정 로드
    config = load_config()
    if not config:
        print("❌ 설정 파일을 로드할 수 없습니다.")
        return
    
    # 로깅 설정
    setup_logging(config['logging'])
    logging.info("Bitcoin News Monitor 시작됨")
    
    # 설정 유효성 검사
    if not validate_config(config):
        print("❌ 설정이 올바르지 않습니다.")
        logging.error("설정 유효성 검사 실패")
        return
    
    # 모니터링 및 텔레그램 봇 초기화
    news_monitor = NewsMonitor(config)
    telegram_bot = TelegramBot(config)
    
    # 텔레그램 봇 연결 테스트
    if not telegram_bot.test_connection():
        print("❌ 텔레그램 봇 연결에 실패했습니다.")
        logging.error("텔레그램 봇 연결 실패")
        return
    
    print("✅ 텔레그램 봇 연결 성공")
    
    # 초기 시작 메시지 전송
    telegram_bot.send_message("🤖 Bitcoin News Monitor가 시작되었습니다!\n\n📰 비트코인 관련 뉴스를 모니터링하고 있습니다...")
    
    # 스케줄 설정
    interval = config['monitoring']['interval_minutes']
    schedule.every(interval).minutes.do(monitor_news)
    
    print(f"⏰ {interval}분마다 뉴스를 확인합니다.")
    logging.info(f"모니터링 간격: {interval}분")
    
    # 첫 실행
    monitor_news()
    
    # 무한 루프로 스케줄 실행
    try:
        while True:
            schedule.run_pending()
            time.sleep(30)  # 30초마다 스케줄 체크
    except KeyboardInterrupt:
        print("\n⛔ Bitcoin News Monitor 종료")
        logging.info("사용자에 의해 프로그램 종료")
        telegram_bot.send_message("⛔ Bitcoin News Monitor가 종료되었습니다.")

if __name__ == "__main__":
    main()
