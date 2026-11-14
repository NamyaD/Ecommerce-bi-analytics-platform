"""Post-transform integrity checks."""
def validate(tables):
    failures=[]
    for name,df in tables.items():
        if df.columns.duplicated().any(): failures.append(f"{name}: duplicate column names")
    items=tables.get("order_items")
    if items is not None:
        if "quantity" in items and (items.quantity<=0).any(): failures.append("order_items: non-positive quantity")
        if "unit_price" in items and (items.unit_price<=0).any(): failures.append("order_items: non-positive unit price")
        if "order_id" in items and "orders" in tables and "order_id" in tables["orders"] and not set(items.order_id).issubset(set(tables["orders"].order_id)): failures.append("order_items: orphan order")
    if "orders" in tables and "customer_id" in tables["orders"] and "customers" in tables and "customer_id" in tables["customers"]:
        if not set(tables["orders"].customer_id).issubset(set(tables["customers"].customer_id)): failures.append("orders: orphan customer")
    return failures
