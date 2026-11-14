"""Clean source data while retaining detailed quality metrics."""
import pandas as pd

def transform(tables:dict[str,pd.DataFrame])->tuple[dict[str,pd.DataFrame],dict]:
    clean={}; report={"rows_received":{},"duplicate_rows":{},"null_issues":{},"invalid_rows":{},"orphan_rows":{},"rows_rejected":{},"rows_cleaned":{}}
    for name,df in tables.items():
        report["rows_received"][name]=int(len(df)); dup=int(df.duplicated().sum()); report["duplicate_rows"][name]=dup; df=df.drop_duplicates().copy()
        report["null_issues"][name]={c:int(v) for c,v in df.isna().sum().items() if v}
        clean[name]=df
    c=clean["customers"]; c["city"]=c["city"].fillna("Unknown"); c["region"]=c["region"].fillna("Unknown")
    p=clean["products"]; p["category"]=p["category"].astype(str).str.strip().str.title().replace({"Electronics":"Electronics","Electronics ":"Electronics"})
    # Normalize the deliberately inconsistent spelling.
    p["category"]=p["category"].replace({"Electronics":"Electronics","ElectronicS":"Electronics"})
    for table,col in [("order_items","quantity"),("order_items","unit_price"),("products","unit_price"),("products","cost_price")]:
        df=clean[table]; invalid=(pd.to_numeric(df[col],errors="coerce")<=0)|pd.to_numeric(df[col],errors="coerce").isna(); report["invalid_rows"][f"{table}.{col}"]=int(invalid.sum())
        df.drop(index=df.index[invalid],inplace=True)
    valid_customers=set(c.customer_id); o=clean["orders"]; orphan=~o.customer_id.isin(valid_customers); report["orphan_rows"]["orders.customer_id"]=int(orphan.sum()); o.drop(index=o.index[orphan],inplace=True)
    valid_orders=set(o.order_id)
    for table in ["order_items","payments","deliveries"]:
        df=clean[table]; bad=~df.order_id.isin(valid_orders); report["orphan_rows"][f"{table}.order_id"]=int(bad.sum()); df.drop(index=df.index[bad],inplace=True)
    prod=set(p.product_id); it=clean["order_items"]; bad=~it.product_id.isin(prod); report["orphan_rows"]["order_items.product_id"]=int(bad.sum()); it.drop(index=it.index[bad],inplace=True)
    clean["order_items"]["line_revenue"]=clean["order_items"].quantity*clean["order_items"].unit_price
    for name,df in clean.items(): report["rows_rejected"][name]=max(0,report["rows_received"][name]-len(df)); report["rows_cleaned"][name]=int(len(df))
    report["validation_failures"]=[]
    return clean,report
