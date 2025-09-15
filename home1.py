from dotenv import load_dotenv
import traceback
import streamlit as st
import pickle
import pandas as pd
import numpy as np
import os
import joblib
from supabase import create_client, Client
from io import StringIO
from datetime import datetime
import report

load_dotenv()


# Home page function with login and signup options
def home_page():

    st.markdown(
        """
        <style>
        /* Enhance buttons */
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            font-size: 12px;
            border-radius: 8px;
            padding: 5px 15px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Create a two-column layout for the main content and the buttons
    col1, col2 = st.columns([3, 1])  # The second column is narrower (1 part out of 4)

    with col1:
        # Main content of the Home Page
        st.title("Smart Real Estate Price Predictor")
        st.markdown(
            """
            <style>
                .subtitle {
                    font-size: 20px;
                    font-weight: bold;
                    color: #4CAF50; 
                    text-align: center;
                }
            </style>
            <p class="subtitle">
                Get accurate, AI-powered price predictions for properties in your ideal neighborhood.
            </p>
            """,
            unsafe_allow_html=True
        )


    with col2:
        # Check if the user is logged in
        if "user" in st.session_state:
            user = st.session_state["user"]
            
            # Check if the user has a display_name, else use the UID
            display_name = user.display_name.split()[0] if user.display_name else user.uid
            
            # Display a personalized welcome message
            st.write(f"Welcome, {display_name} 👋")
        else:
            # Create two buttons in the same row (side by side) if not logged in
            col3, col4 = st.columns([1, 1])  # Create two columns in col2
            with col3:
                login_but = st.button("Login")
            with col4:
                signup_but = st.button("Sign Up")

            # Handle the button clicks
            if login_but:  # Check if the login button is clicked
                # When the user clicks 'Login', set current page to 'login'
                st.session_state["current_page"] = "login"
                st.rerun()  # Rerun to navigate to login page

            if signup_but:  # Check if the signup button is clicked
                st.session_state["current_page"] = "signup"
                st.rerun()  # Rerun to navigate to signup page

    # Image
    st.image("./img/house.jpeg", use_container_width=True, width=20)  


    # Using Supabase to Store the csv file, access it and retrieve it.
    # Supabase Initialization
    
    url = os.environ.get("supabase_url")
    key = os.environ.get("supabase_key")
    supabase: Client = create_client(url, key) # type: ignore


    # Function to Read CSV from Supabase Storage
    def read_csv_from_supabase(file_name):
        file = supabase.storage.from_("RealEstateStorage").download(file_name)
        # Convert the byte content to string, then use StringIO to read it as a CSV
        file_str = file.decode("utf-8")  # Decode byte data to string
        return pd.read_csv(StringIO(file_str))  # Use StringIO to read as CSV
    
    
    # Load model and preprocessor
    model = joblib.load("best_svm_model.pkl")
    preprocessor = joblib.load("pipeline.pkl")


    # Read CSV from Supabase directly without downloading
    data = read_csv_from_supabase("preprocessed.csv")

    # Prediction Section
    st.write("\n")
    st.markdown(
            """
            <style>
                .subtitle {
                    font-size: 20px;
                    font-weight: bold;
                    color: #4CAF50; 
                    text-align: center;
                }
            </style>
            <p class="subtitle">
                🏠 Input property details and let our machine learning model estimate its value based on market trends..
            </p>
            """,
            unsafe_allow_html=True
        )

    # Create a form to collect user input
    with st.form("house_prediction_form"):
        # Sub county
        selected_sub_county = st.selectbox("Select the Sub County", options=data['Sub_County'].unique())

        # Neighborhood
        selected_neighborhood = st.selectbox("Select a Neighborhood", options=data['Neighborhood'].unique())

        # Square Meters
        selected_square_mtrs = st.number_input("Enter the square footage of the house", min_value=1, step=1)

        # Bedrooms
        selected_bedrooms = st.selectbox("Select Number of Bedrooms", options=sorted(data['Bedrooms'].dropna().unique()))

        # Bathrooms
        selected_bathrooms = st.selectbox("Select Number of Bathrooms", options=sorted(data['Bathrooms'].dropna().unique()))


        col_submitted, col_report = st.columns([0.2, 1.5])

        with col_submitted:
            submitted = st.form_submit_button("Predict")

        with col_report:
            view_report  =   st.form_submit_button("View report")
        

    # Perform prediction only if the form is submitted and the user is logged in
    if submitted:
        if "user" not in st.session_state:
            st.warning("You need to log in to make a prediction.")
        else:
            # Combine user input into a single DataFrame only if user is logged in
            user_input = pd.DataFrame({
                "Sub_County": [selected_sub_county],
                "Neighborhood": [selected_neighborhood],
                "sq_mtrs": [selected_square_mtrs],
                "Bedrooms": [selected_bedrooms],
                "Bathrooms": [selected_bathrooms],
            })
            
            # Retrieve exact match rent price
        actual_price = data[
            (data["Sub_County"] == selected_sub_county) &
            (data["Neighborhood"] == selected_neighborhood) &
            (data["sq_mtrs"] == selected_square_mtrs) &
            (data["Bedrooms"] == selected_bedrooms) &
            (data["Bathrooms"] == selected_bathrooms)
        ]["Price"].values  

        st.subheader("Prediction Results")
        
        # Checking for the actual price.
        if len(actual_price) > 0:
            actual_price = actual_price[0]
            st.success(f"**Exact Rent Price Found:** {actual_price:,} KES")
        else:
            st.warning("No exact actual price found. Displaying an approximate rent price.")

            # Find similar properties
            filtered_data = data[
                (data["Sub_County"] == selected_sub_county) & 
                (data["Neighborhood"] == selected_neighborhood)
            ]
            similar_properties = filtered_data[
                (filtered_data["Bedrooms"] == selected_bedrooms) & 
                (filtered_data["Bathrooms"] == selected_bathrooms)
            ]

            # Calculate estimated price
            if not similar_properties.empty:
                estimated_price = similar_properties["Price"].median()
            else:
                estimated_price = filtered_data["Price"].median()

            # **New Safe Handling for NaN values**
            if pd.isna(estimated_price):  
                st.error("No data available to estimate rent price.")
            else:
                estimated_price = int(estimated_price)
                st.info(f"**Average Rent Price Based on the Neighborhood :** {estimated_price:,} KES")

            # **Display predicted price (if available)**
            if "predicted_price" in locals() and predicted_price: # type: ignore
                predicted_price = int(predicted_price)
                if abs(predicted_price - estimated_price) > 5000:  # Only show if a big difference exists
                    st.success(f"**Predicted Rent Price (ML Model):** {predicted_price:,} KES")

            # Apply preprocessing to user input
            try:
                processed_input = preprocessor.transform(user_input) # type: ignore

                # Make prediction
                log_prediction = model.predict(processed_input)

                # Reverse the logarithmic transformation to get the actual price
                predicted_price = np.exp(log_prediction[0])

                # Display the prediction
                st.success(f"Predicted Rent Price (KES): {predicted_price:,.0f}")

                # Store the prediction in Supabase
                user = st.session_state["user"]
                prediction_record = {
                    "user_id": user.uid,
                    "sub_county": selected_sub_county,
                    "neighborhood": selected_neighborhood,
                    "sq_mtrs": int(selected_square_mtrs),
                    "bedrooms": int(selected_bedrooms),
                    "bathrooms": int(selected_bathrooms),
                    "predicted_price": round(predicted_price, 2),
                    "Actual_price": int(estimated_price),
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # ISO format
                }

                try:
                    # Storing the prediction in Supabase database.
                    response = supabase.table("prediction").insert(prediction_record).execute()
                    
                    if response.data:
                        st.success("Prediction stored successfully!")
                    else:
                        st.error("Failed to store the prediction in Supabase.")
                        st.code(response, language="json")  # Display Supabase response for debugging
                except Exception as e:
                    st.error("An error occurred while storing the prediction.")
                    st.code(traceback.format_exc(), language="python")


            except Exception as e:
                st.error(f"An error occurred during preprocessing or prediction: {e}")

    else:
        # If the user is not logged in, display a prompt
        if "user" not in st.session_state:
            st.warning("Please log in to access the prediction form.")

    if view_report:
        report.display_report()

    # Footer Section
    st.markdown("---")
    st.write("© 2025 Kelvin Njuguna | All rights reserved.")