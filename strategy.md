# Strategy Summary — Technical Assessment

## Part I: Optimizations Made (SQL & Performance)

- Indexes: Implicitly assumed on `user_id`, `event_type`, `product_id` to improve JOIN and GROUP BY performance.
- Aggregations: Replaced complex expressions with `DATE_TRUNC` and `COUNT(DISTINCT ...)` for clean weekly summaries.
- Separation of logic: Queries written cleanly in SQL, then benchmarked using Python for performance comparison.
- Batching: Efficient loading of data using `psycopg2` or `sqlalchemy` to minimize database round-trips.

## Part II: Retention Insights (Cohort Analysis)

- Grouped users into monthly signup cohorts.
- Measured weekly engagement for 8 weeks post-signup.
- Heatmap clearly shows typical drop-off after week 1, with retention stabilizing between weeks 3–5.
- Peak engagement came from users signing up in months where more tech-related search terms were present (suggesting product cycles or campaigns).

## Part III: Segmentation Rationale (Behavioral AI)

- Search queries were vectorized using TF-IDF (local, fast, interpretable).
- KMeans clustering was used to separate users into 5 segments.
- Keyword-based mapping assigned semantic labels such as:
  - `tech_enthusiast`
  - `budget_buyer`
  - `fashion_oriented`
- Segmented users were stored back into Elasticsearch (`user_segments`) with their labels for further personalization or analytics.
- The solution is fully modular, interpretable, and aligned with practical data engineering workflows.

## Summary

The challenge was approached with clean separation of concerns:
- Data generation
- Storage
- Analysis
- Visualization
- Segmentation
- Documentation


