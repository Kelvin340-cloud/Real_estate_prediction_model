import streamlit as st
from firebase_admin import auth
import base64

def forgot_password_page():
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

    # Reset Login Info
    st.markdown(
        "<h3 style='text-align: center;'>Reset Password</h3>",
        unsafe_allow_html=True
    )

    # Use columns to center and reduce the width of the form
    col_form_left, col_form_center, col_form_right = st.columns([0.3, 0.4, 0.3]) #create columns to center the form
    with col_form_center:
        with st.form("forgot_password_form", border=True):
            # Center the image
            st.markdown(
                    f"""
                    <div style="display: flex; justify-content: center;">
                        <img src="data:image/png;base64,{logo_base64}" width="200">
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            st.write("\n")    
            forgot_email = st.text_input("Enter your email to reset password")

            # Create two columns for buttons
            col1, col2 = st.columns([0.6, 0.4])  

            with col1:
                forgot_submit = st.form_submit_button("Send Reset Link")

            with col2:
                if st.form_submit_button("Back to Login", type="secondary"):
                    st.session_state['forgot_password'] = False
                    st.rerun()

            if forgot_submit:
                if forgot_email:
                    try:
                        auth.generate_password_reset_link(forgot_email)
                        st.success(f"Password reset link sent to {forgot_email}")
                        st.session_state['forgot_password'] = False
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error sending password reset link: {e}. Check console and firebase settings.")
                        print(f"Firebase password reset error: {e}")
                else:
                    st.error("Please enter your email address.")