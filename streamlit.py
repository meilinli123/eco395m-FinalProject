import streamlit as st
import psycopg2
import openai
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
import os
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import pandas as pd
import sqlite3
import statsmodels.api as sm
import statsmodels.formula.api as smf
from streamlit_extras.dataframe_explorer import dataframe_explorer


# Set page configuration
st.set_page_config(
    page_title="Car Analysis App",
    page_icon=":car:",
    layout="wide"
)

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

# begin page

st.sidebar.header("Search Options")
car_make = st.sidebar.text_input("Enter Car Make:")
car_model = st.sidebar.text_input("Enter Car Model:")
search_button = st.sidebar.button("Search")

# populating cars.com logo
st.title("Find Your Dream Car")
st.image('https://s3.amazonaws.com/fzautomotive/dealers/56998b9186be8.png')
st.image('https://www.cars.com/images/cars_logo_primary@2x-369317d81682f33d21c8fbdc7959f837.png?vsn=d',
         caption='Data provided by Cars.com')


# Streamlit app
st.title("Interactive Chatbot with PostgreSQL Data")

# User input
user_input = st.text_input("You:", "")

# Display the PostgreSQL dataset in Streamlit
st.write("## PostgreSQL Dataset")
#st.write(df)

# custom query search
dataframe = dataframe_explorer(df, case=False)
dataframe = pd.DataFrame(dataframe)
st.dataframe(dataframe)
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


from analysis import top_5_expensive_brand

top_5_expensive_brand_dataset = top_5_expensive_brand()
st.bar_chart(top_5_expensive_brand_dataset, x = "brand", y = "avg_price" )


#Analysis displayed in stream lit


import streamlit as st
import pandas as pd
from analysis import top_10_brands, top_5_expensive_brand, top_5_cheapest_brand, make_state, model_state, connect_to_database, Mileage_price


# Connect to the database
def get_database_connection():
    try:
        return connect_to_database()  # Replace with your actual database connection logic
    except Exception as e:
        st.error(f"Error connecting to the database: {e}")
        return None

# Function to display top 10 brands
def display_top_10_brands():
    st.header("Top 10 Car Brands by Count")
    top10_df = top_10_brands()
    if top10_df is not None:
        st.bar_chart(top10_df.set_index("brand"))

# Function to display top 5 expensive brands
def display_top_5_expensive_brands():
    st.header("Top 5 Expensive Car Brands")
    top5_expensive_df = top_5_expensive_brand()
    if top5_expensive_df is not None:
        st.bar_chart(top5_expensive_df.set_index("brand"))

# Function to display top 5 cheapest brands
def display_top_5_cheapest_brands():
    st.header("Top 5 Cheapest Car Brands")
    top5_cheapest_df = top_5_cheapest_brand()
    if top5_cheapest_df is not None:
        st.bar_chart(top5_cheapest_df.set_index("brand"))

# Function to display car count by make and state
def display_make_state():
    st.header("Car Count by Make and State")
    make_state_df = make_state()
    if make_state_df is not None:
        st.bar_chart(make_state_df.set_index(["make", "state"]))

# Function to display car count by model and state
def display_model_state():
    st.header("Car Count by Model and State")
    model_state_df = model_state()

    if model_state_df is not None:
        fig, ax = plt.subplots()
        sns.barplot(x = "state", y = "model", data = model_state_df, ax = ax)
        st.pyplot(fig)
        st.bar_chart(model_state_df.set_index(["model", "state"]))

# Streamlit app layout
st.title("Car Analysis Dashboard")

# Display selected analysis based on user input or default
analysis_option = st.sidebar.selectbox("Select Analysis", ["Top 10 Brands", "Top 5 Expensive Brands",
                                                           "Top 5 Cheapest Brands",])

if analysis_option == "Top 10 Brands":
    display_top_10_brands()
elif analysis_option == "Top 5 Expensive Brands":
    display_top_5_expensive_brands()
elif analysis_option == "Top 5 Cheapest Brands":
    display_top_5_cheapest_brands()
elif analysis_option == "Make State":
    display_make_state()
elif analysis_option == "Model State":
    display_model_state()


# Create an empty DataFrame to store results
results_df = pd.DataFrame(columns=["Make", "Mileage Coefficient", "Intercept", "R-squared"])


df = Mileage_price()
df = df.fillna(0)


    # Perform OLS regression
df['mileage'] = df['mileage'].astype(float)
df['price'] = df['price'].astype(float)
X = sm.add_constant(df['mileage'])
y = df['price']
model = sm.OLS(y, X).fit()

    # Store results in the DataFrame
results_df = pd.DataFrame()
results_df["Mileage Coefficient"] = model.params['mileage']
results_df["const"] = model.params['const']


# Streamlit app
st.title("Mileage vs. Price Analysis by Brand")

# Display OLS regression results
st.write("OLS Regression Results:")
st.dataframe(model.params)

# Plot OLS regression lines
st.write("OLS Regression Lines:")
fig, ax = plt.subplots()
sns.regplot(data = df, x = "mileage", y = "price", ax = ax)
st.pyplot(fig)


st.write("Scatter plot of Mileage vs. Price:")
st.scatter_chart(df[['mileage', 'price']])
