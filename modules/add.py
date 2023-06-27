import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import os
import yfinance as yf
import time

date=time.strftime("%Y-%m-%d")

def AddStock():
    st.title("Add Stocks")

    name = st.text_input("Enter the name of the stock: ")
    tk_name = st.text_input("Enter Ticker Name of stock")
    tk_name = tk_name.upper()
    price = st.number_input("Enter the price at which you buy the stock: ")
    price=round(price,2)
    quanty = int(st.number_input("Quantity of the stock: "))
    tc = int(price * quanty)
    
    if not tk_name:
        st.warning("Please enter a valid ticker symbol")
        return
    
    cureent_value = yf.download(tk_name, period='1d')

    
    cv = cureent_value['Close'].iloc[-1]
    current_total=cv*quanty

    if(current_total>tc):
        status="Profit"
    elif(current_total<tc):
        status="Loss"
    else:
        status="No change"
    df = pd.DataFrame([[name,tk_name, price, quanty, tc, cv,current_total,status]])
    df.columns = ['Stock Name','Ticker Name', 'Price', 'Quantity', 'Total Cost', 'Current Value','Total Current Value','status']
    
    if st.button("Submit"):
        if os.path.isfile('port.csv'):
            df.to_csv("port.csv", mode="a", index=False, header=False)
        else:
            df.to_csv("port.csv", mode="a", index=False, header=True)
        st.text("Thank you for choosing our product")
        st.success("The data is entered in the file")
