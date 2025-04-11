import requests
import logging
import os

from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime

# Setting logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Load API key and MongoDB URI
load_dotenv()
API_KEY = os.getenv("DEEPSEARCH_CRAWLER_API_KEY")
MONGO_URI = os.getenv("MONGODB_URI")

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client["deepsearch_news"]
collection = db["articles"]

def fetch_articles(page = 1, page_size = 50):
    url = "https://api-v2.deepsearch.com/v1/global-articles"
    params = {
        "date_from": "2025-04-01",
        "date_to": "2025-04-10",
        "page": page,
        "page_size": page_size,
        "api_key": API_KEY
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # 4xx/5xx 에러 발생 시 예외

        data = response.json()
        articles = data.get("data", [])

        logger.info(f"📡 API 호출 성공 - 페이지 {page}, 수신 기사 수: {len(articles)}")
        return articles

    except requests.exceptions.RequestException as e:
        logger.error(f"❌ API 호출 실패 - 페이지 {page}, 오류: {str(e)}")
        return []

    except ValueError as e:
        logger.error(f"❌ JSON 디코딩 실패 - 페이지 {page}, 오류: {str(e)}")
        return []

def save_to_mongo(articles):
    saved_count = 0
    skipped_count = 0

    for article in articles:
        # 중복 방지 : 기사 URL 이 이미 있는지 확인
        article_id = article.get("id")

        if collection.find_one({"id" : article["id"]}):
            logger.info(f"🟡 중복 스킵 - 기사 ID: {article_id}, 제목: {article.get('title_ko', '')[:30]}...")
            skipped_count += 1
            continue

        collection.insert_one(article)
        logger.info(f"✅ 저장 완료 - 기사 ID: {article_id}, 제목: {article.get('title_ko', '')[:30]}...")
        saved_count += 1

    logger.info(f"총 저장: {saved_count}건 / 중복 스킵: {skipped_count}건")

def run_crawler():
    max_pages = 5
    for page in range(1, max_pages + 1):   # 5페이지 까지 예시
        logger.info(f"🏃🏻페이지 {page} 크롤링 중...")
        articles = fetch_articles(page=page)
        logger.info(f"➡️ {len(articles)}개 기사 수집됨")

        save_to_mongo(articles)

        if len(articles) < 50:
            logger.info("✅ 마지막 페이지에 도달했으므로 크롤링 종료")
            break


if __name__ == "__main__":
    run_crawler()
    logger.info("전체 크롤링 작업 완료")