import streamlit as st
from firebase_admin import auth
from firebase_init import initialize_firebase  # Import Firebase initialization function
import base64

# Initialize Firebase
initialize_firebase()

def signup_page():

    # Add background image to the page
    # Function to load image as base64
    def get_base64_image(image_path):
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")

    # Convert image to base64
    img_base64 = get_base64_image('img/background.avif')
    logo_base64 = get_base64_image('img/Logo1.png')

    st.markdown(
        f"""
        <style>
            .stApp {{
                background-image: url('data:image/avif;base64,{img_base64}');
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                min-height: 100vh;
            }}
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        "<h3 style='text-align: center;'>Create a New Account</h3>",
        unsafe_allow_html=True
    )

    # Sign-up form with first name, last name, email, password, confirm password, and username
    # Use columns to center and reduce the width of the form
    col1, col2, col3 = st.columns([0.3, 0.4, 0.3])  # Adjust width to make the form narrower
    with col2:
        with st.form("signup_form", border=True):
            
            # Center the image
            st.markdown(
                f"""
                <div style="display: flex; justify-content: center;">
                    <img src="data:image/png;base64,{logo_base64}" width="200">
                </div>
                """,
                unsafe_allow_html=True
            )

            # Signup input
            first_name = st.text_input("First Name")
            last_name = st.text_input("Last Name")
            email = st.text_input("Email Address")
            password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            username = st.text_input("Unique Username")
            
            submit_button = st.form_submit_button("Sign Up")

            if submit_button:
                # Check if any required fields are empty
                if not first_name or not last_name or not email or not password or not confirm_password or not username:
                    st.warning("Please fill in all fields.")
                elif password != confirm_password:
                    st.error("Passwords do not match. Please try again.")
                else:
                    try:
                        # Create the user in Firebase
                        display_name = f"{first_name} {last_name}"  # Set display name
                        auth.create_user(
                            email=email,
                            password=password,
                            uid=username,
                            display_name=display_name
                        )
                        st.success("Account created successfully! Redirecting to login page...")
                        st.balloons()
                        st.session_state["current_page"] = "login"  # Set the page to 'login'
                    except Exception as e:
                        st.error(f"Error during sign up: {e}")

    if st.session_state.get("current_page") == "login":
        st.rerun()  # Rerun the app to apply page change
