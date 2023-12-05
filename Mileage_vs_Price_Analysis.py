import streamlit as st
import pandas as pd
import sqlite3
import statsmodels.api as sm
import statsmodels.formula.api as smf

# Create a connection to SQLite database
conn = sqlite3.connect('finalproject.db') 

# Define a list of selected brands
selected_brands = ["Audi", "Toyota", "Volkswagen", "Jeep", "Honda",
                    "Mazda", "RAM", "Buick", "Lexus", "GMC"]

# Create an empty DataFrame to store results
results_df = pd.DataFrame(columns=["Make", "Mileage Coefficient", "Intercept", "R-squared"])

# Loop through selected brands and perform OLS regression
for selected_brand in selected_brands:
    # Define a SQL query to retrieve data for the selected brand
    query = f'''
        SELECT Mileage, Price
        FROM car_basic
        WHERE Make = '{selected_brand}'
    '''

    # Execute the SQL query and read the results into a Pandas DataFrame
    df = pd.read_sql_query(query, conn)

    # Perform OLS regression
    X = sm.add_constant(df['Mileage'])
    y = df['Price']
    model = sm.OLS(y, X).fit()

    # Store results in the DataFrame
    results_df = results_df.append({"Make": selected_brand,
                                    "Mileage Coefficient": model.params['Mileage'],
                                    "Intercept": model.params['const'],
                                    "R-squared": model.rsquared}, ignore_index=True)

# Close the database connection
conn.close()

# Streamlit app
st.title("Mileage vs. Price Analysis by Brand")

# Display OLS regression results
st.write("OLS Regression Results:")
st.dataframe(results_df)

# Plot OLS regression lines
st.write("OLS Regression Lines:")
for index, row in results_df.iterrows():
    selected_brand = row["Make"]
    mileage_coefficient = row["Mileage Coefficient"]
    intercept = row["Intercept"]

    df_brand = df[df['Make'] == selected_brand]

    # Plot mileage vs. price scatter plot
    st.subheader(f"Brand: {selected_brand}")
    st.write("Scatter plot of Mileage vs. Price:")
    st.scatter_chart(df_brand[['Mileage', 'Price']])

    # Plot OLS regression line
    st.write(f"OLS Regression Line for {selected_brand}:")
    st.line_chart(df_brand[['Mileage', 'Price']])
