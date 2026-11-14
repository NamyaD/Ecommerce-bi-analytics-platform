"""Shared configuration and database helpers."""
import os
from pathlib import Path
from sqlalchemy import create_engine

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"
PROCESSED.mkdir(parents=True, exist_ok=True)
DB_URL = os.getenv("DB_URL", "sqlite:///data/processed/ecommerce_bi.sqlite")
if DB_URL.startswith("sqlite:///") and not DB_URL.startswith("sqlite:////"):
    DB_URL = "sqlite:///" + str((ROOT / DB_URL.replace("sqlite:///", "", 1)).resolve())

def get_engine():
    return create_engine(DB_URL, future=True)
