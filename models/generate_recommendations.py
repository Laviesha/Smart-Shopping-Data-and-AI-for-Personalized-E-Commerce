
# import sqlite3
# import json
# import numpy as np
# from scipy.spatial.distance import cdist
# from concurrent.futures import ProcessPoolExecutor

# # Function to compute cosine similarity
# def cosine_similarity_matrix(customer_embeddings, product_embeddings):
#     return 1 - cdist(customer_embeddings, product_embeddings, metric="cosine")

# # Function to process a batch of customers
# def process_batch(customer_batch, product_ids, product_embeddings):
#     batch_recommendations = []
#     customer_embeddings = np.array([json.loads(cust[1]) for cust in customer_batch])

#     # Compute cosine similarity for the batch
#     similarity_matrix = cosine_similarity_matrix(customer_embeddings, product_embeddings)

#     for idx, (customer_id, _) in enumerate(customer_batch):
#         # Sort products by similarity score (descending order)
#         top_products = np.argsort(-similarity_matrix[idx])[:5]
#         recommended_products = [product_ids[i] for i in top_products]

#         # Store recommendations
#         for product_id in recommended_products:
#             batch_recommendations.append((customer_id, product_id))

#     return batch_recommendations

# # Main function to generate recommendations
# def generate_recommendations():
#     # conn = sqlite3.connect("database/ecommerce.db")
#     conn = sqlite3.connect("../database/ecommerce.db")

#     cursor = conn.cursor()

#     # Fetch all customer embeddings
#     cursor.execute("SELECT customer_id, embedding FROM customer_embeddings")
#     customers = cursor.fetchall()

#     # Fetch all product embeddings
#     cursor.execute("SELECT product_id, embedding FROM product_embeddings")
#     products = cursor.fetchall()

#     # Extract product embeddings as a NumPy array
#     product_ids = [prod[0] for prod in products]
#     product_embeddings = np.array([json.loads(prod[1]) for prod in products])

#     # Split customers into batches of 100
#     batch_size = 100
#     customer_batches = [customers[i : i + batch_size] for i in range(0, len(customers), batch_size)]

#     recommendations = []

#     # Use multiprocessing to process batches in parallel
#     with ProcessPoolExecutor() as executor:
#         results = executor.map(process_batch, customer_batches, [product_ids] * len(customer_batches), [product_embeddings] * len(customer_batches))

#         for result in results:
#             recommendations.extend(result)

#     # Insert recommendations into database in bulk
#     cursor.executemany("INSERT INTO recommendations (Customer_ID, Product_ID) VALUES (?, ?)", recommendations)

#     conn.commit()
#     conn.close()

#     # Save recommendations to JSON
#     with open("recommendations.json", "w") as json_file:
#         json.dump(
#     {
#         cust_id: [prod for c_id, prod in recommendations if c_id == cust_id]
#         for cust_id, _ in customers
#     },
#     json_file,
#     indent=4
# )


#     print("✅ Recommendations generated successfully and saved in 'recommendations.json'!")

# if __name__ == "__main__":
#     generate_recommendations()


# import sqlite3
# import json
# import numpy as np
# from scipy.spatial.distance import cdist
# from concurrent.futures import ProcessPoolExecutor

# # Function to compute cosine similarity
# def cosine_similarity_matrix(customer_embeddings, product_embeddings):
#     return 1 - cdist(customer_embeddings, product_embeddings, metric="cosine")

# # Function to process a batch of customers
# def process_batch(customer_batch, product_ids, product_embeddings):
#     batch_recommendations = []
#     customer_embeddings = np.array([json.loads(cust[1]) for cust in customer_batch])

#     # Compute cosine similarity for the batch
#     similarity_matrix = cosine_similarity_matrix(customer_embeddings, product_embeddings)

#     for idx, (customer_id, _) in enumerate(customer_batch):
#         # Sort products by similarity score (descending order)
#         top_products = np.argsort(-similarity_matrix[idx])[:5]
#         recommended_products = [product_ids[i] for i in top_products]

