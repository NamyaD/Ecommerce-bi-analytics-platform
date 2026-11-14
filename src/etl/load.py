"""Load cleaned sources and dimensional warehouse tables."""
import pandas as pd
from sqlalchemy import text
from src.config import get_engine

def load(tables:dict[str,pd.DataFrame])->None:
    engine=get_engine()
    with engine.begin() as conn:
        for name,df in tables.items(): df.to_sql(f"stg_{name}",conn,if_exists="replace",index=False)
        # Dimension tables retain natural IDs for an approachable portfolio schema.
        tables["customers"].to_sql("dim_customer",conn,if_exists="replace",index=False)
        tables["sellers"].to_sql("dim_seller",conn,if_exists="replace",index=False)
        tables["products"].to_sql("dim_product",conn,if_exists="replace",index=False)
        tables["dates"].to_sql("dim_date",conn,if_exists="replace",index=False)
        tables["locations"].to_sql("dim_location",conn,if_exists="replace",index=False)
        tables["orders"].to_sql("fact_orders",conn,if_exists="replace",index=False)
        tables["order_items"].to_sql("fact_order_items",conn,if_exists="replace",index=False)
        tables["payments"].to_sql("fact_payments",conn,if_exists="replace",index=False)
        tables["deliveries"].to_sql("fact_deliveries",conn,if_exists="replace",index=False)
        conn.execute(text("CREATE INDEX IF NOT EXISTS ix_fact_orders_customer ON fact_orders(customer_id)"))
        conn.execute(text("CREATE INDEX IF NOT EXISTS ix_fact_orders_date ON fact_orders(order_date)"))
        conn.execute(text("CREATE INDEX IF NOT EXISTS ix_fact_items_product ON fact_order_items(product_id)"))
