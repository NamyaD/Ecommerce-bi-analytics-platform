# Architecture

Synthetic CSV generator → extract → transform → validate → SQLAlchemy load → staging and star-schema tables → SQL/Python KPIs → statistical analysis → trend forecast → Power BI semantic/report layer. SQLite is the zero-service local default; PostgreSQL is supported via DB_URL.
