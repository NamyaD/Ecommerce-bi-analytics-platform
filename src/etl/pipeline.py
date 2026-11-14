"""Run the complete extract-transform-validate-load pipeline."""
import json, logging
from src.config import PROCESSED
from src.etl.extract import extract
from src.etl.transform import transform
from src.etl.validate import validate
from src.etl.load import load
logging.basicConfig(level=logging.INFO,format="%(asctime)s %(levelname)s %(message)s")
def main():
    logging.info("Extracting raw sources"); raw=extract(); logging.info("Transforming and cleaning"); clean,report=transform(raw); failures=validate(clean); report["validation_failures"]=failures
    report["rows_received_total"]=sum(report["rows_received"].values()); report["rows_cleaned_total"]=sum(report["rows_cleaned"].values()); report["rows_rejected_total"]=sum(report["rows_rejected"].values())
    with (PROCESSED/"data_quality_report.json").open("w") as f: json.dump(report,f,indent=2)
    if failures: raise ValueError(f"Data validation failed: {failures}")
    logging.info("Loading warehouse tables"); load(clean); logging.info("ETL completed")
if __name__=="__main__": main()
