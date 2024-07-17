# Import libraries
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

SCREEN_WIDTH = 4480
SCREEN_HEIGHT = 2520

# Set up Streamlit app title
st.title("Gaze Data Visualization")

# Increase graph resolution dots per inch
plt.figure(dpi=600)

sns.set(style="whitegrid", color_codes=True)
sns.set(font_scale=1)

# Connect to the SQLite database
conn = sqlite3.connect('gazedata.db')

# Get distinct gaze data types
gaze_data_headers = conn.execute('SELECT DISTINCT header FROM GazeData ORDER BY header DESC').fetchall()
gaze_data_headers = [data[0] for data in gaze_data_headers]

# Streamlit UI for selecting gaze data
selected_gaze_data = st.selectbox('Select Gaze Data', gaze_data_headers)

# Query data for the selected gaze data type, ordered by ID
query = f"SELECT X, Y FROM GazeData WHERE header = '{selected_gaze_data}' AND state = 0 ORDER BY time ASC"

data = pd.read_sql_query(query, conn)
conn.close()

# Prepare lists for plotting
xList = []
yList = []
engaged = 0
count = 0

# Process data for plotting
for index, row in data.iterrows():
    #x = row['X']
    #y = 1 - row['Y']  # Reverse y-coordinate
    x = row['X'] / SCREEN_WIDTH
    y = 1 - (row['Y'] / SCREEN_HEIGHT) 
    count += 1

    # Check engagement in the specified area
    #if 0.3 < x < 0.6 and 0.25 < y < 0.6:
    if 0.3 < x < 0.6 and 0.25 < y < 0.6:
        engaged += 1

    xList.append(x)
    yList.append(y)

# Display engagement count and total count
st.write(f"Engaged Points: {engaged}")
st.write(f"Total Points: {count}")

# Plot the scatter plot
plt.figure(figsize=(20, 20))
plt.scatter(xList, yList, color='darkred', marker='D', s=20)
plt.xticks(fontsize=25)
plt.yticks(fontsize=25)

# Add labels and title
plt.title('Eye Tracking', fontsize=100)
plt.xlabel('X-Coordinate', fontsize=100)
plt.ylabel('Y-Coordinate', fontsize=100)

# Display the plot in Streamlit
st.pyplot(plt)

# Show grid
plt.grid(True)

# Display sample data (10 lines)
st.subheader("Random Sample Data")
sample_data = data.sample(n=10)  # Random sample of 10 lines
st.write(sample_data)

# Show data statistics
st.subheader("Data Statistics")
st.write(data.describe())

# Box plots for X and Y
fig, axes = plt.subplots(1, 2, figsize=(20, 10))

# Box plot for X
sns.boxplot(ax=axes[0], x=data['X'], color='lightblue')
axes[0].set_title('Box Plot of X', fontsize=25)
axes[0].set_xlabel('X', fontsize=20)

# Box plot for Y
sns.boxplot(ax=axes[1], x=data['Y'], color='lightgreen')
axes[1].set_title('Box Plot of Y', fontsize=25)
axes[1].set_xlabel('Y', fontsize=20)

# Display box plots in Streamlit
st.pyplot(fig)
