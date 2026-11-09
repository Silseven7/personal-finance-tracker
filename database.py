import sqlite3

# Connect to our database
def connect_db():
    return sqlite3.connect("finance.db")


# Create the transactions table
def create_table():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            description TEXT
        )
    """)

    conn.commit()
    conn.close()

    # Save a new transaction to the database
def add_transaction(transaction_type, category, amount, description):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO transactions (type, category, amount, description)
        VALUES (?, ?, ?, ?)
    """, (transaction_type, category, amount, description))

    conn.commit()
    conn.close()

    # Retrieve all transactions from the database
def get_transactions():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, type, category, amount, description
        FROM transactions
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    transactions = []

    for row in rows:
        transactions.append({
            "ID": row[0],
            "Type": row[1],
            "Category": row[2],
            "Amount": row[3],
            "Description": row[4]
        })

    return transactions


    # Delete a transaction using its ID
def delete_transaction(transaction_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM transactions WHERE id = ?",
        (transaction_id,)
    )

    conn.commit()
    conn.close()