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
