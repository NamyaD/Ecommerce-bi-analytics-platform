"""Generate deterministic, relational synthetic Indian e-commerce data."""
import os, random
from datetime import date
import numpy as np
import pandas as pd
from src.config import RAW

CITIES = {"North":["Delhi","Chandigarh","Amritsar","Jaipur","Lucknow"],"West":["Mumbai","Pune","Ahmedabad"],"South":["Bengaluru","Chennai","Hyderabad","Kochi"],"East":["Kolkata","Bhubaneswar","Patna","Guwahati"]}
CATEGORIES = {"Electronics":["Mobiles","Audio","Computers"],"Fashion":["Clothing","Footwear","Accessories"],"Home":["Kitchen","Furniture","Decor"],"Beauty":["Skincare","Haircare","Makeup"],"Sports":["Fitness","Outdoor","Equipment"]}

def main():
    seed=int(os.getenv("RANDOM_SEED",42)); rng=np.random.default_rng(seed); random.seed(seed)
    nc=int(os.getenv("N_CUSTOMERS",10000)); no=int(os.getenv("N_ORDERS",25000)); npd=int(os.getenv("N_PRODUCTS",1000)); ns=int(os.getenv("N_SELLERS",250))
    start=pd.Timestamp(os.getenv("START_DATE","2024-01-01")); end=pd.Timestamp(os.getenv("END_DATE","2025-12-31")); dates=(end-start).days
    RAW.mkdir(parents=True,exist_ok=True)
    regions=list(CITIES); city_rows=[(r,c) for r,cs in CITIES.items() for c in cs]
    customers=pd.DataFrame({"customer_id":np.arange(1,nc+1),"customer_name":[f"Customer {i:05d}" for i in range(1,nc+1)],"email":[f"customer{i}@example.test" for i in range(1,nc+1)],"signup_date":(start-pd.to_timedelta(rng.integers(0,500,nc),unit="D")).date.astype(str),"region":rng.choice(regions,nc),"city":None,"customer_segment":rng.choice(["New","Regular","Loyal","At Risk"],nc,p=[.25,.4,.2,.15])})
    for i,row in customers.iterrows(): customers.at[i,"city"]=rng.choice(CITIES[row.region])
    sellers=pd.DataFrame({"seller_id":np.arange(1,ns+1),"seller_name":[f"Seller {i:04d}" for i in range(1,ns+1)],"seller_region":rng.choice(regions,ns),"seller_tier":rng.choice(["Gold","Silver","Bronze"],ns,p=[.2,.35,.45]),"joined_date":(start-pd.to_timedelta(rng.integers(30,1000,ns),unit="D")).date.astype(str)})
    products=[]
    cats=list(CATEGORIES)
    for i in range(1,npd+1):
        cat=rng.choice(cats); price=round(float(rng.lognormal(6,0.8)),2); products.append((i,f"{cat} Product {i:04d}",cat,rng.choice(CATEGORIES[cat]),int(rng.integers(1,ns+1)),price,round(price*float(rng.uniform(.45,.8)),2)))
    products=pd.DataFrame(products,columns=["product_id","product_name","category","subcategory","seller_id","unit_price","cost_price"]);
    order_dates=start+pd.to_timedelta(rng.integers(0,dates+1,no),unit="D"); cust_ids=rng.integers(1,nc+1,no); statuses=rng.choice(["delivered","cancelled","returned","shipped"],no,p=[.82,.07,.04,.07])
    orders=pd.DataFrame({"order_id":np.arange(1,no+1),"customer_id":cust_ids,"order_date":order_dates,"order_status":statuses,"promotion_applied":rng.choice([0,1],no,p=[.65,.35]),"payment_method":rng.choice(["UPI","Card","COD","Net Banking","Wallet"],no)})
    items=[]; item_id=1
    for o in orders.itertuples(index=False):
        for _ in range(int(rng.choice([1,2,3],p=[.58,.32,.10]))):
            p=products.iloc[int(rng.integers(0,npd))]; qty=int(rng.integers(1,5)); items.append((item_id,o.order_id,int(p.product_id),int(p.seller_id),qty,float(p.unit_price))); item_id+=1
    items=pd.DataFrame(items,columns=["order_item_id","order_id","product_id","seller_id","quantity","unit_price"]); items["line_revenue"]=items.quantity*items.unit_price
    payments=pd.DataFrame({"payment_id":np.arange(1,no+1),"order_id":orders.order_id,"payment_date":orders.order_date+pd.to_timedelta(rng.integers(0,3,no),unit="D"),"payment_status":np.where(rng.random(no)<.035,"failed","paid"),"payment_amount":items.groupby("order_id").line_revenue.sum().reindex(orders.order_id).fillna(0).to_numpy()})
    delay=rng.normal(1.0,3.0,no).round().astype(int); promised=orders.order_date+pd.to_timedelta(rng.integers(2,7,no),unit="D"); actual=promised+pd.to_timedelta(delay,unit="D")
    deliveries=pd.DataFrame({"delivery_id":np.arange(1,no+1),"order_id":orders.order_id,"promised_delivery_date":promised,"actual_delivery_date":actual,"delivery_status":np.where(delay>0,"delayed","on_time"),"customer_rating":np.clip(np.rint(4.2-delay*.18+rng.normal(0,.8,no)),1,5)})
    locations=pd.DataFrame(city_rows,columns=["region","city"]); locations.insert(0,"location_id",np.arange(1,len(locations)+1))
    dates_df=pd.DataFrame({"date":pd.date_range(start,end)}); dates_df["year"]=dates_df.date.dt.year; dates_df["quarter"]=dates_df.date.dt.quarter; dates_df["month"]=dates_df.date.dt.month; dates_df["month_name"]=dates_df.date.dt.month_name(); dates_df["year_month"]=dates_df.date.dt.strftime("%Y-%m")
    tables={"customers":customers,"sellers":sellers,"products":products,"orders":orders,"order_items":items,"payments":payments,"deliveries":deliveries,"locations":locations,"dates":dates_df}
    # Controlled source defects are deliberately retained for ETL observability.
    customers.loc[customers.sample(frac=.002,random_state=seed).index,"city"]=None
    if len(items)>20:
        items.loc[items.index[:3],"quantity"]=[0,-1,0]; items.loc[items.index[3:5],"unit_price"]=[-5,-2]
    orders.loc[orders.index[:2],"customer_id"]=nc+999
    products.loc[products.index[:4],"category"]="electronicS "
    for name,df in tables.items():
        if name in {"customers","products"}: df.to_csv(RAW/f"{name}.csv",index=False)
        else: df.to_csv(RAW/f"{name}.csv",index=False)
    # Add a duplicate customer source row for duplicate detection.
    customers.iloc[[0]].to_csv(RAW/"customers.csv",mode="a",header=False,index=False)
    print(f"Generated {nc:,} customers, {no:,} orders, {len(items):,} items in {RAW}")
if __name__=="__main__": main()
