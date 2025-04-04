import sqlite3

def check_database():
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect('ecommerce.db')
        cursor = conn.cursor()

        # Check if the connection is successful
        print("Database connected successfully.")

        # Query to get the list of tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        # Print the list of tables
        if tables:
            print("Tables in the database:")
            for table in tables:
                print(table[0])  # Print table name
        else:
            print("No tables found in the database.")

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the connection
        if conn:
            conn.close()

if __name__ == "__main__":
    check_database()