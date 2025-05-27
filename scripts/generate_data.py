import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta
import os

fake = Faker()

NUM_USERS = 1000
NUM_PRODUCTS = 200
DAYS_RANGE = 365

COUNTRIES = ['MA', 'FR', 'SA', 'US', 'UAE']
CATEGORIES = [
    'electronics',
    'clothing',
    'beauty',
    'home_and_kitchen',
    'toys',
    'groceries',
    'furniture',
    'automotive',
    'stationery',
    'sports_and_leisure'
]
EVENT_TYPES = ['viewed', 'add-to-cart', 'purchased']

def generate_users():
    users = []
    start_date = datetime.now() - timedelta(days=DAYS_RANGE)
    for i in range(1, NUM_USERS + 1):
        signup_date = start_date + timedelta(days=random.randint(0, DAYS_RANGE))
        users.append([i, signup_date.date(), random.choice(COUNTRIES)])
    return pd.DataFrame(users, columns=['user_id', 'signup_date', 'country'])

def generate_products():
    products = []
    for i in range(1, NUM_PRODUCTS + 1):
        category = random.choice(CATEGORIES)
        price = round(random.uniform(5, 5000), 2)  # prices in MAD
        products.append([i, category, price])
    return pd.DataFrame(products, columns=['product_id', 'category', 'price'])

def generate_events(users_df, products_df):
    events = []
    for _, user in users_df.iterrows():
        num_events = random.randint(5, 50)
        for _ in range(num_events):
            event_date = user['signup_date'] + timedelta(days=random.randint(0, 60))
            if event_date > datetime.now().date():
                continue
            product = products_df.sample(1).iloc[0]
            event_type = random.choices(EVENT_TYPES, weights=[0.6, 0.3, 0.1])[0]
            events.append([user['user_id'], event_type, product['product_id'], event_date])
    return pd.DataFrame(events, columns=['user_id', 'event_type', 'product_id', 'timestamp'])

def save_data(users_df, products_df, events_df):
    os.makedirs("data", exist_ok=True)
    users_df.to_csv("data/users.csv", index=False)
    products_df.to_csv("data/products.csv", index=False)
    events_df.to_csv("data/events.csv", index=False)
    print("Data generated and saved in /data folder.")

def main():
    print("🔄 Generating fake data...")
    users = generate_users()
    products = generate_products()
    events = generate_events(users, products)
    save_data(users, products, events)

if __name__ == "__main__":
    main()
