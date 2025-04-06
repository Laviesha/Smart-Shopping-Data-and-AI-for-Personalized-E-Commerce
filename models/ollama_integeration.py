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
