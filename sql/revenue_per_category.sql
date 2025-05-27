SELECT
    p.category,
    SUM(p.price) AS total_revenue
FROM events e
JOIN products p ON e.product_id = p.product_id
WHERE e.event_type = 'purchased'
GROUP BY p.category
ORDER BY total_revenue DESC;
