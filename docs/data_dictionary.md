# Data dictionary

| Entity | Grain | Key fields |
|---|---|---|
| customers | one customer | customer_id, region, city, segment |
| sellers | one seller | seller_id, region, tier |
| products | one SKU | product_id, seller_id, category, prices |
| orders | one order | order_id, customer_id, order_date, status, promotion |
| order_items | one order line | order_item_id, order_id, product_id, quantity, unit_price, line_revenue |
| payments | one payment | payment_id, order_id, status, amount |
| deliveries | one delivery | delivery_id, order_id, promised/actual dates, rating |
| dimensions | one entity/date/location | natural source key retained |
| facts | one business event at stated grain | order/payment/delivery/line IDs |
