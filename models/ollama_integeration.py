# import requests
# import json

# OLLAMA_URL = "http://127.0.0.1:11434/api/embeddings"
# MODEL_NAME = "all-minilm"

# def get_embedding(text):
#     payload = {
#         "model": MODEL_NAME,
#         "prompt": text
#     }
#     response = requests.post(OLLAMA_URL, json=payload)
    
#     if response.status_code == 200:
#         return response.json().get("embedding", [])
#     else:
#         print(f"Error: {response.status_code}, {response.text}")
#         return None

# if __name__ == "__main__":
#     text = "Hello, how are you?"
#     embedding = get_embedding(text)
    
#     if embedding:
#         print(f"Embedding vector (length {len(embedding)}): {embedding[:5]}...")  # Display first 5 values

import ollama
import sqlite3
import json

# Connect to SQLite
conn = sqlite3.connect('recommendation.db')
cursor = conn.cursor()

# Create a table to store embeddings
cursor.execute('''
    CREATE TABLE IF NOT EXISTS product_embeddings (
        product_id TEXT PRIMARY KEY,
        name TEXT,
        description TEXT,
        embedding TEXT
    )
''')

# Example product descriptions
products = [
    ("P1", "Running Shoes", "Comfortable running shoes for sports"),
    ("P2", "Wireless Headphones", "Noise-canceling Bluetooth headphones"),
]

# Generate embeddings & store them
for product_id, name, desc in products:
    response = ollama.embeddings(model="all-minilm", prompt=desc)
    embedding_vector = json.dumps(response['embedding'])  # Store as JSON string

    cursor.execute("INSERT INTO product_embeddings VALUES (?, ?, ?, ?)", (product_id, name, desc, embedding_vector))

conn.commit()
conn.close()

print("✅ Embeddings saved successfully!")
