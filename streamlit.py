import streamlit as st
import psycopg2
import openai
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
import os

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Connect to PostgreSQL database
try:
    conn = psycopg2.connect(
        database="libraries",
        user="postgres",
        password="luolex",
        host="34.173.71.254",
        port="5432",
    )

    # Specify the SQL query to retrieve data
    query = "SELECT * FROM pls_fy2014_pupld14a"

    # Retrieve data into a pandas DataFrame
    df = pd.read_sql_query(query, conn)

finally:
    # Close the database connection in a 'finally' block to ensure it's always closed
    if conn:
        conn.close()

# Streamlit app
st.title("Interactive Chatbot with PostgreSQL Data")

# User input
user_input = st.text_input("You:", "")

# Display the PostgreSQL dataset in Streamlit
st.write("## PostgreSQL Dataset")
st.write(df)

# Generate response using OpenAI API
if user_input:
    response = openai.Completion.create(
        engine="gpt-3.5-turbo",  # Use the appropriate engine for your needs
        prompt=user_input,
        max_tokens=100,
    )

    st.text("ChatGPT:", response["choices"][0]["text"])

# Display map of US with libraries grouped by states using streamlit-folium
st.write("## US Map with Libraries Grouped by States")

# Create a folium map centered at the US
m = folium.Map(location=[37.0902, -95.7129], zoom_start=4)

# Add markers for each state with libraries
for state, state_df in df.groupby('stabr'):
    state_marker = folium.Marker([state_df["latitude"].mean(), state_df["longitud"].mean()],
                                 popup=f"State: {state}\nLibraries: {len(state_df)}")
    state_marker.add_to(m)

# Display the Folium map in Streamlit using folium_static
folium_static(m)





