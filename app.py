import streamlit as st
# Create an empty transaction list
if "transactions" not in st.session_state:
    st.session_state.transactions = []

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

for transaction in st.session_state.transactions:
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

    transaction = {
        "Type": transaction_type,
        "Category": category,
        "Amount": amount,
        "Description": description
    }

    st.session_state.transactions.append(transaction)

    st.rerun()

    # Display transaction history
st.header("Transaction History")

if st.session_state.transactions:
    st.dataframe(
        st.session_state.transactions,
        use_container_width=True
    )
else:
    st.info("No transactions yet. Add your first transaction!")