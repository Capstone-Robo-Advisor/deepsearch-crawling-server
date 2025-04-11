# 몽고 DB 연결 테스트 스크립트
import logging
import os

from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, OperationFailure
from dotenv import load_dotenv

# Setting logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Load MongoDB URI
load_dotenv()
MONGO_URI = os.getenv("MONGODB_URI")

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    db = client["deepsearch_news"]
    collections = db.list_collection_names()  # 여기서 실제 연결 시도
    print("✅ 연결 성공!")
    print("컬렉션 목록:", collections)

except (ServerSelectionTimeoutError, OperationFailure) as e:
    print("❌ MongoDB 연결 실패:", str(e))
