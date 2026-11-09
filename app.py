import streamlit as st

from database import create_table, add_transaction, get_transactions, delete_transaction

# Initialize the database
create_table()

# Load saved transactions
transactions = get_transactions()



# Page configuration
st.set_page_config(
    page_title="Personal Finance Tracker",
    page_icon="💰",
    layout="wide"
)

# Application title
st.title("💰 Personal Finance Tracker")

# Description
st.write("Track your income, expenses, and savings in one place.")

# Calculate financial totals
total_income = 0
total_expenses = 0

for transaction in transactions:
    if transaction["Type"] == "Income":
        total_income += transaction["Amount"]
    else:
        total_expenses += transaction["Amount"]

balance = total_income - total_expenses

# Financial overview
st.header("Financial Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Income", f"€{total_income:.2f}")

with col2:
    st.metric("Total Expenses", f"€{total_expenses:.2f}")

with col3:
    st.metric("Balance", f"€{balance:.2f}")

    # Transaction form
st.header("Add New Transaction")

transaction_type = st.selectbox(
    "Transaction Type",
    ["Income", "Expense"]
)

category = st.selectbox(
    "Category",
    ["Salary", "Food", "Transport", "Shopping", "Bills", "Other"]
)

amount = st.number_input(
    "Amount (€)",
    min_value=0.01,
    step=1.0
)

description = st.text_input(
    "Description"
)

if st.button("Add Transaction"):

    add_transaction(
        transaction_type,
        category,
        amount,
        description
    )

    st.rerun()

    # Display transaction history
st.header("Transaction History")

if transactions:
    st.dataframe(
        transactions,
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("No transactions yet. Add your first transaction!")

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


    # Delete a transaction
st.header("Delete Transaction")

if transactions:
    transaction_ids = [transaction["ID"] for transaction in transactions]

    selected_id = st.selectbox(
        "Select Transaction ID",
        transaction_ids
    )

    if st.button("Delete Transaction"):
        delete_transaction(selected_id)
        st.rerun()
else:
    st.info("There are no transactions to delete.")