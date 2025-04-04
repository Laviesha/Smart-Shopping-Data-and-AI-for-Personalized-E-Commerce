# import json
# import ollama
# from ast import literal_eval
# import re

# DB_PATH = r'C:\Users\m5cd2\Music\Smart-Shopping-Data-and-AI-for-Personalized-E-Commerce\database\ecommerce.db'

# # ✅ Check for cached recommendations
# def get_cached_recommendations(customer_id):
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()
#     cursor.execute("SELECT recommended_ids FROM recommendations WHERE customer_id = ?", (customer_id,))
#     result = cursor.fetchone()
#     conn.close()
#     if result and result[0]:
#         try:
#             return literal_eval(result[0])
#         except:
#             return []
#     return None

# def get_customer_browsing_history(customer_id):
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()
#     cursor.execute("SELECT Browsing_History FROM customers WHERE Customer_ID = ?", (customer_id,))
#     result = cursor.fetchone()
#     conn.close()
#     if result and result[0]:
#         try:
#             return literal_eval(result[0])
#         except Exception as e:
#             print("⚠️ Failed to parse browsing history:", result[0])
#             print("Error:", e)
#             return []
#     return []

# # ✅ Limit product data for speed
# def fetch_product_embeddings(product_ids):
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()
#     placeholder = ', '.join(['?'] * len(product_ids))
#     query = f"SELECT product_id, category FROM product_embeddings WHERE product_id IN ({placeholder})"
#     cursor.execute(query, product_ids)
#     result = cursor.fetchall()
#     conn.close()
#     products = []
#     for row in result:
#         products.append({
#             'product_id': row[0],
#             'category': row[1]
#         })
#     return products

# def fetch_customer_embedding(customer_id):
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()
#     cursor.execute("SELECT embedding FROM customer_embeddings WHERE customer_id = ?", (customer_id,))
#     result = cursor.fetchone()
#     conn.close()
#     if result:
#         return literal_eval(result[0])
#     return []


# def generate_recommendations_llm(customer_embedding, product_data, browsing_history):
#     model_name = 'orca-mini'

#     short_embedding = customer_embedding[:5] if customer_embedding else []
#     categories = list({p['category'] for p in product_data})
#     product_ids = [p['product_id'] for p in product_data]

#     messages = [
#     {
#         "role": "system",
#         "content": "You are a helpful AI assistant that gives personalized shopping recommendations based on user interests and product categories."
#     },
#     {
#         "role": "user",
#         "content": (
#             f"Browsing history categories: {browsing_history}. "
#             f"Customer embedding (truncated): {customer_embedding[:5]}. "
#             f"Available product IDs and categories: {product_data}. "
#             f"\n\nRecommend 5 product IDs ONLY from this list. Do NOT invent new IDs. "
#             f"Return result as a Python list like ['P2000', 'P2001']."
#         )
#     }
# ]

#     print("🧠 Sending request to Ollama LLM...")
#     response = ollama.chat(model=model_name, messages=messages)
#     print("✅ LLM Response Received!")

#     content = response['message']['content'].strip()
#     print("📝 Raw Model Output:", content)

#     # Try parsing JSON or Python list
#     try:
#         return json.loads(content)
#     except json.JSONDecodeError:
#         try:
#             return literal_eval(content)
#         except Exception:
#             # Final fallback: regex extraction
#             ids = re.findall(r'\bP\d{3,5}\b', content)
#             if ids:
#                 return ids
#             print("❌ Still couldn't parse model response after regex.")
#             return []



# def get_recommendations(customer_id):
#     print(f"🔍 Connecting to database: {DB_PATH}")

#     cached = get_cached_recommendations(customer_id)
#     if cached:
#         print("⚡ Using cached recommendations")
#         return cached

#     browsing_history = get_customer_browsing_history(customer_id)
#     print("📌 Customer Browsing History:", browsing_history)