#         # Store customer and their top 5 recommended product IDs as a JSON string
#         batch_recommendations.append((customer_id, json.dumps(recommended_products)))

#     return batch_recommendations

# # Main function to generate recommendations
# def generate_recommendations():
#     # Connect to DB
#     conn = sqlite3.connect("../database/ecommerce.db")
#     cursor = conn.cursor()

#     # Fetch all customer embeddings
#     cursor.execute("SELECT customer_id, embedding FROM customer_embeddings")
#     customers = cursor.fetchall()

#     # Fetch all product embeddings
#     cursor.execute("SELECT product_id, embedding FROM product_embeddings")
#     products = cursor.fetchall()

#     # Extract product data
#     product_ids = [prod[0] for prod in products]
#     product_embeddings = np.array([json.loads(prod[1]) for prod in products])

#     # Split into batches of 100
#     batch_size = 100
#     customer_batches = [customers[i : i + batch_size] for i in range(0, len(customers), batch_size)]

#     recommendations = []

#     # Use multiprocessing to process batches
#     with ProcessPoolExecutor() as executor:
#         results = executor.map(process_batch, customer_batches, [product_ids] * len(customer_batches), [product_embeddings] * len(customer_batches))

#         for result in results:
#             recommendations.extend(result)

#     # Insert recommendations into database (Customer_ID, recommended_ids)
#     cursor.executemany("INSERT INTO recommendations (Customer_ID, recommended_ids) VALUES (?, ?)", recommendations)

#     conn.commit()
#     conn.close()

#     # Save as JSON
#     with open("recommendations.json", "w") as json_file:
#         json.dump(
#             {cust_id: json.loads(prod_list) for cust_id, prod_list in recommendations},
#             json_file,
#             indent=4
#         )

#     print("✅ Recommendations generated successfully and saved in 'recommendations.json'!")

# if __name__ == "__main__":
#     generate_recommendations()

# import sqlite3
# import json
# import numpy as np
# from scipy.spatial.distance import cdist
# from concurrent.futures import ProcessPoolExecutor

# # Function to compute cosine similarity
# def cosine_similarity_matrix(customer_embeddings, product_embeddings):
#     return 1 - cdist(customer_embeddings, product_embeddings, metric="cosine")

# # Function to process a batch of customers
# def process_batch(customer_batch, product_ids, product_embeddings):
#     batch_recommendations = []
#     all_json_output = {}

#     customer_embeddings = np.array([json.loads(cust[1]) for cust in customer_batch])
#     similarity_matrix = cosine_similarity_matrix(customer_embeddings, product_embeddings)

#     for idx, (customer_id, _) in enumerate(customer_batch):
#         top_products_idx = np.argsort(-similarity_matrix[idx])[:5]
#         recommended_products = [product_ids[i] for i in top_products_idx]

#         # For each recommended product, insert as a separate row
#         for product_id in recommended_products:
#             batch_recommendations.append((customer_id, product_id, json.dumps(recommended_products)))

#         # Optional: Save full recommendations per customer
#         all_json_output[customer_id] = recommended_products

#     return batch_recommendations, all_json_output

# def generate_recommendations():
#     conn = sqlite3.connect("../database/ecommerce.db")
#     cursor = conn.cursor()

#     # Optional: Clear existing recommendations
#     cursor.execute("DELETE FROM recommendations")

#     cursor.execute("SELECT customer_id, embedding FROM customer_embeddings")
#     customers = cursor.fetchall()

#     cursor.execute("SELECT product_id, embedding FROM product_embeddings")
#     products = cursor.fetchall()

#     product_ids = [prod[0] for prod in products]
#     product_embeddings = np.array([json.loads(prod[1]) for prod in products])

#     batch_size = 100
#     customer_batches = [customers[i:i+batch_size] for i in range(0, len(customers), batch_size)]

#     all_recommendations = []
#     final_json_output = {}

