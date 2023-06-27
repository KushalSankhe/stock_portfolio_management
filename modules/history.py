import streamlit as st
import csv

def History():
    try:
        with open('history.csv','r')as f:
            reader=csv.reader(f)
            lines=list(reader)
        st.table(lines)
    except FileNotFoundError:
        st.warning("No history present")