# Suggested DAX measures

```dax
Revenue = CALCULATE(SUM(fact_order_items[line_revenue]), NOT fact_orders[order_status] IN {"cancelled", "returned"})
Orders = CALCULATE(DISTINCTCOUNT(fact_orders[order_id]), fact_orders[order_status] <> "cancelled")
AOV = DIVIDE([Revenue], [Orders])
Units Sold = CALCULATE(SUM(fact_order_items[quantity]), fact_orders[order_status] <> "cancelled")
Customers = CALCULATE(DISTINCTCOUNT(fact_orders[customer_id]), fact_orders[order_status] <> "cancelled")
Cancelled Orders = CALCULATE(DISTINCTCOUNT(fact_orders[order_id]), fact_orders[order_status] = "cancelled")
Cancellation Rate = DIVIDE([Cancelled Orders], DISTINCTCOUNT(fact_orders[order_id]))
Returned Orders = CALCULATE(DISTINCTCOUNT(fact_orders[order_id]), fact_orders[order_status] = "returned")
Return Rate = DIVIDE([Returned Orders], DISTINCTCOUNT(fact_orders[order_id]))
```

For repeat-customer rate and LTV, create customer-level summary measures/tables at customer grain; use the explicit formulas in the root README. Revenue growth should use a marked date table and `DATEADD`.
