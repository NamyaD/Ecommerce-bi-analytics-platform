"""Read generated raw CSV sources."""
import pandas as pd
from src.config import RAW
TABLES=["customers","sellers","products","orders","order_items","payments","deliveries","locations","dates"]
def extract() -> dict[str,pd.DataFrame]:
    missing=[name for name in TABLES if not (RAW/f"{name}.csv").exists()]
    if missing: raise FileNotFoundError(f"Missing raw CSVs: {missing}. Run data generation first.")
    return {name:pd.read_csv(RAW/f"{name}.csv") for name in TABLES}
