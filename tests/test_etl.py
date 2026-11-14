import pandas as pd
from src.etl.transform import transform
def sample():
 return {"customers":pd.DataFrame({"customer_id":[1,1],"city":[None,None],"region":["North","North"]}),"sellers":pd.DataFrame({"seller_id":[1]}),"products":pd.DataFrame({"product_id":[1],"category":["electronicS "],"unit_price":[10],"cost_price":[5]}),"orders":pd.DataFrame({"order_id":[1,2],"customer_id":[1,99],"order_status":["delivered","delivered"]}),"order_items":pd.DataFrame({"order_item_id":[1,2,3],"order_id":[1,1,2],"product_id":[1,1,1],"quantity":[2,0,1],"unit_price":[10,10,-2]}),"payments":pd.DataFrame({"payment_id":[1,2],"order_id":[1,2]}),"deliveries":pd.DataFrame({"delivery_id":[1,2],"order_id":[1,2]}),"locations":pd.DataFrame({"location_id":[1]}),"dates":pd.DataFrame({"date":["2024-01-01"]})}
def test_duplicate_missing_invalid_orphan_and_category():
 clean,r=transform(sample()); assert r["duplicate_rows"]["customers"]==1; assert clean["customers"].iloc[0].city=="Unknown"; assert clean["products"].iloc[0].category=="Electronics"; assert len(clean["orders"])==1; assert len(clean["order_items"])==1; assert r["invalid_rows"]["order_items.quantity"]==1
