import sqlite3

def insert_deal(title, value, currency, status, contact_name):
    # Connect to the database
    conn = sqlite3.connect('sales_pipeline.db')
    cursor = conn.cursor()

    # Insert a new deal into the deals table
    cursor.execute('''
    INSERT INTO deals (title, value, currency, status, contact_name)
    VALUES (?, ?, ?, ?, ?)
    ''', (title, value, currency, status, contact_name))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()
    print("New deal inserted successfully!")

# Example usage
insert_deal("The Yes Center Deal", 1500, "SAR", "open", "Azuz")
