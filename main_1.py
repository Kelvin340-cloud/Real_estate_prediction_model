import streamlit as st
# Page Title and Configuration
st.set_page_config(
    page_title="""Predictive Real Estate Pricing Model Using Machine Learning Algorithm and Historical Data Analysis.""",
    layout="wide",
)

from streamlit_option_menu import option_menu
from form.login import login_page
from form.signup import signup_page
import home # Import home page function
import about
import contact
import report
import connection
from account import account_page  # Import the account page functionality
from firebase_init import initialize_firebase  # Ensure Firebase initialization


# Initialize Firebase
initialize_firebase()



# Initialize session state for page management
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "home"  # Default to home page

# Sidebar menu with option menu
def sidebar_menu():
    with st.sidebar:
        # Add an image at the top of the sidebar
        st.image(
            "./img/Logo1.png", 
            use_container_width=True, 
            width=180
        )
        app = option_menu(
            menu_title= 'PRICE SCOPE',
            options=['Home', 'Account', 'About', 'Contact'],
            icons=['house-fill','person-circle','chat-fill','info-circle-fill'],
            menu_icon='🏡',
            default_index=0,
            styles={
                "container": {"padding": "5!important", "background-color": 'black'},
                "icon": {"color": "white", "font-size": "23px"}, 
                "nav-link": {"color": "white", "font-size": "20px", "text-align": "left", "margin": "0px", "--hover-color": "blue"},
                "nav-link-selected": {"background-color": "#02ab21"},
            }
        )
        return app

# Main navigation logic
def main():
    # If user is not logged in (either on login or signup page)
    if st.session_state["current_page"] in ["login", "signup"]:
        if st.session_state["current_page"] == "signup":
            signup_page()  # Show signup page
        elif st.session_state["current_page"] == "login":
            login_page()  # Show login page
    
    # If the user is logged in
    else:
        # Display the sidebar for logged-in users
        app = sidebar_menu()

        if app == "Home":
            st.session_state["current_page"] = "home"
            home.home_page()  # Call the home page function from home.py
        elif app == "Account":
            st.session_state["current_page"] = "account"
            account_page()  # Account page function (where user details are shown)
        elif app == "About":
            st.session_state["current_page"] = "about"
            about.app()  # About page function
        elif app == "Contact":
            st.session_state["current_page"] = "contact"
            contact.app()  # Contact page function
        elif app == "Report":
            st.session_state["current_page"] = "report"
            report.app() # type: ignore
        elif app == "Logout":
            # Log out the user and reset session state
            del st.session_state["user"]  # Clear user session data
            st.session_state["current_page"] = "login"  # Go back to login page
            st.rerun()  # Rerun the app to reflect changes

# Run the app
if __name__ == "__main__":
    main()
