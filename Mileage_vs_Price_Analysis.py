import streamlit as st
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
import psycopg2
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.robust.robust_linear_model import RLM
from postgre import database_info

def write_table(results):
    df_results = pd.DataFrame(results)

    df_results = df_results.sort_values(by='Coefficient', ascending=False).reset_index(drop=True)

    df_results.index = df_results.index + 1

    st.header("Regression Coefficients by Makes")
    st.table(df_results)

def regress(make):
    
    df = query()
    
    X = sm.add_constant(df['mileage'])
    y = df['price']
    model = RLM(y, X).fit()
    message = f"Coefficient = {model.params['mileage']:.4f}"
    
    st.header(f"Regression Analysis for {make}")
    
    st.write(message)

    plt.figure()
    plt.scatter(df['mileage'], y, alpha=0.5)
    plt.title(f"{make} - Price vs. Mileage Regression")
    plt.xlabel("Mileage")
    plt.ylabel("Price")
    plt.plot(df['mileage'], model.predict(X), color='red', linewidth=2)
    st.pyplot(plt)

    return {
        "Make": make,
        "Coefficient": model.params['mileage']
    }

def query():
    conn = psycopg2.connect(**db_info)
    query = f"SELECT price, mileage FROM car_basic WHERE make = '{make}' AND new_used = '1'"
    df = pd.read_sql(query, conn)
    df = df.dropna()
    if len(df) < 3:
        st.warning(f"Insufficient data points for {make} to perform regression analysis. Skipping.")
        return
    return df

if __name__ == "__main__":
    db_info = database_info 

    makes = ["Audi", "Toyota", "Volkswagen", "Jeep", "Honda", "Mazda", "RAM", "Buick", "Lexus", "GMC"]
    
    st.title("Car Price Regression Analysis")

    results = []
    for make in makes:
        result = regress(make)
        results.append(result)

    write_table(results)