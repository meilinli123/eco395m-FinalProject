import psycopg2
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from dotenv import load_dotenv
import os

load_dotenv('bing.env')

db_host = os.getenv('DB_HOST')
db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_pass = os.getenv('DB_PASS')

conn = psycopg2.connect(
    host=db_host,
    database=db_name,
    user=db_user,
    password=db_pass)

query = "SELECT * FROM seller_final JOIN car_basic ON ..."
car_data = pd.read_sql_query(query, conn)

features = car_data[['price', 'mileage', 'new_used', 'produce_year', 'state']]
target = car_data['desired_target_column']

X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2)

model = RandomForestRegressor()
model.fit(X_train, y_train)

predictions = model.predict(X_test)
mse = mean_squared_error(y_test, predictions)
print(f'Mean Squared Error: {mse}')


