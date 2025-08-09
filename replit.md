# Bitcoin News Monitor

## Overview

Bitcoin News Monitor is a Python-based application that automatically tracks and delivers cryptocurrency news notifications via Telegram. The system continuously monitors multiple RSS feeds and news websites for Bitcoin and cryptocurrency-related content, filtering articles based on configurable keywords and sending real-time alerts to designated Telegram channels.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Core Components

**News Collection Engine**
- RSS feed parser using `feedparser` library for structured news sources
- Web scraping module using `BeautifulSoup` and `trafilatura` for content extraction
- Configurable news sources including CoinTelegraph, Decrypt, Bitcoin Magazine, and CoinDesk
- Keyword-based filtering system for relevant content identification

**Notification System**
- Telegram Bot API integration for message delivery
- HTML message formatting with link previews
- Rate limiting and message length validation
- Connection testing and error handling

**Data Management**
- JSON-based storage for processed articles tracking
- Article deduplication using hash generation
- Configurable retention limits for storage optimization
- File-based logging system with rotation support

**Monitoring Scheduler**
- Configurable monitoring intervals (updated: 1 minute for faster updates)
- Maximum articles per notification limiting
- Continuous monitoring with graceful error recovery

### Configuration Management

**Environment-based Configuration**
- JSON configuration file with environment variable overrides
- Separate settings for Telegram credentials, monitoring intervals, and news sources
- Keyword customization for targeted content filtering
- Logging level and storage path configuration

**Modular Design**
- Separation of concerns across dedicated modules (news_monitor, telegram_bot, utils)
- Centralized configuration validation
- Reusable utility functions for text processing and logging

## External Dependencies

**Third-party Services**
- Telegram Bot API for message delivery
- RSS feed endpoints from major cryptocurrency news sources
- Web scraping targets for additional content sources

**Python Libraries**
- `requests` for HTTP communications
- `feedparser` for RSS feed processing
- `BeautifulSoup` for HTML parsing
- `trafilatura` for content extraction
- `schedule` for task scheduling

**Data Storage**
- Local JSON files for article tracking and configuration
- Log files for system monitoring and debugging

**News Sources**
- 인베스팅닷컴 한국어 암호화폐 뉴스 (kr.investing.com)
- 트레이딩뷰 한국어 크립토 뉴스 (kr.tradingview.com)
- 한국어 키워드 필터링 (비트코인, 암호화폐, 코인, 크립토, 블록체인)

**배포 옵션**
- Replit Always On 서비스 (권장, $7/월)
- AWS EC2 프리티어 (무료 1년)
- DigitalOcean VPS ($5/월)
- 개인 컴퓨터/서버 시스템 서비스