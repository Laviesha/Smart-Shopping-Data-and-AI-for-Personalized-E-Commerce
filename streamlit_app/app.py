# import streamlit as st
# import sqlite3
# import os
# import sys
# import os

# # 🔧 Add the 'models' directory to the Python path
# models_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'models'))
# if models_path not in sys.path:
#     sys.path.append(models_path)

# from multi_agent import get_recommendations 

# # ⛳ Make sure this matches your DB path
# DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'database', 'ecommerce.db'))

# # 🧠 Function to fetch details for given product IDs
# def fetch_product_details(product_ids):
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()

#     placeholders = ','.join(['?'] * len(product_ids))
#     query = f"""
#         SELECT Product_ID, Category, Subcategory, Price, Brand, Product_Rating, Probability_of_Recommendation
#         FROM products
#         WHERE Product_ID IN ({placeholders})
#     """
#     cursor.execute(query, product_ids)
#     rows = cursor.fetchall()
#     conn.close()

#     return [
#         {
#             'id': row[0],
#             'category': row[1],
#             'subcategory': row[2],
#             'price': row[3],
#             'brand': row[4],
#             'rating': row[5],
#             'recommendation_score': row[6],
#         }
#         for row in rows
#     ]

# # 🧪 Streamlit interface
# st.title("🛍️ Smart Product Recommendations")

# customer_id = st.text_input("Enter Customer ID:", "C1000")

# if st.button("Get Recommendations"):
#     with st.spinner("Fetching personalized recommendations..."):
#         recommendations = get_recommendations(customer_id)

#         if not recommendations:
#             st.warning("No recommendations found.")
#         else:
#             product_details = fetch_product_details(recommendations)

#             st.success(f"Top {len(product_details)} Recommendations for Customer {customer_id}")
#             for product in product_details:
#                 st.markdown(f"""
#                 **🆔 Product ID:** {product['id']}  
#                 🏷️ **Category:** {product['category']} → {product['subcategory']}  
#                 💰 **Price:** ₹{product['price']}  
#                 🏢 **Brand:** {product['brand']}  
#                 ⭐ **Rating:** {product['rating']}  
#                 🎯 **Recommendation Score:** {product['recommendation_score']:.2f}
#                 ---
#                 """)

import streamlit as st
import sqlite3
import os
import sys

# Add the 'models' directory to the Python path
models_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'models'))
if models_path not in sys.path:
    sys.path.append(models_path)

# 💡 Import recommendation + segment logic
from multi_agent import get_recommendations
from multi_agent import get_customer_segment


# DB path
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'database', 'demo_ecommerce.db'))

# Fetch product info for display
def fetch_product_details(product_ids):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    placeholders = ','.join(['?'] * len(product_ids))
    query = f"""
        SELECT Product_ID, Category, Subcategory, Price, Brand, Product_Rating, Probability_of_Recommendation
        FROM products
        WHERE Product_ID IN ({placeholders})
    """
    cursor.execute(query, product_ids)
    rows = cursor.fetchall()
    conn.close()

    return [
        {
            'id': row[0],
            'category': row[1],
            'subcategory': row[2],
            'price': row[3],
            'brand': row[4],
            'rating': row[5],
            'recommendation_score': row[6],
        }
        for row in rows
    ]

# 🧪 Streamlit UI
st.title("🛍️ Smart Product Recommendations")

customer_id = st.text_input("Enter Customer ID:", "C1000")

if st.button("Get Recommendations"):
    with st.spinner("Analyzing profile..."):
        # Get segment info
        segment = get_customer_segment(customer_id)
        st.info(f"🧑‍💼 Detected Customer Segment: **{segment}**")

        # Get recommendations
        recommendations = get_recommendations(customer_id)

        if not recommendations:
            st.warning("No recommendations found.")
        else:
            product_details = fetch_product_details(recommendations)

            st.success(f"Top {len(product_details)} Recommendations for Customer {customer_id}")
            for product in product_details:
                st.markdown(f"""
                **🆔 Product ID:** {product['id']}  
                🏷️ **Category:** {product['category']} → {product['subcategory']}  
                💰 **Price:** ₹{product['price']}  
                🏢 **Brand:** {product['brand']}  
                ⭐ **Rating:** {product['rating']}  
                🎯 **Recommendation Score:** {product['recommendation_score']:.2f}
                ---
                """)
