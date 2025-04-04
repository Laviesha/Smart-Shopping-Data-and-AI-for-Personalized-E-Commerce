import sqlite3
import ollama

import json
def generate_embedding(text):
    """Generate an embedding for a given text using Ollama's nomic-embed model."""
    response = ollama.embeddings(model='all-minilm', prompt=text)  # Use installed model

    return response['embedding']

def store_embeddings():
    """Fetch product data, generate embeddings, and store in DB."""
    conn = sqlite3.connect('../database/ecommerce.db')
    cursor = conn.cursor()

    # Fetch product details
    cursor.execute("SELECT Product_ID, Category, Brand FROM products")
    products = cursor.fetchall()

    # Ensure product_embeddings table exists
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS product_embeddings (
        product_id TEXT PRIMARY KEY,
        name TEXT,
        description TEXT,
        embedding BLOB
    )
    ''')

    # Process each product
    for product_id, category, brand in products:
        text_data = f"{category} {brand}"  # Combine category & brand
        embedding = generate_embedding(text_data)
        # embedding_blob = pickle.dumps(embedding)  # Convert list to binary
        embedding_blob = json.dumps(embedding)  # ✅ Correct for TEXT format


        # Store in DB
        cursor.execute("INSERT OR REPLACE INTO product_embeddings (product_id, name, description, embedding) VALUES (?, ?, ?, ?)",
                       (product_id, category, text_data, embedding_blob))

    conn.commit()
    conn.close()
    print("✅ Embeddings stored successfully!")

if __name__ == "__main__":
    store_embeddings()
