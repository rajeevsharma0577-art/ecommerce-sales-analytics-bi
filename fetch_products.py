
import requests
import json
from pathlib import Path

API_URL = "https://dummyjson.com/products"
PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_FOLDER = PROJECT_ROOT / "data" / "raw"
RAW_FOLDER.mkdir(parents=True, exist_ok=True)

all_products = []
skip = 0
limit = 100

try:
    print("Connecting to DummyJSON API...")

    while True:
        response = requests.get(
            API_URL,
            params={"limit": limit, "skip": skip},
            timeout=30
        )
        response.raise_for_status()

        data = response.json()
        products = data["products"]

        all_products.extend(products)

        print(f"Fetched: {len(all_products)} / {data['total']}")

        if not products or len(all_products) >= data["total"]:
            break

        skip += len(products)

    output_file = RAW_FOLDER / "products_raw.json"

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(
            {
                "total": len(all_products),
                "products": all_products
            },
            file,
            indent=4,
            ensure_ascii=False
        )

    print("\nAPI FETCH SUCCESSFUL!")
    print("Total Products Fetched:", len(all_products))
    print("Saved At:", output_file)

except requests.exceptions.RequestException as error:
    print("API Connection Failed:", error)

except (KeyError, ValueError) as error:
    print("Data Processing Failed:", error)
