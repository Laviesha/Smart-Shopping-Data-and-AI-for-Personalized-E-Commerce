
# import sqlite3

# def get_customer_data(customer_id):
#     """Fetch customer data from the database."""
#     print("Connecting to database...")
#     conn = sqlite3.connect(r'C:\Users\m5cd2\Music\Smart-Shopping-Data-and-AI-for-Personalized-E-Commerce\database\ecommerce.db')
#     print("Connected to database.")
#     cursor = conn.cursor()
#     print("Executing query to fetch customer data...")
    
#     cursor.execute("SELECT * FROM customers WHERE Customer_ID = ?", (customer_id,))
#     customer_data = cursor.fetchone()
    
#     conn.close()
#     return customer_data

# def get_product_recommendations(customer_id):
#     """Generate product recommendations for a customer."""
#     # This is a placeholder for your recommendation logic
#     # You can implement your recommendation algorithm here
#     recommendations = []
    
#     # Example: Fetch products based on some criteria
#     conn = sqlite3.connect(r'C:\Users\m5cd2\Music\Smart-Shopping-Data-and-AI-for-Personalized-E-Commerce\database\ecommerce.db')
#     cursor = conn.cursor()
    
#     cursor.execute("SELECT * FROM products")  # Modify this query based on your logic
#     products = cursor.fetchall()
    
#     # Simple logic to recommend all products (replace with actual logic)
#     for product in products:
#         recommendations.append(product)
    
#     conn.close()
#     return recommendations

# if __name__ == "__main__":
#     # Example usage
#     customer_id = 'C1000'  # Replace with an actual customer ID
#     customer_data = get_customer_data(customer_id)
#     print("Customer Data:", customer_data)
    
#     recommendations = get_product_recommendations(customer_id)
#     print("Product Recommendations:", recommendations)
import sqlite3
def create_sample_data():
    """Create sample data in the database for testing."""
    conn = sqlite3.connect(r'C:\Users\m5cd2\Music\Smart-Shopping-Data-and-AI-for-Personalized-E-Commerce\database\ecommerce.db')
    cursor = conn.cursor()
    
    # Drop the customers table if it exists (optional, use with caution)
    cursor.execute('DROP TABLE IF EXISTS customers')
    
    # Create customers table with the desired schema
    cursor.execute('''
    CREATE TABLE customers (
        Customer_ID TEXT PRIMARY KEY,
        Age INTEGER,
        Gender TEXT,
        Location TEXT,
        Browsing_History TEXT,
        Purchase_History TEXT
    )
    ''')
    
    # Drop the products table if it exists (optional, use with caution)
    cursor.execute('DROP TABLE IF EXISTS products')
    
    # Create products table with the desired schema
    cursor.execute('''
    CREATE TABLE products (
        Product_ID TEXT PRIMARY KEY,
        Category TEXT,
        Price REAL,
        Brand TEXT,
        Average_Rating REAL
    )
    ''')
    
    # Insert sample customer data
    cursor.execute("INSERT OR IGNORE INTO customers (Customer_ID, Age, Gender, Location, Browsing_History, Purchase_History) VALUES ('C001', 30, 'Male', 'New York', 'Product1,Product2', 'Product1')")
    
    # Insert sample product data
    cursor.execute("INSERT OR IGNORE INTO products (Product_ID, Category, Price, Brand, Average_Rating) VALUES ('P001', 'Electronics', 19.99, 'Brand A', 4.5)")
    cursor.execute("INSERT OR IGNORE INTO products (Product_ID, Category, Price, Brand, Average_Rating) VALUES ('P002', 'Home', 29.99, 'Brand B', 4.0)")
    
    conn.commit()
    conn.close()

def get_customer_data(customer_id):
    """Fetch customer data from the database."""
    print("Connecting to database...")
    conn = sqlite3.connect(r'C:\Users\m5cd2\Music\Smart-Shopping-Data-and-AI-for-Personalized-E-Commerce\database\ecommerce.db')
    print("Connected to database.")
    cursor = conn.cursor()
    print("Executing query to fetch customer data...")
    
    cursor.execute("SELECT * FROM customers WHERE Customer_ID = ?", (customer_id,))
    customer_data = cursor.fetchone()
    
    print("Fetched Customer Data:", customer_data)  # Debugging line
    conn.close()
    return customer_data

def get_product_recommendations():
    """Generate product recommendations."""
    recommendations = []
    
    conn = sqlite3.connect(r'C:\Users\m5cd2\Music\Smart-Shopping-Data-and-AI-for-Personalized-E-Commerce\database\ecommerce.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    
    for product in products:
        recommendations.append(product)
    
    print("Fetched Product Recommendations:", recommendations)  # Debugging line
    conn.close()
    return recommendations

if __name__ == "__main__":
    # Create sample data for testing
    create_sample_data()
    
    # Example usage
    customer_id = 'C001'  # Replace with an actual customer ID
    customer_data = get_customer_data(customer_id)
    print("Customer Data:", customer_data)
    
    recommendations = get_product_recommendations()
    print("Product Recommendations:", recommendations)