import sqlite3
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Connect to the SQLite database
conn = sqlite3.connect('gazedata.db')

# Get distinct headers
headers = conn.execute('SELECT DISTINCT header FROM GazeData').fetchall()
headers = [header[0] for header in headers]

# Streamlit UI to select header
selected_header = st.selectbox('Select Header', headers)

# Query data for the selected header, ordered by ID
query = f"SELECT docX, docY FROM GazeData WHERE header = '{selected_header}' AND state = 0 ORDER BY id"
data = pd.read_sql_query(query, conn)
conn.close()

# Check if data is available
if not data.empty:
    # Plot the data using matplotlib
    fig, ax = plt.subplots()
    ax.scatter(data['docX'], data['docY'])
    ax.set_xlabel('Gaze X in Document Coordinates')
    ax.set_ylabel('Gaze Y in Document Coordinates')
    ax.set_title(f'Gaze Data Scatter Plot for Header: {selected_header}')

    # Display the plot in Streamlit
    st.pyplot(fig)
else:
    st.write(f"No valid gaze data found for header: {selected_header}")