#     # ✅ Limit number of products
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()
#     cursor.execute("SELECT product_id, category FROM product_embeddings LIMIT 500")
#     all_products = [{'product_id': row[0], 'category': row[1]} for row in cursor.fetchall()]
#     conn.close()

#     print("📊 Limited Product IDs fetched:", len(all_products))

#     # ✅ Extract categories from browsing history
#     browsed_categories = set(browsing_history)  # Directly use as categories

#     # ✅ Filter products based on categories from browsing history
#     filtered_products = [prod for prod in all_products if prod['category'] in browsed_categories]
#     product_data = filtered_products[:1]  # send only top 1 for testing

#     print("🛒 Filtered Products for LLM:", product_data)

#     customer_embedding = fetch_customer_embedding(customer_id)
#     print("🔢 Customer Embedding Fetched:", customer_embedding[:5])

#     recommended_product_ids = generate_recommendations_llm(customer_embedding, product_data, browsing_history)
#     print("✨ Recommended Product IDs:", recommended_product_ids)

#     # ✅ Save to DB for caching
#     if recommended_product_ids:
#         conn = sqlite3.connect(DB_PATH)
#         cursor = conn.cursor()
#         cursor.execute("INSERT INTO recommendations (customer_id, recommended_ids) VALUES (?, ?)", (customer_id, str(recommended_product_ids)))
#         conn.commit()
#         conn.close()

#     return recommended_product_ids


# # Run this part when executing the script
# if __name__ == '__main__':
#     test_customer_id = 'C1000'
#     recommendations = get_recommendations(test_customer_id)
#     print("\n🛍️ Final Recommendations:", recommendations)


import sqlite3
import json
from ast import literal_eval

DB_PATH = r'C:\Users\m5cd2\Music\Smart-Shopping-Data-and-AI-for-Personalized-E-Commerce\database\ecommerce.db'
def get_customer_segment(customer_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT Customer_Segment FROM customers WHERE Customer_ID = ?", (customer_id,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0]
    return None


# Agent 1: Recommend related products for frequent buyers
def recommend_for_frequent_buyers(browsing_history):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    categories = ', '.join('?' * len(browsing_history))
    cursor.execute(f"""
        SELECT Product_ID FROM product_recommendation_data
        WHERE Category IN ({categories})
        ORDER BY Probability_of_Recommendation DESC
        LIMIT 5
    """, browsing_history)
    results = [row[0] for row in cursor.fetchall()]
    conn.close()
    return results

# Agent 2: Recommend popular/discounted products for new visitors
def recommend_for_new_visitors():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT Product_ID FROM products
        WHERE Holiday = 'Yes' OR Product_Rating > 4
        ORDER BY Probability_of_Recommendation DESC
        LIMIT 5
    """)
    results = [row[0] for row in cursor.fetchall()]
    conn.close()
    return results

def get_customer_browsing_history(customer_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT Browsing_History FROM customers WHERE Customer_ID = ?", (customer_id,))
    result = cursor.fetchone()
    conn.close()
    return literal_eval(result[0]) if result and result[0] else []

def get_recommendations(customer_id):
    print(f"🔍 Connecting to database: {DB_PATH}")
    
    segment = get_customer_segment(customer_id)
    print(f"📂 Customer Segment: {segment}")

    if not segment:
        print("⚠️ Segment not found. Returning empty list.")
        return []

    if segment.lower() == "frequent buyer":
        history = get_customer_browsing_history(customer_id)
        print(f"📌 Browsing History: {history}")
        return recommend_for_frequent_buyers(history)

    elif segment.lower() == "new visitor":
        return recommend_for_new_visitors()

    else:
        print("⚠️ Unknown segment. Returning empty list.")
        return []

# Run the recommendation pipeline
if __name__ == '__main__':
    test_customer_id = 'C1000'
    recommendations = get_recommendations(test_customer_id)
    print("\n🛍️ Final Recommendations:", recommendations)
