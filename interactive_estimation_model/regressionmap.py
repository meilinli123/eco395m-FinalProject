import streamlit as st
import folium
from folium import Marker
from streamlit_folium import folium_static
import pandas as pd
import joblib


# Load the Decision Tree model and label encoders
decision_tree = joblib.load('interactive_estimation_model/decision_tree_model.joblib')
label_encoders = joblib.load('interactive_estimation_model/label_encoders.joblib')
# Load the one-hot encoder (based on training data)
one_hot_encoder = joblib.load('interactive_estimation_model/one_hot_encoder.joblib')

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

# Function to get latitude and longitude for a state code
def get_coordinates_for_state(state_code):
    # Define a mapping between state codes and their geographical coordinates
    state_coordinates = {
    "AL": (32.806671, -88.474270, 30.2234, -87.6349),
    "AK": (61.0169, -147.8656, 51.6351, -179.1489),
    "AZ": (33.7298, -109.0452, 31.3322, -114.818),
    "AR": (34.9697, -89.6925, 33.0041, -94.4842),
    "CA": (36.7783, -119.5313, 32.5341, -114.1315),
    "CO": (39.5501, -102.0416, 36.9931, -109.0452),
    "CT": (41.6032, -71.7874, 40.9665, -73.7278),
    "DE": (38.4511, -75.0479, 38.4511, -75.0479),
    "FL": (27.9944, -80.0318, 24.3963, -87.6349),
    "GA": (32.1574, -80.8414, 30.3556, -84.3219),
    "HI": (20.7961, -154.9615, 18.7763, -154.8061),
    "ID": (44.0682, -111.7111, 41.9918, -117.0224),
    "IL": (40.3495, -87.6349, 36.9931, -91.5131),
    "IN": (41.7627, -84.8065, 37.7718, -88.0971),
    "IA": (42.0046, -90.1401, 40.3755, -96.6395),
    "KS": (39.5501, -94.8994, 36.9931, -102.0416),
    "KY": (37.5139, -82.2625, 36.4984, -89.5715),
    "LA": (31.1801, -88.9231, 28.9335, -93.8356),
    "ME": (45.2538, -66.9406, 42.9774, -70.7038),
    "MD": (39.7220, -74.9454, 37.9032, -79.4877),
    "MA": (42.0330, -70.6387, 41.1855, -73.5081),
    "MI": (45.2353, -82.1228, 41.7590, -90.4182),
    "MN": (47.4679, -89.5715, 43.4994, -96.6395),
    "MS": (32.2988, -88.0971, 30.3556, -91.6216),
    "MO": (40.6136, -89.5715, 35.9959, -95.7747),
    "MT": (48.9982, -104.0489, 44.3537, -116.0372),
    "NE": (42.0046, -95.7735, 39.9999, -104.0535),
    "NV": (39.5501, -114.0435, 35.0019, -120.0055),
    "NH": (45.0159, -70.9323, 42.6970, -72.5501),
    "NJ": (40.6994, -73.7278, 38.9288, -75.5594),
    "NM": (36.9931, -103.0019, 31.3322, -109.0452),
    "NY": (45.0109, -71.1851, 40.4774, -79.7626),
    "NC": (36.5880, -75.5619, 33.8423, -83.3199),
    "ND": (48.9982, -96.6012, 45.9358, -104.0489),
    "OH": (41.9788, -80.5180, 38.4032, -84.8202),
    "OK": (37.0015, -94.4315, 33.6158, -103.0022),
    "OR": (46.292874, -116.4638, 41.9918, -124.5662),
    "PA": (42.2691, -74.8740, 39.7220, -80.5180),
    "RI": (42.0139, -71.1851, 41.1466, -71.7099),
    "SC": (35.2131, -78.4993, 32.0346, -83.3539),
    "SD": (45.9432, -96.6012, 42.4796, -104.0489),
    "TN": (36.6782, -81.6469, 34.9834, -90.3131),
    "TX": (36.4931, -94.0415, 25.8374, -106.6456),
    "UT": (41.0034, -109.0452, 36.9971, -114.0435),
    "VT": (45.0134, -73.7278, 42.7262, -73.1414),
    "VA": (39.7285, -75.5594, 36.5408, -83.6753),
    "WA": (49.0025, -116.4638, 45.5435, -124.5662),
    "WV": (40.6374, -80.5180, 37.2019, -84.8202),
    "WI": (45.0126, -86.5653, 42.4919, -92.8875),
    "WY": (45.0021, -104.0455, 41.0034, -111.0457),
}

    return state_coordinates.get(state_code, (0, 0))  # Default to (0, 0) if state code not found

# Streamlit app
def main():
    st.title("Car Price Estimation and Map")

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

            # Create a Streamlit map with a marker
            st.sidebar.subheader("Estimated Car Location")
            st.sidebar.text(f"Estimated Price: ${estimated_price:.2f}")

            # Example: Use the state code (zip code) for location
            state_code = zip_code
            m = folium.Map(location=get_coordinates_for_state(state_code), zoom_start=8)

            # Add a marker for the estimated location of the car
            marker_estimated = folium.Marker(
                location=get_coordinates_for_state(state_code),
                popup=f"Estimated Price: ${estimated_price:.2f}",
                tooltip=f"Estimated Price: ${estimated_price:.2f}",
            )
            marker_estimated.add_to(m)

            # Display the map
            folium_static(m)

            st.success(f"The estimated price for the car is: ${estimated_price:.2f}")

if __name__ == "__main__":
    main()
