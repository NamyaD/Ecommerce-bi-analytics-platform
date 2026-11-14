import pandas as pd
from sqlalchemy import create_engine
import src.analytics.analytics as analytics

def test_kpi_calculations(monkeypatch):
    engine=create_engine("sqlite:///:memory:")
    pd.DataFrame({"order_id":[1,2,3],"customer_id":[10,10,20],"order_status":["delivered","delivered","cancelled"]}).to_sql("fact_orders",engine,index=False)
    pd.DataFrame({"order_id":[1,1,2,3],"product_id":[1,2,1,1],"seller_id":[7,7,7,7],"quantity":[1,2,1,1],"line_revenue":[100.,50.,100.,100.]}).to_sql("fact_order_items",engine,index=False)
    pd.DataFrame({"order_id":[1,2],"delivery_status":["on_time","delayed"],"actual_delivery_date":["2024-01-02","2024-01-05"],"promised_delivery_date":["2024-01-02","2024-01-03"]}).to_sql("fact_deliveries",engine,index=False)
    pd.DataFrame({"product_id":[1,2],"category":["Electronics","Home"]}).to_sql("dim_product",engine,index=False)
    monkeypatch.setattr(analytics,"get_engine",lambda:engine)
    k=analytics.calculate_kpis()
    assert k["total_revenue"]==250.0
    assert k["total_orders"]==2
    assert k["aov"]==125.0
    assert k["unique_customers"]==1
    assert k["repeat_customer_rate"]==1.0
    assert abs(k["cancellation_rate"]-1/3)<0.0001
