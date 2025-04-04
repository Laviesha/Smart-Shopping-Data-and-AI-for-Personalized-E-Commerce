# import sqlite3
# import pandas as pd
# import os

# # ✅ Update this to your actual data folder path
# DATA_FOLDER = r"C:\Users\m5cd2\Music\Smart-Shopping-Data-and-AI-for-Personalized-E-Commerce\data"

# DB_PATH = "database/ecommerce.db"



# CUSTOMER_CSV = os.path.join(DATA_FOLDER, "customer_data_collection.csv")
# PRODUCT_CSV = os.path.join(DATA_FOLDER, "product_recommendation_data.csv")


# def import_customers():
#     """Import customer data into SQLite."""
#     df = pd.read_csv(CUSTOMER_CSV)

#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()

#     for _, row in df.iterrows():
#         cursor.execute("""
#             INSERT OR IGNORE INTO customers (Customer_ID, Age, Gender, Location, Browsing_History, Purchase_History)
#             VALUES (?, ?, ?, ?, ?, ?)
#         """, (row["Customer_ID"], row["Age"], row["Gender"], row["Location"], row["Browsing_History"], row["Purchase_History"]))

#     conn.commit()
#     conn.close()
#     print("✅ Customer data imported successfully!")


# def import_products():
#     """Import product data into SQLite."""
#     df = pd.read_csv(PRODUCT_CSV)

#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()

#     for _, row in df.iterrows():
#         cursor.execute("""
#             INSERT OR IGNORE INTO products (Product_ID, Category, Price, Brand, Average_Rating)
#             VALUES (?, ?, ?, ?, ?)
#         """, (row["Product_ID"], row["Category"], row["Price"], row["Brand"], row["Average_Rating_of_Similar_Products"]))

#     conn.commit()
#     conn.close()
#     print("✅ Product data imported successfully!")


# if __name__ == "__main__":
#     import_customers()
#     import_products()


import sqlite3
import pandas as pd
import os
import json

def safe_json_load(value):
    try:
        return json.loads(value)  # ✅ Convert to proper Python list
    except json.JSONDecodeError:
        if isinstance(value, list):  # If already a list, convert to JSON string
            return value
        print(f"[ERROR] Invalid JSON format: {value}")
        return []  # Return an empty list to avoid crashing

# ✅ Update this to your actual data folder path
DATA_FOLDER = r"C:\Users\m5cd2\Music\Smart-Shopping-Data-and-AI-for-Personalized-E-Commerce\data"

DB_PATH = "database/ecommerce.db"



CUSTOMER_CSV = os.path.join(DATA_FOLDER, "customer_data_collection.csv")
PRODUCT_CSV = os.path.join(DATA_FOLDER, "product_recommendation_data.csv")


def import_customers():
    """Import customer data into SQLite."""
    df = pd.read_csv(CUSTOMER_CSV)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    for _, row in df.iterrows():
        # cursor.execute("""
        #     INSERT OR IGNORE INTO customers (Customer_ID, Age, Gender, Location, Browsing_History, Purchase_History)
        #     VALUES (?, ?, ?, ?, ?, ?)
        # """, (row["Customer_ID"], row["Age"], row["Gender"], row["Location"], row["Browsing_History"], row["Purchase_History"]))

          cursor.execute("""
              INSERT OR REPLACE INTO customers (
              Customer_ID, Age, Gender, Location, Browsing_History, Purchase_History,
              Customer_Segment, Avg_Order_Value, Holiday, Season
              ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
              """, (
              row['Customer_ID'], row['Age'], row['Gender'], row['Location'],
              row['Browsing_History'], row['Purchase_History'],
              row['Customer_Segment'], row['Avg_Order_Value'],
              row['Holiday'], row['Season']
             ))

    conn.commit()
    conn.close()
    print("✅ Customer data imported successfully!")


# def import_products():
#     """Import product data into SQLite."""
#     df = pd.read_csv(PRODUCT_CSV)

#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()

#     for _, row in df.iterrows():
#         cursor.execute("""
#             INSERT OR IGNORE INTO products (Product_ID, Category, Price, Brand, Average_Rating)
#             VALUES (?, ?, ?, ?, ?)
#         """, (row["Product_ID"], row["Category"], row["Price"], row["Brand"], row["Average_Rating_of_Similar_Products"]))

#     conn.commit()
    # conn.close()
def import_products():
    """Import product data into SQLite."""
    df = pd.read_csv(PRODUCT_CSV)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    for _, row in df.iterrows():
        cursor.execute("""
            INSERT OR IGNORE INTO products (
                Product_ID, Category, Subcategory, Price, Brand,
                Average_Rating_of_Similar_Products, Product_Rating,
                Customer_Review_Sentiment_Score, Holiday, Season,
                Geographical_Location, Similar_Product_List,
                Probability_of_Recommendation
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            row["Product_ID"], row["Category"], row["Subcategory"], row["Price"], row["Brand"],
            row["Average_Rating_of_Similar_Products"], row["Product_Rating"],
            row["Customer_Review_Sentiment_Score"], row["Holiday"], row["Season"],
            row["Geographical_Location"], row["Similar_Product_List"],
            row["Probability_of_Recommendation"]
        ))

    conn.commit()
    conn.close()

    print("✅ Product data imported successfully!")


if __name__ == "__main__":
    import_customers()
    import_products()

