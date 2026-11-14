# Ecommerce-bi-analytics-platform
End-to-end e-commerce BI analytics platform with ETL, SQL, statistical analysis, forecasting and business insights.

# E-Commerce Business Intelligence & Analytics Platform

An end-to-end portfolio project for BI Engineer, Data Analyst and Data Engineer internships. It generates reproducible synthetic Indian e-commerce data, deliberately injects source-quality defects, cleans and validates the data, loads an analytical warehouse, and produces KPI, statistical, forecast and business-insight outputs for Power BI.

> **Data notice:** All records are synthetic. Results and forecasts depend on the random seed and environment configuration; they are not claims about a real business.

## Business problem

An e-commerce team needs a consistent view of sales, customers, products, sellers, regions and fulfilment. This platform answers revenue movement, product/seller performance, AOV, repeat purchase, customer value, cancellations, returns, delivery performance, promotion association and three-month outlook questions.

## Architecture

```text
Synthetic Data
      ↓
Extract → Transform → Validate
      ↓
PostgreSQL / SQLite warehouse
      ↓
SQL Analytics → Python KPI Layer
      ↓
Statistics → Forecasting → Power BI
```

SQLite is the default and needs no Docker. SQLAlchemy supports PostgreSQL by setting `DB_URL`.

## Stack and dataset

Python 3.11+, Pandas, NumPy, SQLAlchemy, SQLite/PostgreSQL, SciPy, scikit-learn and pytest. Defaults: 10,000 customers, 25,000 orders, 1,000 products, 250 sellers, 24 months and 50,000+ generated order items. Indian regions and cities are represented.

Configure using `.env` (copy `.env.example`; export values in your shell or use your preferred dotenv loader): `RANDOM_SEED`, `N_CUSTOMERS`, `N_ORDERS`, `N_PRODUCTS`, `N_SELLERS`, `START_DATE`, `END_DATE`, `DB_URL`. Scale these counts as compute permits. The default seed is 42.

## Data model and ETL

Raw CSV entities: customers, sellers, products, orders, order_items, payments, deliveries, locations and dates. ETL deduplicates, normalizes categories, fills missing customer city, rejects invalid quantities/prices and orphan foreign keys, calculates line revenue, validates referential integrity and loads staging plus warehouse tables. The quality report records received, duplicate, null, invalid, orphan, rejected and cleaned counts.

Warehouse dimensions: `dim_customer`, `dim_product`, `dim_seller`, `dim_date`, `dim_location`. Facts: `fact_orders` (one row/order), `fact_order_items` (one row/order-product line), `fact_payments` (one row/payment) and `fact_deliveries` (one row/delivery). Natural source IDs are retained as keys for clarity.

## SQL analytics

The `sql/` directory contains runnable examples for quality, customer, product, seller, region, operations, KPI and advanced analysis, including CTEs, ranking, lag, rolling windows and running totals. The warehouse loader creates indexes on order date/customer and item product.

## KPI definitions

- Revenue: sum of item extended revenue on orders excluding cancelled and returned orders.
- Orders: count of orders excluding cancelled orders (returned orders remain in this count).
- AOV: recognized revenue divided by non-cancelled orders.
- Units sold: sum of quantities on non-cancelled orders.
- Unique customers: distinct customers with non-cancelled orders.
- Repeat customer rate: customers with at least two non-cancelled orders divided by customers with at least one.
- Cancellation/return rate: cancelled/returned order count divided by all orders.
- On-time delivery rate: deliveries marked on_time divided by deliveries for non-cancelled orders.
- Average delivery variance: mean actual minus promised days (negative means early).
- Revenue per customer: recognized revenue / distinct purchasing customers. Customer lifetime value proxy: mean observed recognized revenue per purchasing customer over the dataset window.
- Revenue per seller/category: recognized item revenue grouped by seller/category.

## Statistical analysis

Welch's t-test compares order revenue distributions for promoted vs non-promoted orders (an order-total proxy for AOV; the test is not causal). Pearson correlation evaluates delivery variance vs rating. Linear regression predicts order revenue from promotion flag, order month and item count, with MAE and R².

## Forecasting

Linear trend regression forecasts monthly revenue and non-cancelled order volume for the next three months. A chronological 80/20 holdout reports MAE/RMSE. It is a baseline, not a seasonality-aware production forecast.

## Business insights and Power BI

`business_insights.json`, `kpis.json`, `statistical_analysis.json` and `forecast.json` are generated outputs. `powerbi/` specifies five report pages and DAX measures; no fake PBIX is included. Import warehouse tables or export curated views from the database.

## How to run

Install Python 3.11+ and dependencies:

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate ; macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python -m src.data_generation.generate_data
python -m src.etl.pipeline
python -m src.analytics.analytics
python -m src.statistics.analysis
python -m src.forecasting.forecast
pytest -q
```

Run commands from the repository root. For PostgreSQL, start optional `docker compose up -d` and set `DB_URL` to a PostgreSQL SQLAlchemy URL; credentials should be supplied through environment variables and never committed.

## Testing and limitations

Tests cover transformation rules, invalid values, duplicate/orphan handling, KPI formulas and core outputs. Synthetic data has designed distributions and does not represent real customer behaviour. The model uses natural IDs rather than generated surrogate keys; SQL DDL documents a production-oriented target. The forecasting model is intentionally simple, and promotion comparison/correlation are observational. No Power BI binary is generated.

## Project structure

See `src/` for generation, ETL, analytics, statistics and forecasting; `database/` for schema references; `sql/` for analysis; `powerbi/` for report design; `tests/` for automated checks; and `docs/` for architecture, dictionary, questions and resume phrasing.

## Future improvements

Add incremental CDC ingestion, slowly changing dimensions, orchestrated scheduling, automated freshness/volume monitoring, seasonal forecasting and a published Power BI semantic model.
