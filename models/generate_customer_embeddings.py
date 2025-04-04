import sqlite3
import ollama
import numpy as np
import json

def generate_embedding(text):
    if not text:  # Handle empty text case
        return None
    response = ollama.embeddings(model='all-minilm', prompt=text)
    return response['embedding']  # Direct JSON-compatible list

def store_customer_embeddings():
    conn = sqlite3.connect(r'C:\Users\m5cd2\Music\Smart-Shopping-Data-and-AI-for-Personalized-E-Commerce\database\ecommerce.db')
    cursor = conn.cursor()

    cursor.execute("SELECT Customer_ID, Browsing_History, Purchase_History FROM customers")
    customers = cursor.fetchall()

    for customer_id, browsing, purchase in customers:
        text_data = f"{browsing} {purchase}" if browsing and purchase else browsing or purchase
        embedding = generate_embedding(text_data)
        
        if embedding is not None:
            embedding_json = json.dumps(embedding)  # Convert list to JSON string
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
