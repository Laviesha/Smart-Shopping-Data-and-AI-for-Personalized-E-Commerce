import sqlite3

def create_database():
    # conn = sqlite3.connect('ecommerce.db')
    conn = sqlite3.connect('ecommerce.db')

    cursor = conn.cursor()

    # # Create customers table (already exists)
    # cursor.execute('''
    # CREATE TABLE IF NOT EXISTS customers (
    #     Customer_ID TEXT PRIMARY KEY,
    #     Age INTEGER,
    #     Gender TEXT,
    #     Location TEXT,
    #     Browsing_History TEXT,
    #     Purchase_History TEXT
    # )
    # ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS customers (
        Customer_ID TEXT PRIMARY KEY,
        Age INTEGER,
        Gender TEXT,
        Location TEXT,
        Browsing_History TEXT,
        Purchase_History TEXT,
        Customer_Segment TEXT,
        Avg_Order_Value REAL,
        Holiday TEXT,
        Season TEXT
    )
    ''')


    # Create products table (already exists)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        Product_ID TEXT PRIMARY KEY,
        Category TEXT,
        Subcategory TEXT,
        Price REAL,
        Brand TEXT,
        Average_Rating_of_Similar_Products REAL,
        Product_Rating REAL,
        Customer_Review_Sentiment_Score REAL,
        Holiday TEXT,
        Season TEXT,
        Geographical_Location TEXT,
        Similar_Product_List TEXT,
        Probability_of_Recommendation REAL,
        embedding TEXT
);
    ''')

    # Create product embeddings table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS product_embeddings (
        product_id TEXT PRIMARY KEY,
        category TEXT,
        subcategory TEXT,
        price REAL,
        brand TEXT,
        avg_rating_similar REAL,
        product_rating REAL,
        review_sentiment_score REAL,
        holiday TEXT,
        season TEXT,
        geographical_location TEXT,
        similar_products TEXT,
        probability_of_recommendation REAL,
        embedding TEXT
    )
    ''')

    # Create recommendations table (already exists)
    # cursor.execute('''
    # CREATE TABLE IF NOT EXISTS recommendations (
    #     Recommendation_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    #     Customer_ID TEXT,
    #     Product_ID TEXT,
    #     FOREIGN KEY (Customer_ID) REFERENCES customers(Customer_ID),
    #     FOREIGN KEY (Product_ID) REFERENCES products(Product_ID)
    # )
    # ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS recommendations (
    Recommendation_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Customer_ID TEXT,
    recommended_ids TEXT,
    Customer_Segment TEXT
    )
    ''')


    # # ✅ Update customer_embeddings table to use JSON text
    # cursor.execute('''
    # CREATE TABLE IF NOT EXISTS customer_embeddings (
    #     customer_id TEXT PRIMARY KEY,
    #     embedding TEXT,
    #     FOREIGN KEY (customer_id) REFERENCES customers(Customer_ID)
    # )
    # ''')
    # ✅ Update customer_embeddings table to use JSON text format for embedding
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS customer_embeddings (
        customer_id TEXT PRIMARY KEY,
        embedding TEXT NOT NULL,             -- embedding stored as JSON string
        segment TEXT,                        -- add segment info
        FOREIGN KEY (customer_id) REFERENCES customers(Customer_ID) ON DELETE CASCADE
    )
    ''')


    conn.commit()
    conn.close()
    print("✅ Database and tables created successfully!")

if __name__ == "__main__":
    create_database()

