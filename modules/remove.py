import streamlit as st
import csv
import os

def RemoveEntry():
    st.title("Remove Stocks from different Portfolio")

    entry_id = st.text_input("Enter the unique identifier of the stock entry: ")
    qty = st.number_input("Enter Quantity")
    found = False

    if st.button("Submit"):
        with open('port.csv', 'r') as source:
            reader = csv.reader(source)
            rows = list(reader)

        new_rows = []
        profit_loss = 0
        valid_qty = True

        for row in rows:
            if entry_id == row[0]:
                found = True
                csv_qty = float(row[4])

                if qty > csv_qty:
                    st.warning("The quantity you entered is greater than the quantity available")
                    valid_qty = False
                    new_qty = csv_qty  # Do not subtract any quantity
                else:
                    new_qty = csv_qty - qty  # Subtract the entered quantity

                total_cost = float(row[3]) * new_qty
                total_current_value = float(row[6]) * new_qty
                profit_loss = total_current_value - total_cost

                if new_qty > 0:
                    row[4] = str(new_qty)
                    row[5] = str(total_cost)
                    row[7] = str(total_current_value)
                    new_rows.append(row)
                    name=row[1]
                    st.success(f"Successfullty removed {qty} stocks from {name}")
                    
                else:
                    st.warning(f"Stock entry with ID {entry_id} has been completely removed.")
                    break  # Exit the loop if the stock entry is completely removed
            else:
                new_rows.append(row)

        if found:
            with open('port.csv', 'w', newline='') as result:
                writer = csv.writer(result)
                writer.writerows(new_rows)

            if valid_qty:
                with open('history.csv', 'a') as hw:
                    if os.stat('history.csv').st_size == 0:
                        hw.write("Stock Name,Quantity,Profit/Loss\n")
                    hw.write(f"{name},{qty},{profit_loss}\n")

            if valid_qty and new_qty <= 0:
                st.success(f"Stock entry with ID {entry_id} has been removed from the file.")
        else:
            st.warning(f"Stock entry with ID {entry_id} not found.")

