
import json
import pandas as pd
from pathlib import Path

# 1. Project location
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# 2. File paths
RAW_FILE = PROJECT_ROOT / "data" / "raw" / "products_raw.json"
OUTPUT_FOLDER = PROJECT_ROOT / "data" / "processed"
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = OUTPUT_FOLDER / "products_cleaned.csv"

try:
    print("Reading API raw data...")

    # 3. Read JSON
    with open(RAW_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    df = pd.DataFrame(data["products"])

    print("Raw records:", len(df))

    # 4. Select required columns
    required_columns = [
        "id",
        "title",
        "category",
        "price",
        "discountPercentage",
        "rating",
        "stock",
        "brand",
        "sku",
        "availabilityStatus"
    ]

    df = df[required_columns].copy()

    # 5. Rename columns
    df.rename(columns={
        "id": "ProductID",
        "title": "ProductName",
        "category": "Category",
        "price": "Price",
        "discountPercentage": "DiscountPercentage",
        "rating": "Rating",
        "stock": "Stock",
        "brand": "Brand",
        "sku": "SKU",
        "availabilityStatus": "AvailabilityStatus"
    }, inplace=True)

    # 6. Clean missing values
    df["Brand"] = df["Brand"].fillna("Unknown")
    df["SKU"] = df["SKU"].fillna("Unknown")
    df["AvailabilityStatus"] = (
        df["AvailabilityStatus"].fillna("Unknown")
    )

    # 7. Remove duplicate Product IDs
    df.drop_duplicates(
        subset=["ProductID"],
        keep="last",
        inplace=True
    )

    # 8. Save processed CSV
    df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

    print("\nPRODUCT PROCESSING SUCCESSFUL!")
    print("Total Clean Products:", len(df))
    print("Duplicate Product IDs:", df["ProductID"].duplicated().sum())
    print("Missing Values:", df.isnull().sum().sum())
    print("Saved File:", OUTPUT_FILE)

except Exception as error:
    print("\nPRODUCT PROCESSING FAILED!")
    print("Error:", error)
