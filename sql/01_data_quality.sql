SELECT 'orders' table_name, COUNT(*) row_count, SUM(CASE WHEN customer_id IS NULL THEN 1 ELSE 0 END) null_customer_ids FROM fact_orders;
SELECT COUNT(*) orphan_orders FROM fact_orders o LEFT JOIN dim_customer c USING(customer_id) WHERE c.customer_id IS NULL;