#     with ProcessPoolExecutor() as executor:
#         results = executor.map(process_batch, customer_batches, [product_ids]*len(customer_batches), [product_embeddings]*len(customer_batches))

#         for recs, json_output in results:
#             all_recommendations.extend(recs)
#             final_json_output.update(json_output)

#     # Insert flattened recommendations into table
#     cursor.executemany("INSERT INTO recommendations (Customer_ID, Product_ID, recommended_ids) VALUES (?, ?, ?)", all_recommendations)

#     conn.commit()
#     conn.close()

#     # Save full recommendations to JSON
#     with open("recommendations.json", "w") as f:
#         json.dump(final_json_output, f, indent=4)

#     print("✅ Recommendations inserted into database and saved to 'recommendations.json'.")

# if __name__ == "__main__":
#     generate_recommendations()


import sqlite3
import json
import numpy as np
from scipy.spatial.distance import cdist
from concurrent.futures import ProcessPoolExecutor

# Sample static list of popular product IDs (you can generate dynamically from ratings/sales)
popular_product_ids = ["P001", "P002", "P003", "P004", "P005"]

# Function to compute cosine similarity
def cosine_similarity_matrix(customer_embeddings, product_embeddings):
    return 1 - cdist(customer_embeddings, product_embeddings, metric="cosine")

# Function to process a batch of customers
def process_batch(customer_batch, product_ids, product_embeddings):
    batch_recommendations = []
    customer_embeddings = np.array([json.loads(cust[1]) for cust in customer_batch])

    # Compute cosine similarity for the batch
    similarity_matrix = cosine_similarity_matrix(customer_embeddings, product_embeddings)

    for idx, (customer_id, embedding_str, segment) in enumerate(customer_batch):
        if segment.lower() == "frequent_buyer":
            # Recommend top 5 similar products
            top_products = np.argsort(-similarity_matrix[idx])[:5]
            recommended_products = [product_ids[i] for i in top_products]
        elif segment.lower() == "new_visitor":
            # Recommend popular products
            recommended_products = popular_product_ids[:5]
        else:
            # Default fallback: similarity-based
            top_products = np.argsort(-similarity_matrix[idx])[:5]
            recommended_products = [product_ids[i] for i in top_products]

        batch_recommendations.append((customer_id, json.dumps(recommended_products), segment))

    return batch_recommendations

# Main function
def generate_recommendations():
    conn = sqlite3.connect("../database/ecommerce.db")
    cursor = conn.cursor()

   
    cursor.execute('''
        SELECT ce.customer_id, ce.embedding, cu.Customer_Segment
        FROM customer_embeddings ce
        JOIN customers cu ON ce.customer_id = cu.Customer_ID
    ''')

    customers = cursor.fetchall()

    # Fetch product embeddings
    cursor.execute("SELECT product_id, embedding FROM product_embeddings")
    products = cursor.fetchall()

    product_ids = [prod[0] for prod in products]
    product_embeddings = np.array([json.loads(prod[1]) for prod in products])

    # Split into batches
    batch_size = 100
    customer_batches = [customers[i : i + batch_size] for i in range(0, len(customers), batch_size)]

    recommendations = []

    # Use multiprocessing
    with ProcessPoolExecutor() as executor:
        results = executor.map(process_batch, customer_batches, [product_ids] * len(customer_batches), [product_embeddings] * len(customer_batches))
        for result in results:
            recommendations.extend(result)

    # Save to database
    cursor.executemany(
        "INSERT INTO recommendations (Customer_ID, recommended_ids, Customer_Segment) VALUES (?, ?, ?)",
        recommendations
    )

    conn.commit()
    conn.close()

    # Save to JSON
    with open("recommendations.json", "w") as json_file:
        json.dump({cust_id: json.loads(prod_list) for cust_id, prod_list, _ in recommendations}, json_file, indent=4)

    print("✅ Recommendations generated with segment-based logic and saved!")

if __name__ == "__main__":
    generate_recommendations()
