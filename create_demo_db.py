# import pandas as pd
# import sqlite3
# import os

# # Load CSVs
# customers = pd.read_csv("data/customer_data_collection.csv").head(1000)
# products = pd.read_csv("data/product_recommendation_data.csv").head(1000)

# # Create a new SQLite DB
# db_path = "database/demo_ecommerce.db"
# os.makedirs("database", exist_ok=True)
# conn = sqlite3.connect(db_path)

# # Write tables to DB
# customers.to_sql("customers", conn, if_exists="replace", index=False)
# products.to_sql("products", conn, if_exists="replace", index=False)

# conn.commit()
# conn.close()

# print(f"✅ Demo database created at: {db_path}")

import pandas as pd
import sqlite3
import os

# Load full CSVs
customers = pd.read_csv("data/customer_data_collection.csv")
products = pd.read_csv("data/product_recommendation_data.csv")

# Randomly sample 1000 entries (set seed for reproducibility)
customers_sample = customers.sample(n=1000, random_state=42)
products_sample = products.sample(n=1000, random_state=42)

# Create a new SQLite DB
db_path = "database/demo_ecommerce.db"
os.makedirs("database", exist_ok=True)
conn = sqlite3.connect(db_path)

# Save sampled data to the database
customers_sample.to_sql("customers", conn, if_exists="replace", index=False)
products_sample.to_sql("products", conn, if_exists="replace", index=False)

# ✅ Save sampled customer IDs to CSV for testing
customers_sample[['Customer_ID']].to_csv("data/demo_customer_ids.csv", index=False)

conn.commit()
conn.close()

print(f"✅ Random sample database created at: {db_path}")
print(f"📄 Sampled customer IDs saved to: data/demo_customer_ids.csv")
