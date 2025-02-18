import sqlite3

# Database file path (will create 'affiliate_data.db' in the current directory)
DB_PATH = 'affiliate_data.db'

# Connect to SQLite (creates the database file if it doesn't exist)
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# # Create Affiliates table (with an added email column)
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS affiliates (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     name TEXT NOT NULL,
#     referral_id TEXT NOT NULL UNIQUE,
#     email TEXT NOT NULL,
#     pwd TEXT NOT NULL
# )
# """)

# # Create Sales table
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS sales (
    # id INTEGER PRIMARY KEY AUTOINCREMENT,
    # product_name TEXT NOT NULL,
    # referral_id INTEGER NOT NULL,
    # commission REAL NOT NULL,
    # sale_date TEXT NOT NULL,
    # FOREIGN KEY (referral_id) REFERENCES affiliates (referral_id)
# )
# """)

# # Create Clicks table
# cursor.execute("""
# CREATE TABLE clicks (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     referral_id TEXT NOT NULL,
#     click_time TEXT NOT NULL
# )
# """)


# cursor.execute("""
# CREATE TABLE customers (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     full_name TEXT NOT NULL,
#     mobile_number TEXT,
#     timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
# )
# """)


# conn.execute("""
#     INSERT INTO affiliates (referral_id, name, email, pwd)
#     VALUES ('demo02', 'Soham S', 'ss@example.com', '123')
# """)


# conn.execute("""
#     INSERT INTO sales (product_name, referral_id, commission, sale_date, customer_name)
#     VALUES ('dentowin', 'demo02', '30', '30/12/2024, 23:19:02 ', 'heyo moto')
# """)


# conn.execute("""
#     ALTER TABLE sales ADD COLUMN customer_name TEXT;
# """)



# Commit and close the connection
conn.commit()
conn.close()

print("Database and tables created successfully!")
