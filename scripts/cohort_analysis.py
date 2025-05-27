import pandas as pd
from sqlalchemy import create_engine
import seaborn as sns
import matplotlib.pyplot as plt

# Database connection config
DB_NAME = "ecommerce"
DB_USER = "postgres"
DB_PASSWORD = "admin"  
DB_HOST = "localhost"
DB_PORT = "5432"

# SQL to extract cohort data
SQL_QUERY = """
SELECT 
    u.user_id,
    DATE_TRUNC('month', u.signup_date) AS cohort_month,
    DATE_TRUNC('week', e.timestamp) AS event_week,
    EXTRACT(WEEK FROM e.timestamp) - EXTRACT(WEEK FROM u.signup_date) AS weeks_since_signup
FROM users u
JOIN events e ON u.user_id = e.user_id
WHERE e.timestamp >= u.signup_date
  AND EXTRACT(WEEK FROM e.timestamp) - EXTRACT(WEEK FROM u.signup_date) < 8;
"""

def load_cohort_data():
    engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
    df = pd.read_sql(SQL_QUERY, engine)
    return df

def build_retention_matrix(df):
    df['signup_date'] = pd.to_datetime(df['cohort_month'])
    df['event_week'] = pd.to_datetime(df['event_week'])

    df['weeks_since_signup'] = ((df['event_week'] - df['signup_date']).dt.days // 7).astype(int)
    df['cohort_month'] = df['signup_date'].dt.to_period('M')

    # ✅ Add this line to remove invalid values
    df = df[df['weeks_since_signup'] >= 0]

    # Keep only weeks 0 to 7
    df = df[df['weeks_since_signup'] < 8]

    cohort_pivot = (
        df.groupby(['cohort_month', 'weeks_since_signup'])['user_id']
        .nunique()
        .unstack(fill_value=0)
        .sort_index()
    )
    return cohort_pivot

def plot_retention_matrix(matrix):
    plt.figure(figsize=(12, 6))
    sns.heatmap(matrix, annot=True, fmt='d', cmap='Blues')
    plt.title("Weekly Retention by Cohort")
    plt.xlabel("Weeks Since Signup")
    plt.ylabel("Cohort Month")
    plt.tight_layout()
    
    
    plt.savefig("figures/retention_heatmap.png")
    plt.show()



if __name__ == "__main__":
    df = load_cohort_data()
    retention_matrix = build_retention_matrix(df)
    print(retention_matrix)
    plot_retention_matrix(retention_matrix)

