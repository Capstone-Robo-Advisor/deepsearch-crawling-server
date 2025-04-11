# 1. Python 베이스 이미지
FROM python:3.10-slim

# 2. 작업 디렉토리 생성
WORKDIR /app

# 3. 로컬 코드 복사
COPY . .

# 4. 의존성 설치
RUN pip install --no-cache-dir -r requirements.txt

# 5. 실행 명령
CMD ["python", "crawling/deepsearch_crawler.py"]