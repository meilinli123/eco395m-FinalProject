import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
import psycopg2
from sqlalchemy import create_engine
import joblib

# Connect to your PostgreSQL database
def connect_to_database():
    try:
        connection = psycopg2.connect(
            user="postgres",
            password="luolex",
            host="34.173.71.254",
            port=5432,
            database="finalproject",
        )
        return connection
    except psycopg2.Error as e:
        print(f"Error connecting to the database: {e}")
        return None

# Function to fetch data from the database
def fetch_data():
    connection = connect_to_database()
    if connection:
        # Replace 'car_basic' and 'seller_final' with the actual table names in your database
        query = """
            SELECT car_basic.make, car_basic.model, car_basic.produce_year, car_basic.mileage,
                   seller_final.zip_code, car_basic.price
            FROM car_basic
            JOIN seller_final ON car_basic.vin = seller_final.vin
        """
        df = pd.read_sql_query(query, connection)
        connection.close()
        return df
    else:
        return None

# Load your dataset
df = fetch_data()

if df is not None:
    # Encode categorical variables if needed (e.g., make and model)
    label_encoders = {}
    
    categorical_columns = ['make', 'model', 'produce_year', 'mileage']  # Add other categorical columns if needed
    
    for column in categorical_columns:
        label_encoder = LabelEncoder()
        df[column] = label_encoder.fit_transform(df[column])
        label_encoders[column] = label_encoder

    # One-hot encode the zip_code
    one_hot_encoder = OneHotEncoder(sparse=False, drop='first')
    zip_code_encoded = one_hot_encoder.fit_transform(df[['zip_code']])
    zip_code_columns = [f'zip_code_{code}' for code in one_hot_encoder.get_feature_names_out(['zip_code'])]
    zip_code_df = pd.DataFrame(zip_code_encoded, columns=zip_code_columns)
    df = pd.concat([df, zip_code_df], axis=1)

    # Select features and target variable
    features = ['make', 'model', 'produce_year', 'mileage'] + zip_code_columns
    X = df[features]
    y = df['price']

    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize and train the Decision Tree Regression model
    model = DecisionTreeRegressor()
    model.fit(X_train, y_train)

    # Save the trained model
    joblib.dump(model, 'decision_tree_model.joblib')

    # Save the label encoders
    joblib.dump(label_encoders, 'label_encoders.joblib')
    
    joblib.dump(one_hot_encoder, 'one_hot_encoder.joblib')

    # Make predictions on the test set
    predictions = model.predict(X_test)

    # Evaluate the model (optional)
    mse = mean_squared_error(y_test, predictions)
    print(f'Mean Squared Error: {mse}')
    

    # Now you can use the trained model to make predictions on new data
    new_zip_code = '44707'  # Replace with the actual new zip code
    new_data = pd.DataFrame({
        'make': [label_encoders['make'].transform(['Lincoln'])[0]],
        'model': [label_encoders['model'].transform(['Corsair Standard'])[0]],
        'produce_year': [2022],
        'mileage': [50000],
        'zip_code': [new_zip_code]
    })

    # One-hot encode the new zip code
    new_zip_code_encoded = one_hot_encoder.transform(new_data[['zip_code']])
    new_zip_code_columns = [f'zip_code_{code}' for code in one_hot_encoder.get_feature_names_out(['zip_code'])]
    new_zip_code_df = pd.DataFrame(new_zip_code_encoded, columns=new_zip_code_columns)
    new_data = pd.concat([new_data, new_zip_code_df], axis=1)

    # Make a prediction for the new data
    estimated_price = model.predict(new_data[features])
    print(f'Estimated Price for New Data: {estimated_price[0]}')
else:
    print("Failed to fetch data from the database.")



