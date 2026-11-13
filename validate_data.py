
import pandas as pd
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CLEAN = ROOT / "data" / "clean"
DB = ROOT / "data" / "instamart.db"

customers = pd.read_csv(CLEAN / "customers.csv")
products = pd.read_csv(CLEAN / "products.csv")
orders = pd.read_csv(CLEAN / "orders.csv")

# Customer validation
assert len(customers) == 1200
assert customers["city"].nunique() == 6
assert customers["gender"].value_counts().to_dict() == {
    "female": 610, "male": 560, "unknown": 30
}
assert customers["age"].isna().sum() == 0

# Order validation
assert len(orders) == 12309
assert orders["order_id"].nunique() == 12309
assert orders["status"].value_counts().to_dict() == {
    "completed": 11110, "cancelled": 1199
}
assert orders["order_amount"].isna().sum() == 0
assert orders.loc[
    orders["status"] == "completed", "delivery_minutes"
].isna().sum() == 0
assert orders.loc[
    orders["status"] == "cancelled", "delivery_minutes"
].isna().sum() == 1199
assert round(
    orders.loc[orders["status"] == "completed", "order_amount"].sum(), 2
) == 2998668.80

# SQLite validation
with sqlite3.connect(DB) as conn:
    tables = pd.read_sql_query(
        "SELECT name FROM sqlite_master WHERE type='table'", conn
    )["name"].tolist()

    assert all(t in tables for t in ["customers", "products", "orders"])

    for table, expected in [
        ("customers", 1200),
        ("products", 40),
        ("orders", 12309)
    ]:
        actual = pd.read_sql_query(
            f"SELECT COUNT(*) AS total FROM {table}", conn
        ).iloc[0, 0]
        assert actual == expected

print("ALL CHECKPOINTS PASSED")
