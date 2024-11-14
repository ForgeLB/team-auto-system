import sqlite3

# Connect to the database (or create it if it doesn't exist)
conn = sqlite3.connect('sales_pipeline.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Create a table for deals
cursor.execute('''
CREATE TABLE IF NOT EXISTS deals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    value REAL NOT NULL,
    currency TEXT NOT NULL,
    status TEXT NOT NULL,
    contact_name TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database and table created successfully!")
