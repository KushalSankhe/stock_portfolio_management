import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import csv
import os
import sys

sys.path.insert(1,"c:/users/citiususer/appdata/local/programs/python/python311/lib/site-packages")



st.title("Stock Portfolio Management")

with st.sidebar:
    selected = option_menu("Main Menu", ["Your Portfolio", 'Add Stocks','Remove Entries'], 
        icons=['person-circle','database-add', 'database-dash'], menu_icon="cast", default_index=0)
    selected

def Home():
    # try:
    #     pass
    # except UnboundLocalError:
    #     st.warning("File is empty try adding some data")
    # if UnboundLocalError:
    #     st.warning("File is empty try adding some data")
    # else:
    #     with open('port.csv','r')as f:
    #         a=f.readlines()
    #     st.table(a)
    #     print(a)

    try:
        # with open('port.csv','r')as f:
        #     a=f.readlines()
        # f=['stock name','price','quantity','total price']
        # st.table(a)
        # print(a)
        with open('port.csv', 'r') as f:
            reader = csv.reader(f)
            lines=list(reader)
        st.table(lines)
    except UnboundLocalError:
        st.warning("File is empty")
    except FileNotFoundError:
        st.warning("File is not there")
            
    
def AddStock():
    st.title("Add Stocks")

    name=st.text_input("Enter the name of the stock: ")
    price=int(st.number_input("Enter the price at which you buy the stock: "))
    quanty=int(st.number_input("Quantity of the stock: "))
    tc=int(price*quanty)
    # df=pd.DataFrame([[name,price,quanty,tc]],columns=["Stock Name","Price","Quantity","Total Cost"])
    df=pd.DataFrame([[name,price,quanty,tc]])
    df.columns=['Stock Name','Price','Quantity', 'Total Cost']
    if(st.button("Submit")):
        if os.path.isfile('port.csv'):
            df.to_csv("port.csv", mode="a", index=False, header=False)
        else:
            df.to_csv("port.csv", mode="a", index=False, header=True)
        # df.to_csv("port.csv",mode="a",index=False, header=True)
        st.text("Thank you for chosing our product")
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
        st.success(f"{name} has been removed from the file.")

if (selected=="Add Stocks"):
    AddStock()
elif(selected=="Remove Entries"):
    RemoveEntry()
else:
    Home()