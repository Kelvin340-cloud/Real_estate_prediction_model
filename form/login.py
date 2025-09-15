import streamlit as st
from firebase_admin import auth
from firebase_init import initialize_firebase
import base64
from .forgot_password import forgot_password_page

# Initialize Firebase
initialize_firebase()

def login_page():

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

    # Log in Info.
    st.markdown(
        "<h3 style='text-align: center;'>Login to Your Account</h3>",
        unsafe_allow_html=True
    )

    # Use columns to center and reduce the width of the form
    col1, col2, col3 = st.columns([0.3, 0.4, 0.3])

    if not st.session_state.get('forgot_password', False): #show login form only if forgot password is false or not set.
        with col2:
            with st.form("login_form", border=True):
                # Center the image
                st.markdown(
                    f"""
                    <div style="display: flex; justify-content: center;">
                        <img src="data:image/png;base64,{logo_base64}" width="200">
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                email = st.text_input("Email Address", key="email_input")
                password = st.text_input("Password", type="password", key="password_input")

                #split the buttons into columns
                col_login, col_forgot = st.columns([0.6, 0.4])

                with col_login:
                    submit_button = st.form_submit_button("Login")

                with col_forgot:
                    if st.form_submit_button("Forgot Password?", type="secondary"):
                        st.session_state['forgot_password'] = True #set state to show forgot password form
                        st.rerun() #force rerun to hide login form

                if submit_button:
                    try:
                        user = auth.get_user_by_email(email)
                        st.session_state["user"] = user
                        st.session_state["current_page"] = "home"
                        st.success(f"Login successful! Welcome {user.display_name.split()[0]}")
                    except Exception as e:
                        st.error(f"Error during login: {e}")
    else:
        forgot_password_page() #if forgot password is true, show only the forgot password form.

    if st.session_state.get("current_page") == "home":
        st.rerun()