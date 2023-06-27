import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import csv
import os
import yfinance as yf

def RemoveEntry():
    st.title("Remove Stocks from different Portfolio")

    name = st.text_input("Enter the name of the stock You want to remove: ")
    if st.button("Submit"):
        with open('port.csv', 'r') as source:
            reader = csv.reader(source)
            rows = list(reader)
        with open('port.csv', 'w', newline='') as result:
            writer = csv.writer(result)
            for row in rows:
                if row[0] != name:
                    writer.writerow(row)
                else:
                    profit_loss = row[6] # assuming profit/loss is in column 6
                    with open('history.csv','a')as hw:
                        if os.stat('history.csv').st_size == 0:
                            hw.write("name,Profit/Loss\n")
                        hw.write(f"{name},{profit_loss}\n")
        st.success(f"{name} has been removed from the file.")