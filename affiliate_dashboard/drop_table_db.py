import sqlite3

db_name =  'affiliate_data.db'
table_name = 'sales'

def drop_table(db_name, table_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
    conn.commit()
    conn.close()

# Example usage
drop_table(db_name, table_name)
