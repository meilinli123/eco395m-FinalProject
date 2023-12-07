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
from streamlit_option_menu import option_menu
from scipy import stats
import altair as alt
import streamlit as st
import numpy as np
import pandas as pd
from analysis import top_10_brands, top_5_expensive_brand, top_5_cheapest_brand, make_state, model_state, \
    connect_to_database, Mileage_price
from interactive_estimation_model import regressionmap
# openai.api_key = os.getenv("OPENAI_API_KEY")

# Set page configuration
st.set_page_config(
    page_title="Car Analysis App",
    page_icon=":car:",
    layout="wide"
)

# populating cars.com logo
st.title("Search About Your Dream Car!")
st.image('https://s3.amazonaws.com/fzautomotive/dealers/56998b9186be8.png')
st.image('https://www.cars.com/images/cars_logo_primary@2x-369317d81682f33d21c8fbdc7959f837.png?vsn=d',
         caption=' *All data provided by Cars.com - for educational purposes only*')


@st.cache_data(ttl=7200, show_spinner=False)
def generate_text(prompt):
    formatted_prompt = prompt.strip().lower()

    completions = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": "You are a car expert hired to provide details on car selections as well as help get the best price for the specified car)."},
            {"role": "user", "content": formatted_prompt}
        ],
        max_tokens=800

    )
    message = completions.choices[0].message["content"]
    return message.strip()


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
        sns.barplot(x="state", y="model", data=model_state_df, ax=ax)
        st.pyplot(fig)
        st.bar_chart(model_state_df.set_index(["model", "state"]))


try:
    conn = psycopg2.connect(
        database="libraries",
        user="postgres",
        password="luolex",
        host="34.173.71.254",
        port="5432")

    query = "SELECT * FROM pls_fy2014_pupld14a"

    df = pd.read_sql_query(query, conn)

finally:
    if conn:
        conn.close()

app_menu = ['Chatbot Suggestions', 'Interactive Data', 'Analysis Dashboard', 'Price Prediction']

with st.sidebar:
    app_menu_options = option_menu(
        menu_title="App Features", options=app_menu,
        menu_icon="chevron-double-left", default_index=0, orientation="vertical")

if app_menu_options == 'Chatbot Suggestions':
    with st.form('Search Options'):

        car_make = st.text_input("Enter Car Make:")

        car_model = st.text_input("Enter Car Model:")

        car_year = st.date_input('Enter Car Year')

        if st.form_submit_button("Search"):
            gen_ai_Input_one = f"""
                Given the select vehicle and each feature related to the vehicle,could you identify the features that are most important?
                vehicle make: {car_make}
                vehicle model: {car_model}
                vehicle year:{car_year}
                - 

                Please provide actionable insights on which features that can determine the longevity of this vehicle..

            """
            Factors_Ret = generate_text(gen_ai_Input_one)
            st.markdown(Factors_Ret)

if app_menu_options == 'Interactive Data':

    analysis_option = st.selectbox("Select Analysis",
                                   ["Top 10 Brands", "Top 5 Expensive Brands", "Top 5 Cheapest Brands", ])

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

    # custom query search
    # dataframe = dataframe_explorer(df, case=False)
    # dataframe = pd.DataFrame(dataframe)
    # st.dataframe(dataframe)
    # if st.checkbox('Activate Ai Agent'):
    #     gen_ai_Input = f"""
    #                 Given the select vehicle and each feature related to the vehicle,could you identify the features that are most important?
    #                 - Reason for the current price fo this vehicle : {dataframe.to_dict()}
    #                 - Features that can determine the longevity of this vehicle
    #                 Please provide actionable insights on which features should be closely monitored and the possible price that can be negotiated.
    #             """

    #     Factors_Ret = generate_text(gen_ai_Input)
    #     st.markdown(Factors_Ret)

if app_menu_options == 'Analysis Dashboard':
    st.header("Car Analysis Dashboard")

    # st.write("## US Map with Libraries Grouped by States")

    # m = folium.Map(location=[37.0902, -95.7129], zoom_start=4)

    # for state, state_df in df.groupby('stabr'):
    #     state_marker = folium.Marker([state_df["latitude"].mean(), state_df["longitud"].mean()],
    #     popup=f"State: {state}\nLibraries: {len(state_df)}")
    #     state_marker.add_to(m)

    # folium_static(m)

    st.subheader("Mileage vs. Price Analysis by Brand")

    df = Mileage_price()
    df = df.fillna(0)

    # Perform OLS regression
    df['mileage'] = df['mileage'].astype(float)
    df['price'] = df['price'].astype(float)

    with st.form('Custom Car Make Info'):

        AnalysisCol_one, AnalysisCol_two = st.columns(2)

        df_plot_selection = st.multiselect('Select Car Makes to Plot', df['make'].unique(), default=df['make'].unique())

        filtered_cars = df[df['make'].isin(df_plot_selection)]

        if st.form_submit_button("Custom Search"):
            st.write("Scatter plot of Mileage vs. Price:")

            c = (
                alt.Chart(filtered_cars)
                    .mark_circle()
                    .encode(x="mileage", y="price", size="produced_year", color="make",
                            tooltip=["mileage", "price", "produced_year", 'make'])
            )

            st.altair_chart(c, use_container_width=True)

            filtered_cars['mileage_scaled'] = (filtered_cars['mileage'] - filtered_cars['mileage'].min()) / (
                        filtered_cars['mileage'].max() - filtered_cars['mileage'].min())
            filtered_cars['price_scaled'] = (filtered_cars['price'] - filtered_cars['price'].min()) / (
                        filtered_cars['price'].max() - filtered_cars['price'].min())

            slope, intercept, r_value, p_value, std_err = stats.linregress(filtered_cars['mileage_scaled'],
                                                                           filtered_cars['price_scaled'])

            fig, ax = plt.subplots()
            ax.scatter(filtered_cars['mileage_scaled'], filtered_cars['price_scaled'], label='Data points')
            ax.plot(filtered_cars['mileage_scaled'], intercept + slope * filtered_cars['mileage_scaled'], 'r',
                    label='Fitted line')

            ax.set_xlabel('Mileage')
            ax.set_ylabel('Price')
            ax.legend()
            st.pyplot(fig)

    # X = sm.add_constant(df['mileage'])
    # y = df['price']
    # model = sm.OLS(y, X).fit()

    # # Store results in the DataFrame
    # results_df = pd.DataFrame()
    # results_df["Mileage Coefficient"] = model.params['mileage']
    # results_df["const"] = model.params['const']

    # Streamlit app

    # # Display OLS regression results
    # st.write("OLS Regression Results:")
    # st.dataframe(model.params)

    # # Plot OLS regression lines
    # st.write("OLS Regression Lines:")
    # fig, ax = plt.subplots()
    # sns.regplot(data = df, x = "mileage", y = "price", ax = ax)
    # st.pyplot(fig)


#price pred
if app_menu_options == 'Price Prediction':
    regressionmap.main()