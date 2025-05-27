import time
import pandas as pd
from sqlalchemy import create_engine

# Database connection config
DB_NAME = "ecommerce"
DB_USER = "postgres"
DB_PASSWORD = "admin"  
DB_HOST = "localhost"
DB_PORT = "5432"

# Weekly Active Users SQL query
SQL_QUERY = """
SELECT 
    DATE_TRUNC('week', timestamp) AS week_start,
    COUNT(DISTINCT user_id) AS weekly_active_users
FROM events
GROUP BY week_start
ORDER BY week_start;
"""

def benchmark_query():
    engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
    
    print("Running Weekly Active Users query...")
    start_time = time.time()
    
    df = pd.read_sql(SQL_QUERY, engine)
    
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"Query returned {len(df)} rows in {duration:.4f} seconds.")
    return df

if __name__ == "__main__":
    benchmark_query()
