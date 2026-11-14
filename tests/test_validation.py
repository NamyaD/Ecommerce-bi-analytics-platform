import pandas as pd
from src.etl.validate import validate
def test_validation_detects_invalid_quantity():
 t={"customers":pd.DataFrame({"customer_id":[1]}),"orders":pd.DataFrame({"customer_id":[1]}),"order_items":pd.DataFrame({"quantity":[0],"unit_price":[1]})}; assert any("quantity" in x for x in validate(t))
