import pandas as pd
import psycopg2
from sqlalchemy import create_engine

# Database connection parameters
DB_NAME = "ecommerce"
DB_USER = "postgres"
DB_PASSWORD = "admin"  
DB_HOST = "localhost"
DB_PORT = "5432"

# File paths
USERS_CSV = "data/users.csv"
PRODUCTS_CSV = "data/products.csv"
EVENTS_CSV = "data/events.csv"

def load_csv_to_postgres(csv_path, table_name, engine):
    print(f"Loading {csv_path} into {table_name}...")
    df = pd.read_csv(csv_path)
    df.to_sql(table_name, con=engine, index=False, if_exists='append')
    print(f"Loaded {len(df)} rows into '{table_name}'")

def main():
    print("Connecting to PostgreSQL...")
    try:
        engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
        
        load_csv_to_postgres(USERS_CSV, "users", engine)
        load_csv_to_postgres(PRODUCTS_CSV, "products", engine)
        load_csv_to_postgres(EVENTS_CSV, "events", engine)

        print("All data loaded successfully.")

    except Exception as e:
        print("Error loading data:", e)

if __name__ == "__main__":
    main()
