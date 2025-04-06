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

# 🚨 Better to use real product search keywords, not just IDs
query = input("\nEnter a product search (e.g., 'wireless headphones'): ").strip()

# Generate embedding for search query
query_embedding = get_embedding(query)

# ✅ Match your table schema
cursor.execute("SELECT product_id, category, subcategory, brand, embedding FROM product_embeddings")
products = cursor.fetchall()

# Compute similarity scores
similarities = []
for product_id, category, subcategory, brand, embedding in products:
    if isinstance(embedding, bytes):
        embedding = embedding.decode('utf-8')

    product_embedding = json.loads(embedding)
    similarity = cosine_similarity(query_embedding, product_embedding)

    # ✅ Fallback for missing subcategory
    product_title = f"{brand} - {category} > {subcategory or 'General'}"

    similarities.append((product_id, product_title, similarity))

# Sort and show top 5 recommendations
similarities.sort(key=lambda x: x[2], reverse=True)

print("\n🔍 Top Recommended Products:")
for product_id, title, sim in similarities[:5]:
    print(f"📌 {title} ({product_id}) [Similarity: {sim:.3f}]")

conn.close()
