SELECT
    DATE_TRUNC('week', timestamp) AS week_start,
    COUNT(DISTINCT user_id) AS weekly_active_users
FROM events
GROUP BY week_start
ORDER BY week_start;
