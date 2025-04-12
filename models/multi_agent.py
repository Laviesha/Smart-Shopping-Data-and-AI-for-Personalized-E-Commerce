import sqlite3
import json
from ast import literal_eval
import time
import os

# DB_PATH = r'C:\Users\m5cd2\Music\Smart-Shopping-Data-and-AI-for-Personalized-E-Commerce\database\ecommerce.db'
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'database', 'demo_ecommerce.db'))

# Get customer's segment from database
def get_customer_segment(customer_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT Customer_Segment FROM customers WHERE Customer_ID = ?", (customer_id,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0].strip().lower()
    return None

def recommend_for_frequent_buyers(browsing_history):
    if not browsing_history:
        print("⚠️ No browsing history found for frequent buyer.")
        return []

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    categories = ', '.join('?' * len(browsing_history))

    # 🔄 Use the 'products' table instead of 'product_recommendation_data'
    cursor.execute(f"""
        SELECT Product_ID FROM products
        WHERE Category IN ({categories})
        ORDER BY Probability_of_Recommendation DESC
        LIMIT 5
    """, browsing_history)

    results = [row[0] for row in cursor.fetchall()]
    conn.close()
    return results


# Agent 2: Recommend popular or discounted products for new visitors
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

# Agent 3: Use pre-generated recommendations for fallback cases
def get_generated_recommendations(customer_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT recommended_ids FROM recommendations WHERE Customer_ID = ?", (customer_id,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return json.loads(result[0])
    return []

# Get customer's browsing history from database
def get_customer_browsing_history(customer_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT Browsing_History FROM customers WHERE Customer_ID = ?", (customer_id,))
    result = cursor.fetchone()
    conn.close()
    return literal_eval(result[0]) if result and result[0] else []

# Main function: route to correct agent
def get_recommendations(customer_id):
    print(f"\n🔍 Connecting to database: {DB_PATH}")
    
    segment = get_customer_segment(customer_id)
    print(f"📂 Customer Segment: {segment}")

    if not segment:
        print("⚠️ Segment not found. Returning empty list.")
        return []

    if segment == "frequent buyer":
        history = get_customer_browsing_history(customer_id)
        print(f"📌 Browsing History: {history}")
        if not history:
            print("⚠️ Empty browsing history. Falling back to popular items.")
            return recommend_for_new_visitors()
        return recommend_for_frequent_buyers(history)

    elif segment == "new visitor":
        return recommend_for_new_visitors()

    else:
        print("ℹ️ Fallback to pre-generated recommendations.")
        return get_generated_recommendations(customer_id)

# Run the recommendation pipeline for a test customer
if __name__ == '__main__':
    test_customer_id = 'C1002'  # Change this to test other customers
    print(f"🚀 Running recommendation pipeline for customer {test_customer_id}")
    start_time = time.time()

    recommendations = get_recommendations(test_customer_id)

    end_time = time.time()
    elapsed = end_time - start_time

    print("\n🛍️ Final Recommendations:", recommendations)
    print(f"⏱️ Time taken: {elapsed:.2f} seconds")

