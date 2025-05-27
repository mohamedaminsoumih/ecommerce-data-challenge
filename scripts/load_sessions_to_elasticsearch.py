from elasticsearch import Elasticsearch, helpers
from faker import Faker
import random
from datetime import datetime, timedelta

# (Used Claude to give me a realistic e-commerce search terms)
real_queries = [
    "wireless headphones",
    "gaming laptop",
    "cheap phone",
    "summer dress",
    "office chair",
    "budget smartphone",
    "discount backpack",
    "men's running shoes",
    "4k smart tv",
    "wireless mouse",
    "ladies handbag",
    "baby stroller",
    "kitchen appliances",
    "headphones under 200",
    "gaming monitor 144hz",
    "winter jacket",
    "gaming keyboard",
    "formal shoes men",
    "air fryer",
    "led desk lamp"
]


# Connect to local Elasticsearch (no auth)
es = Elasticsearch("http://localhost:9200")

fake = Faker()

# Sample product IDs
product_ids = [f"p{str(i).zfill(3)}" for i in range(1, 51)]

# Generate fake session documents
def generate_session_docs(n=1000):
    sessions = []
    for _ in range(n):
        user_id = fake.uuid4()
        search_query = random.choice(real_queries)
        clicked = random.sample(product_ids, k=random.randint(1, 4))
        timestamp = fake.date_time_between(start_date='-3M', end_date='now')

        sessions.append({
            "_index": "user_sessions",
            "_source": {
                "user_id": user_id,
                "search_query": search_query,
                "clicked_product_ids": clicked,
                "timestamp": timestamp.isoformat()
            }
        })
    return sessions

# Load data
def load_data():
    docs = generate_session_docs()
    helpers.bulk(es, docs)
    print(f"Inserted {len(docs)} documents into 'user_sessions' index.")

if __name__ == "__main__":
    load_data()
