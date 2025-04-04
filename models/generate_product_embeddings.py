import sqlite3
import ollama
import json

# Connect to SQLite database
conn = sqlite3.connect("../database/ecommerce.db")
cursor = conn.cursor()

# 🔥 Fetch all products (only columns that exist in `products`)
cursor.execute("""
    SELECT Product_ID, Category, Price, Brand, Average_Rating_of_Similar_Products 
    FROM products
""")
products = cursor.fetchall()

# Function to get embeddings using Ollama
def get_embedding(text):
    response = ollama.embeddings(model="all-minilm", prompt=text)
    return response["embedding"]

# Store embeddings
for product in products:
    product_id, category, price, brand, avg_rating = product

    # 🔥 Use only the columns that exist
    product_desc = f"{category} by {brand}, avg rating: {avg_rating}/5"

    embedding = get_embedding(product_desc)
    
    # ✅ Insert into product_embeddings (only existing columns)
    cursor.execute("""
        INSERT OR REPLACE INTO product_embeddings 
        (product_id, category, price, brand, avg_rating_similar, embedding) 
        VALUES (?, ?, ?, ?, ?, ?)
    """, (product_id, category, price, brand, avg_rating, json.dumps(embedding)))

conn.commit()
conn.close()
print("✅ Product embeddings stored successfully!")


# import sqlite3
# import ollama
# import json

# # Connect to SQLite database
# conn = sqlite3.connect("../database/ecommerce.db")
# cursor = conn.cursor()

# # 🔥 Fetch all relevant product columns
# cursor.execute("""
#     SELECT 
#         Product_ID, Category, Subcategory, Price, Brand,
#         Average_Rating_of_Similar_Products, Product_Rating,
#         Customer_Review_Sentiment_Score, Holiday, Season,
#         Geographical_Location
#     FROM products
# """)
# products = cursor.fetchall()

# # Function to get embeddings using Ollama
# def get_embedding(text):
#     response = ollama.embeddings(model="all-minilm", prompt=text)
#     return response["embedding"]

# # Store embeddings
# for product in products:
#     (
#         product_id, category, subcategory, price, brand,
#         avg_rating_similar, product_rating, sentiment_score,
#         holiday, season, location
#     ) = product

#     # 🔥 Build a detailed description for embeddings
#     product_desc = (
#         f"{category} > {subcategory}, Brand: {brand}, "
#         f"Price: ₹{price}, Product Rating: {product_rating}/5, "
#         f"Sentiment Score: {sentiment_score}, "
#         f"Season: {season}, Holiday: {holiday}, Location: {location}"
#     )

#     embedding = get_embedding(product_desc)

#     # ✅ Insert into product_embeddings
#     cursor.execute("""
#         INSERT OR REPLACE INTO product_embeddings 
#         (product_id, category, price, brand, avg_rating_similar, embedding) 
#         VALUES (?, ?, ?, ?, ?, ?)
#     """, (product_id, category, price, brand, avg_rating_similar, json.dumps(embedding)))

# conn.commit()
# conn.close()
# print("✅ Product embeddings stored successfully!")
