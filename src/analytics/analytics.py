"""Calculate documented business KPIs and automated insights."""
import json, pandas as pd
from sqlalchemy import text
from src.config import PROCESSED,get_engine

def calculate_kpis()->dict:
    e=get_engine()
    orders=pd.read_sql("SELECT * FROM fact_orders",e); items=pd.read_sql("SELECT * FROM fact_order_items",e); deliveries=pd.read_sql("SELECT * FROM fact_deliveries",e)
    valid=orders[~orders.order_status.isin(["cancelled","returned"])]; rev=float(items[items.order_id.isin(valid.order_id)].line_revenue.sum()); n=int(len(valid)); cust=valid.groupby("customer_id").order_id.nunique();
    repeat=float((cust>=2).sum()/cust.size) if cust.size else 0.0; total_orders=max(len(orders),1)
    returned=int((orders.order_status=="returned").sum()); cancelled=int((orders.order_status=="cancelled").sum())
    delivered=deliveries[deliveries.order_id.isin(valid.order_id)]; ontime=float((delivered.delivery_status=="on_time").mean()) if len(delivered) else 0.0
    avg_days=float((pd.to_datetime(delivered.actual_delivery_date)-pd.to_datetime(delivered.promised_delivery_date)).dt.days.mean()) if len(delivered) else 0.0
    by_customer=items[items.order_id.isin(valid.order_id)].merge(valid[["order_id","customer_id"]],on="order_id").groupby("customer_id").line_revenue.sum()
    k={"total_revenue":round(rev,2),"total_orders":n,"aov":round(rev/n,2) if n else 0,"units_sold":int(items[items.order_id.isin(valid.order_id)].quantity.sum()),"unique_customers":int(valid.customer_id.nunique()),"repeat_customer_rate":round(repeat,4),"cancellation_rate":round(cancelled/total_orders,4),"return_rate":round(returned/total_orders,4),"on_time_delivery_rate":round(ontime,4),"average_delivery_variance_days":round(avg_days,2),"revenue_per_customer":round(rev/valid.customer_id.nunique(),2) if valid.customer_id.nunique() else 0,"customer_lifetime_value_mean":round(float(by_customer.mean()),2) if len(by_customer) else 0,"revenue_per_seller":{},"revenue_per_category":{}}
    item_dim=items.merge(pd.read_sql("SELECT product_id,category FROM dim_product",e),on="product_id"); item_dim=item_dim[item_dim.order_id.isin(valid.order_id)]
    k["revenue_per_seller"]={str(int(a)):round(float(v),2) for a,v in item_dim.groupby("seller_id").line_revenue.sum().items()}; k["revenue_per_category"]={str(a):round(float(v),2) for a,v in item_dim.groupby("category").line_revenue.sum().items()}
    return k
def main():
    k=calculate_kpis(); (PROCESSED/"kpis.json").write_text(json.dumps(k,indent=2)); e=get_engine()
    monthly_orders=pd.read_sql("SELECT order_id,order_date,order_status FROM fact_orders",e); monthly_items=pd.read_sql("SELECT order_id,line_revenue FROM fact_order_items",e); monthly_orders=monthly_orders[~monthly_orders.order_status.isin(["cancelled","returned"])]; monthly=monthly_orders.merge(monthly_items,on="order_id"); monthly["month"]=pd.to_datetime(monthly.order_date).dt.strftime("%Y-%m"); monthly=monthly.groupby("month",as_index=False).line_revenue.sum().rename(columns={"line_revenue":"revenue"}).sort_values("month")
    insights=[]
    if len(monthly)>=2:
        last=monthly.iloc[-1]; prev=monthly.iloc[-2]; growth=(last.revenue/prev.revenue-1)*100 if prev.revenue else 0; insights.append(f"Revenue in {last.month} was ₹{last.revenue:,.0f}, changing {growth:+.1f}% month-over-month.")
    cust= pd.read_sql("SELECT customer_id,SUM(line_revenue) revenue FROM fact_orders o JOIN fact_order_items i USING(order_id) WHERE order_status NOT IN ('cancelled','returned') GROUP BY customer_id",e)
    if len(cust):
        top=cust.nlargest(max(1,int(len(cust)*.1)),"revenue").revenue.sum()/cust.revenue.sum()*100; insights.append(f"The top 10% of purchasing customers contributed {top:.1f}% of recognized item revenue.")
    cat=max(k["revenue_per_category"],key=k["revenue_per_category"].get) if k["revenue_per_category"] else "N/A"
    insights.append(f"{cat} was the highest-revenue product category in this generated dataset.")
    (PROCESSED/"business_insights.json").write_text(json.dumps({"insights":insights},indent=2)); print(json.dumps({"kpis":{a:b for a,b in k.items() if not isinstance(b,dict)},"insights":insights},indent=2))
if __name__=="__main__": main()
