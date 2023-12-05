import psycopg2
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

conn = psycopg2.connect(
    host='34.173.71.254',
    database='car_basic',
    user='postgres',
    password='your_password')

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

