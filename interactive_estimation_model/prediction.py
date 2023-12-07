import streamlit as st
import joblib
import pandas as pd

# Load the Decision Tree model and label encoders
decision_tree = joblib.load('decision_tree_model.joblib')
label_encoders = joblib.load('label_encoders.joblib')
# Load the one-hot encoder (based on training data)
one_hot_encoder = joblib.load('one_hot_encoder.joblib')

# Function to encode categorical variables for prediction
def encode_input_data(make, model, produce_year, mileage, zip_code):

    encoded_data = {
        'make': [label_encoders['make'].transform([make])[0]],
        'model': [label_encoders['model'].transform([model])[0]],
        'produce_year': [produce_year],
        'mileage': [mileage],
        'zip_code': [zip_code]
    }

    # One-hot encode the zip code
    zip_code_encoded = one_hot_encoder.transform(pd.DataFrame(encoded_data['zip_code']))
    zip_code_columns = [f'zip_code_{code}' for code in one_hot_encoder.get_feature_names_out(['zip_code'])]
    zip_code_df = pd.DataFrame(zip_code_encoded, columns=zip_code_columns)
    encoded_data.update(zip_code_df)

    return pd.DataFrame(encoded_data, columns=['make', 'model', 'produce_year', 'mileage'] + zip_code_columns)

# Streamlit app
def main():
    st.title("Car Price Estimation")

    # User input for car details
    make = st.text_input("Enter the car brand (make):", "")
    model = st.text_input("Enter the car model:", "")
    produce_year = st.number_input("Enter the production year:", 2000, 2023, 2010)
    mileage = st.number_input("Enter the mileage:", 0.0, 100000.0, 50000.0)
    zip_code = st.text_input("Enter the seller's zip code:", "")

    # Button to trigger the estimation
    if st.button("Estimate Car Price"):
        # Encode user input for prediction
        input_data = encode_input_data(make, model, produce_year, mileage, zip_code)

        if input_data is not None:
            # Make a prediction
            estimated_price = decision_tree.predict(input_data)[0]

            # Decorate the output on the Streamlit app
            st.success(f"The estimated price for the car is: ${estimated_price:.2f}")

if __name__ == "__main__":
    main()
