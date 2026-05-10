import os
import ssl
import urllib3
from dotenv import load_dotenv

load_dotenv()

# 회사 SSL 프록시 우회
ssl._create_default_https_context = ssl._create_unverified_context
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
OUTPUT_DIR = "output"

CATEGORY_URLS = {
    "종목분석": "https://finance.naver.com/research/company_list.naver",
    "산업분석": "https://finance.naver.com/research/industry_list.naver",
    "시황정보": "https://finance.naver.com/research/market_info_list.naver",
    "투자정보": "https://finance.naver.com/research/invest_list.naver",
    "경제분석": "https://finance.naver.com/research/economy_list.naver",
    "채권분석": "https://finance.naver.com/research/debenture_list.naver",
}

MAJOR_BROKERS = {
    "삼성증권", "미래에셋증권", "KB증권", "NH투자증권", "한국투자증권",
    "신한투자증권", "키움증권", "하나증권", "대신증권", "메리츠증권",
    "IBK투자증권", "교보증권", "유안타증권", "현대차증권", "LS증권",
}

TOP_N_PER_CATEGORY = 5
PDF_MAX_PAGES = 3
FLASH_MODEL = "gemini-2.5-flash"   # 1차 개별 요약
PRO_MODEL = "gemini-2.5-pro"    # 2차 종합 인사이트

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Referer": "https://finance.naver.com/",
}
