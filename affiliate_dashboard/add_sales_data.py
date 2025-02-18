import sqlite3

# Database file path
DB_PATH = 'affiliate_data.db'

# Connect to the database
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Add affiliate data
cursor.execute("INSERT INTO affiliates (name, referral_id) VALUES (?, ?)", 
               ('Jane Smith', 'affiliate456'))

# Add sales data
cursor.execute("""
INSERT INTO sales (product_name, affiliate_id, commission, sale_date) 
VALUES (?, ?, ?, ?)
""", 
('Product 2', 2, 50.0, '2024-12-27 15:45'))

# Commit and close the connection
conn.commit()
conn.close()

print("Data added successfully!")
