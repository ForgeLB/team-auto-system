import sqlite3

def fetch_deals():
    # Connect to the database
    conn = sqlite3.connect('sales_pipeline.db')
    cursor = conn.cursor()

    # Query all deals
    cursor.execute('SELECT * FROM deals')
    deals = cursor.fetchall()

    # Close the connection
    conn.close()

    return deals

# Example usage
deals = fetch_deals()
for deal in deals:
    print(deal)
