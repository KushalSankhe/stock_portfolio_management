import streamlit as st
import pandas as pd
import os
import yfinance as yf
import time

date = time.strftime("%Y-%m-%d")

def AddStock():
    st.title("Add Stocks")

    name = st.text_input("Enter the name of the stock: ")
    tk_name = st.text_input("Enter Ticker Name of stock")
    tk_name = tk_name.upper()
    price = st.number_input("Enter the price at which you buy the stock: ")
    price = round(price, 2)
    quantity = int(st.number_input("Quantity of the stock: "))
    total_cost = int(price * quantity)

    if not tk_name:
        st.warning("Please enter a valid ticker symbol")
        return

    current_value = yf.download(tk_name, period='1d')
    current_price = current_value['Close'].iloc[-1]
    current_total = current_price * quantity

    if current_total > total_cost:
        status = "Profit"
    elif current_total < total_cost:
        status = "Loss"
    else:
        status = "No change"

    # Load existing data from file if it exists
    if os.path.isfile('port.csv'):
        data = pd.read_csv('port.csv')
        last_id = data['ID'].max() if 'ID' in data.columns else 0
        next_id = last_id + 1
    else:
        next_id = 1

    df = pd.DataFrame(
        [[next_id, name, tk_name, price, quantity, total_cost, current_price, current_total, status]],
        columns=['ID', 'Stock Name', 'Ticker Name', 'Price', 'Quantity', 'Total Cost', 'Current Price',
                 'Current Total', 'Status']
    )

    if st.button("Submit"):
        if os.path.isfile('port.csv'):
            df.to_csv("port.csv", mode="a", index=False, header=False)
        else:
            df.to_csv("port.csv", mode="a", index=False, header=True)
        st.text("Thank you for choosing our product")
        st.success("The data is entered in the file")
