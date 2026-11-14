-- PostgreSQL-oriented target schema. Runtime tables are created by SQLAlchemy/pandas.
CREATE TABLE IF NOT EXISTS dim_customer (customer_id BIGINT PRIMARY KEY, customer_name TEXT NOT NULL, email TEXT, signup_date DATE, region TEXT, city TEXT, customer_segment TEXT);
CREATE TABLE IF NOT EXISTS dim_seller (seller_id BIGINT PRIMARY KEY, seller_name TEXT NOT NULL, seller_region TEXT, seller_tier TEXT, joined_date DATE);
CREATE TABLE IF NOT EXISTS dim_product (product_id BIGINT PRIMARY KEY, product_name TEXT NOT NULL, category TEXT, subcategory TEXT, seller_id BIGINT REFERENCES dim_seller(seller_id), unit_price NUMERIC(12,2), cost_price NUMERIC(12,2));
CREATE TABLE IF NOT EXISTS dim_date (date DATE PRIMARY KEY, year INT, quarter INT, month INT, month_name TEXT, year_month TEXT);
CREATE TABLE IF NOT EXISTS dim_location (location_id BIGINT PRIMARY KEY, region TEXT, city TEXT);
CREATE TABLE IF NOT EXISTS fact_orders (order_id BIGINT PRIMARY KEY, customer_id BIGINT REFERENCES dim_customer(customer_id), order_date DATE, order_status TEXT, promotion_applied BOOLEAN, payment_method TEXT);
CREATE TABLE IF NOT EXISTS fact_order_items (order_item_id BIGINT PRIMARY KEY, order_id BIGINT REFERENCES fact_orders(order_id), product_id BIGINT REFERENCES dim_product(product_id), seller_id BIGINT REFERENCES dim_seller(seller_id), quantity INT CHECK(quantity > 0), unit_price NUMERIC(12,2) CHECK(unit_price > 0), line_revenue NUMERIC(14,2));
CREATE TABLE IF NOT EXISTS fact_payments (payment_id BIGINT PRIMARY KEY, order_id BIGINT REFERENCES fact_orders(order_id), payment_date DATE, payment_status TEXT, payment_amount NUMERIC(14,2));
CREATE TABLE IF NOT EXISTS fact_deliveries (delivery_id BIGINT PRIMARY KEY, order_id BIGINT REFERENCES fact_orders(order_id), promised_delivery_date DATE, actual_delivery_date DATE, delivery_status TEXT, customer_rating INT);
CREATE INDEX IF NOT EXISTS ix_orders_date ON fact_orders(order_date);
CREATE INDEX IF NOT EXISTS ix_items_product ON fact_order_items(product_id);
