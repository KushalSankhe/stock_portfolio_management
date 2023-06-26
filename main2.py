import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import csv
import os
import sys
import yfinance as yf
import time

date=time.strftime("%Y-%m-%d")




st.title("Stock Portfolio Management")

with st.sidebar:
    selected = option_menu("Main Menu", ["Your Portfolio", 'Add Stocks','Remove Entries','history'], 
        icons=['person-circle','database-add', 'database-dash'], menu_icon="cast", default_index=0)
    selected

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
    #     st.table(df)
    # except FileNotFoundError:
    #     st.warning("File not found")
            
    
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
    
    cureent_value = yf.download(tk_name, start=date)
    
    # if cureent_value.empty:
    #     st.warning(f"No data found for ticker symbol {tk_name}")
    #     return
    
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


# def RemoveEntry():
#     st.title("Remove Stocks from different Portfolio")

#     name=st.text_input("Enter the name of the stock You want to remove: ")
#     if(st.button("Submit")):
#         with open('port.csv','r')as source:
#             reader=csv.reader(source)
#         with open('port.csv','w')as result:
#             writer=csv.writer(result)
#             for i in reader:
#                 writer.writerow((reader[i]==name))

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

def history():
    try:
        with open('history.csv','r')as f:
            reader=csv.reader(f)
            lines=list(reader)
        st.table(lines)
    except FileNotFoundError:
        st.warning("No history present")
         
        
    


if (selected=="Add Stocks"):
    AddStock()
elif(selected=="Remove Entries"):
    RemoveEntry()
elif(selected=="history"):
    history()
else:
    Home()