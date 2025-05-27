import time
import pandas as pd
from sqlalchemy import create_engine

# Database connection config
DB_NAME = "ecommerce"
DB_USER = "postgres"
DB_PASSWORD = "admin"  # Replace this
DB_HOST = "localhost"
DB_PORT = "5432"

# Revenue per category SQL query
SQL_QUERY = """
SELECT 
    p.category,
    SUM(p.price) AS total_revenue
FROM events e
JOIN products p ON e.product_id = p.product_id
WHERE e.event_type = 'purchased'
GROUP BY p.category
ORDER BY total_revenue DESC;
"""

def benchmark_query():
    engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
    
    print("Running Revenue per Category query...")
    start_time = time.time()
    
    df = pd.read_sql(SQL_QUERY, engine)
    
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"Query returned {len(df)} rows in {duration:.4f} seconds.")
    return df

if __name__ == "__main__":
    benchmark_query()
