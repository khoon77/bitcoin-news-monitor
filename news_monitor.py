"""
뉴스 모니터링 모듈 - RSS 피드와 웹 스크래핑을 통한 뉴스 수집
"""

import json
import logging
import hashlib
import requests
import feedparser
import trafilatura
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time

class NewsMonitor:
    def __init__(self, config):
        self.config = config
        self.processed_articles_file = config['storage']['processed_articles_file']
        self.keywords = [keyword.lower() for keyword in config['keywords']]
        self.max_stored_articles = config['storage']['max_stored_articles']
        self.processed_articles = self.load_processed_articles()
        
    def load_processed_articles(self):
        """처리된 기사 목록 로드"""
        try:
            with open(self.processed_articles_file, 'r', encoding='utf-8') as f:
                return set(json.load(f))
        except (FileNotFoundError, json.JSONDecodeError):
            logging.info("처리된 기사 파일이 없거나 손상됨. 새로 생성합니다.")
            return set()
    
    def save_processed_articles(self):
        """처리된 기사 목록 저장"""
        try:
            # 최대 저장 개수 제한
            if len(self.processed_articles) > self.max_stored_articles:
                # 오래된 기사들 제거 (단순히 앞쪽 절반 제거)
                articles_list = list(self.processed_articles)
                keep_count = self.max_stored_articles // 2
                self.processed_articles = set(articles_list[-keep_count:])
            
            with open(self.processed_articles_file, 'w', encoding='utf-8') as f:
                json.dump(list(self.processed_articles), f, ensure_ascii=False, indent=2)
        except Exception as e:
            logging.error(f"처리된 기사 저장 실패: {e}")
    
    def generate_article_hash(self, title, url):
        """기사 고유 해시 생성"""
        content = f"{title}{url}".encode('utf-8')
        return hashlib.md5(content).hexdigest()
    
    def is_relevant_article(self, title, content=""):
        """비트코인 관련 기사인지 확인"""
        text = f"{title} {content}".lower()
        return any(keyword in text for keyword in self.keywords)
    
    def get_rss_articles(self):
        """RSS 피드에서 기사 수집"""
        articles = []
        
        for rss_url in self.config['news_sources']['rss_feeds']:
            try:
                logging.info(f"RSS 피드 확인: {rss_url}")
                
                # RSS 피드 파싱
                feed = feedparser.parse(rss_url)
                
                if feed.bozo:
                    logging.warning(f"RSS 피드 파싱 오류: {rss_url}")
                    continue
                
                for entry in feed.entries[:10]:  # 최근 10개 기사만 확인
                    title = entry.get('title', '')
                    link = entry.get('link', '')
                    summary = entry.get('summary', '')
                    published = entry.get('published', '')
                    
                    # 관련성 확인
                    if not self.is_relevant_article(title, summary):
                        continue
                    
                    # 중복 확인
                    article_hash = self.generate_article_hash(title, link)
                    if article_hash in self.processed_articles:
                        continue
                    
                    articles.append({
                        'title': title,
                        'url': link,
                        'summary': summary,
                        'published': published,
                        'source': urlparse(rss_url).netloc,
                        'hash': article_hash
                    })
                
                # 요청 간 딜레이
                time.sleep(1)
                
            except Exception as e:
                logging.error(f"RSS 피드 처리 오류 ({rss_url}): {e}")
        
        return articles
    
    def get_investing_articles(self):
        """인베스팅닷컴 한국어 암호화폐 뉴스 수집"""
        articles = []
        url = "https://kr.investing.com/news/cryptocurrency-news"
        
        try:
            logging.info(f"인베스팅닷컴 뉴스 확인: {url}")
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, timeout=15, headers=headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 인베스팅닷컴 뉴스 기사 선택자 (업데이트된 선택자)
            news_items = soup.find_all(['article', 'div'], class_=['largeTitle', 'mediumTitle1', 'js-article-item'])
            
            if not news_items:
                # 대안 선택자들 시도
                news_items = soup.select('a[data-test="article-title-link"], .articleItem a, .textDiv a')
            
            for item in news_items[:8]:  # 최대 8개
                try:
                    if item.name == 'a':
                        link_elem = item
                        title = item.get_text(strip=True)
                    else:
                        link_elem = item.find('a')
                        title = link_elem.get_text(strip=True) if link_elem else ''
                    
                    if not link_elem or not title or len(title) < 10:
                        continue
                    
                    href = link_elem.get('href', '')
                    if href.startswith('/'):
                        article_url = f"https://kr.investing.com{href}"
                    elif not href.startswith('http'):
                        continue
                    else:
                        article_url = href
                    
                    # 암호화폐 관련 기사인지 확인
                    if not self.is_relevant_article(title):
                        continue
                    
                    # 중복 확인
                    article_hash = self.generate_article_hash(title, article_url)
                    if article_hash in self.processed_articles:
                        continue
                    
                    articles.append({
                        'title': title,
                        'url': article_url,
                        'summary': '',
                        'published': datetime.now().isoformat(),
                        'source': 'kr.investing.com',
                        'hash': article_hash
                    })
                    
                except Exception as e:
                    logging.error(f"인베스팅닷컴 기사 처리 오류: {e}")
                    continue
                    
            logging.info(f"인베스팅닷컴에서 {len(articles)}개 기사 수집")
            
        except Exception as e:
            logging.error(f"인베스팅닷컴 스크래핑 오류: {e}")
        
        return articles
    
    def get_tradingview_articles(self):
        """트레이딩뷰 한국어 크립토 뉴스 수집"""
        articles = []
        url = "https://kr.tradingview.com/news/?category=crypto"
        
        try:
            logging.info(f"트레이딩뷰 뉴스 확인: {url}")
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, timeout=15, headers=headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 트레이딩뷰 뉴스 기사 선택자
            news_items = soup.find_all('a', class_=['apply-common-tooltip', 'news-item'])
            
            if not news_items:
                # 대안 선택자 시도
                news_items = soup.select('a[href*="/news/"], .news-feed a, [data-role="news-item"] a')
            
            for item in news_items[:8]:  # 최대 8개
                try:
                    title_elem = item.find(['h3', 'h2', 'span'], class_=['title', 'headline'])
                    if not title_elem:
                        title_elem = item
                    
                    title = title_elem.get_text(strip=True)
                    
                    if not title or len(title) < 10:
                        continue
                    
                    href = item.get('href', '')
                    if href.startswith('/'):
                        article_url = f"https://kr.tradingview.com{href}"
                    elif not href.startswith('http'):
                        continue
                    else:
                        article_url = href
                    
                    # 암호화폐 관련 기사인지 확인
                    if not self.is_relevant_article(title):
                        continue
                    
                    # 중복 확인
                    article_hash = self.generate_article_hash(title, article_url)
                    if article_hash in self.processed_articles:
                        continue
                    
                    articles.append({
                        'title': title,
                        'url': article_url,
                        'summary': '',
                        'published': datetime.now().isoformat(),
                        'source': 'kr.tradingview.com',
                        'hash': article_hash
                    })
                    
                except Exception as e:
                    logging.error(f"트레이딩뷰 기사 처리 오류: {e}")
                    continue
                    
            logging.info(f"트레이딩뷰에서 {len(articles)}개 기사 수집")
            
        except Exception as e:
            logging.error(f"트레이딩뷰 스크래핑 오류: {e}")
        
        return articles

    def get_scraped_articles(self):
        """한국어 사이트들에서 기사 수집"""
        all_articles = []
        
        # 인베스팅닷컴 뉴스 수집
        investing_articles = self.get_investing_articles()
        all_articles.extend(investing_articles)
        time.sleep(2)
        
        # 트레이딩뷰 뉴스 수집
        tradingview_articles = self.get_tradingview_articles()
        all_articles.extend(tradingview_articles)
        time.sleep(2)
        
        return all_articles
    
    def get_new_articles(self):
        """새로운 기사 수집 (한국어 사이트 전용)"""
        all_articles = []
        
        # 한국어 사이트에서 기사 수집
        scraped_articles = self.get_scraped_articles()
        all_articles.extend(scraped_articles)
        logging.info(f"한국어 사이트에서 총 {len(scraped_articles)}개 새 기사 발견")
        
        # 중복 제거 (URL 기준)
        unique_articles = {}
        for article in all_articles:
            url = article['url']
            if url not in unique_articles:
                unique_articles[url] = article
        
        new_articles = list(unique_articles.values())
        
        # 최대 개수 제한
        max_articles = self.config['monitoring']['max_articles_per_notification']
        if len(new_articles) > max_articles:
            new_articles = new_articles[:max_articles]
            logging.info(f"기사 개수를 {max_articles}개로 제한")
        
        return new_articles
    
    def mark_articles_as_processed(self, articles):
        """기사들을 처리됨으로 표시"""
        for article in articles:
            self.processed_articles.add(article['hash'])
        
        self.save_processed_articles()
        logging.info(f"{len(articles)}개 기사 처리 완료")
