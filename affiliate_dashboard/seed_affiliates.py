# ALTER TABLE affiliates ADD COLUMN pwd TEXT NOT NULL;


import sqlite3

# Connect to the database
conn = sqlite3.connect('affiliate_data.db')

# Create the affiliates table if it doesn't exist
conn.execute("""
    CREATE TABLE IF NOT EXISTS affiliates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        referral_id TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        pwd TEXT NOT NULL
    )
""")

# Insert a default affiliate
try:
    conn.execute("""
        INSERT INTO affiliates (referral_id, name, email, pwd)
        VALUES ('THW5872', 'John Doe', 'john@example.com', 'pwd5872')
    """)
    print("Default affiliate added successfully!")
except sqlite3.IntegrityError:
    print("Affiliate with referral_id 'test123' already exists.")

# Commit and close the connection
conn.commit()
conn.close()
