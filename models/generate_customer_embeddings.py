import sqlite3
import ollama
import json

def generate_embedding(text):
    if not text.strip():  # Handle empty or whitespace-only text
        return None
    response = ollama.embeddings(model='all-minilm', prompt=text)
    return response['embedding']  # JSON-compatible list

def store_customer_embeddings():
    conn = sqlite3.connect(r'C:\Users\m5cd2\Music\Smart-Shopping-Data-and-AI-for-Personalized-E-Commerce\database\ecommerce.db')
    cursor = conn.cursor()

    # ✅ Ensure customer_embeddings table exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customer_embeddings (
            customer_id TEXT PRIMARY KEY,
            embedding TEXT NOT NULL,  -- Embedding stored as JSON
            FOREIGN KEY (customer_id) REFERENCES customers(Customer_ID) ON DELETE CASCADE
        )
    ''')

    # ✅ Fetch customer browsing and purchase history
    cursor.execute("SELECT Customer_ID, Browsing_History, Purchase_History FROM customers")
    customers = cursor.fetchall()

    for customer_id, browsing, purchase in customers:
        text_data = f"{browsing or ''} {purchase or ''}".strip()
        embedding = generate_embedding(text_data)
        
        if embedding is not None:
            embedding_json = json.dumps(embedding)
            cursor.execute('''
                INSERT INTO customer_embeddings (customer_id, embedding)
                VALUES (?, ?)
                ON CONFLICT(customer_id) DO UPDATE SET embedding=excluded.embedding
            ''', (customer_id, embedding_json))

    conn.commit()
    conn.close()
    print("✅ Customer embeddings stored successfully in JSON format!")

if __name__ == "__main__":
    store_customer_embeddings()
