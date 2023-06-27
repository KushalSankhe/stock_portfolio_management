import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import yfinance as yf
def Home():
    try:
        df = pd.read_csv('port.csv')
        if df.empty:
            st.warning("No data in file")
            return
        for i, row in df.iterrows():
            tk_name = row['Ticker Name']
            cureent_value = yf.download(tk_name, period='1d')['Close'].iloc[-1]
            cureent_value=round(cureent_value,2)
            
            df.at[i, 'Current Value'] = cureent_value

            df.at[i, 'Total Current Value'] = round(cureent_value * row['Quantity'], 2)

            df.at[i, 'Profit/Loss'] = round(df.at[i, 'Total Current Value'] - row['Total Cost'], 2)
        df['Price'] = df['Price'].apply(lambda x: round(x, 2))
        df['Total Cost'] = df['Total Cost'].apply(lambda x: round(x, 2))
        st.table(df.style.applymap(lambda x: 'background-color: %s' % ('green' if x > 0 else 'red'), subset=['Profit/Loss']))
    except FileNotFoundError:
        st.warning("File not found")