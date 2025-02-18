import sqlite3

# Connect to the database
conn = sqlite3.connect('affiliate_data.db')

# Fetch all records from affiliates
rows = conn.execute("SELECT * FROM affiliates").fetchall()

# Print the data
if rows:
    for row in rows:
        print(row)
else:
    print("No data found in affiliates table.")

conn.close()
