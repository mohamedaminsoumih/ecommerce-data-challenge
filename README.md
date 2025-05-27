# E-commerce User Behavior Analysis

This project is a technical assessment for a Data Engineer position at YouCan. It analyzes e-commerce user behavior across three dimensions:

1. Database performance optimization  
2. Retention and cohort behavior  
3. User segmentation using AI and Elasticsearch  

## Setup

All setup steps are explained in detail in `setup_instructions.md`.

To install dependencies:

```
pip install -r requirements.txt
```

## Folder Structure

```
ecommerce/
├── data/
│   ├── events.csv
│   ├── products.csv
│   └── users.csv
├── figures/
│   └── retention_heatmap.png
├── scripts/
│   ├── benchmark_weekly_active_users.py
│   ├── cohort_analysis.py
│   ├── generate_data.py
│   ├── load_sessions_to_elasticsearch.py
│   └── segment_users_with_tfidf.py
├── sql/
│   ├── weekly_active_users.sql
│   └── revenue_per_category.sql
├── .git/
├── venv/
├── README.md
├── requirements.txt
├── strategy.md
└── setup_instructions.md
```

## Deliverables by Part

### Part I: Data Exploration & SQL Optimization

- SQL queries stored in `sql/`  
- Python benchmarking in `scripts/benchmark_weekly_active_users.py`  

### Part II: Cohort Analysis

- Retention cohort matrix in `scripts/cohort_analysis.py`  
- Heatmap in `figures/retention_heatmap.png`  

### Part III: Behavioral Segmentation

- TF-IDF vectorization and clustering in `scripts/segment_users_with_tfidf.py`  
- Segmented users stored into Elasticsearch index `user_segments`  

## Notes

- Elasticsearch is required for Part III (run using Docker)  
- PostgreSQL is required for Part I and II  
- Strategy summary provided in `strategy.md`  

