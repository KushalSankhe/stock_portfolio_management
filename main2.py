import streamlit as st
from streamlit_option_menu import option_menu
import time
from modules import home,add,remove,history

date=time.strftime("%Y-%m-%d")


st.title("Stock Portfolio Management")

with st.sidebar:
    selected = option_menu("Main Menu", ["Your Portfolio", 'Add Stocks','Remove Entries','history'], 
        icons=['person-circle','database-add', 'database-dash'], menu_icon="cast", default_index=0)
    selected


if (selected=="Add Stocks"):
    add.AddStock()
elif(selected=="Remove Entries"):
    remove.RemoveEntry()
elif(selected=="history"):
    history.History()
else:
    home.Home()