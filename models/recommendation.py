import ollama
import sqlite3
import json
import numpy as np

# Function to compute cosine similarity
def cosine_similarity(vec1, vec2):
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

# Function to get embedding using Ollama
def get_embedding(text):
    response = ollama.embeddings(model="all-minilm", prompt=text)
    return response["embedding"]

# Connect to SQLite database
conn = sqlite3.connect("../database/ecommerce.db")

cursor = conn.cursor()

# Get user input
query = input("\nEnter a product search: ").strip()

# Generate embedding for search query
query_embedding = get_embedding(query)

# Retrieve stored product embeddings from the database
cursor.execute("SELECT product_id, name, description, embedding FROM product_embeddings")
products = cursor.fetchall()

# Compute similarity scores
similarities = []
for product_id, name, desc, embedding in products:
    # product_embedding = pickle.loads(embedding)  # Convert stored embedding from BLOB
    # product_embedding = pickle.loads(embedding.encode('latin1'))  # Convert stored embedding from str to bytes
    # product_embedding = json.loads(embedding)  # Convert stored JSON string to Python list
    # Instead of pickle.loads(), use json.loads()
    # Ensure embedding is a string before json.loads()
    if isinstance(embedding, bytes):
        embedding = embedding.decode('utf-8')  # Convert bytes to string if needed

    product_embedding = json.loads(embedding)  # ✅ Correct approach





    similarity = cosine_similarity(query_embedding, product_embedding)
    similarities.append((product_id, name, desc, similarity))

# Sort by similarity & display top 5 results
similarities.sort(key=lambda x: x[3], reverse=True)
print("\n🔍 Top Recommended Products:")
for product_id, name, desc, sim in similarities[:5]:
    print(f"📌 {name} ({product_id}) - {desc} [Similarity: {sim:.3f}]")

conn.close()
