import streamlit as st
import re
import requests  # pip install requests

# Create an application.
def app():
    # Title Section
    st.title("📞 Contact Page")
    st.write("Feel free to reach out! Below are different ways you can contact me.")

    @st.dialog("Contact Me")
    def show_contact_form():
        # Import inside the function to avoid circular imports
        from contact import contact_form

        # Call the contact form function if needed
        contact_form()
    if st.button("✉️ Contact Me"):
            show_contact_form()

    # Apply Custom CSS for Background Styling
    st.markdown(
        """
        <style>
        /* Background Styling */
        .stApp {
            background-image: url('https://source.unsplash.com/1600x900/?communication,network');
            background-size: cover;
        }
        /* Enhance buttons */
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            font-size: 12px;
            border-radius: 8px;
            padding: 5px 15px;
        }
        /* Improve form inputs */
        input, textarea {
            border-radius: 8px;
            padding: 10px;
            border: 2px solid #4CAF50;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    

    # Social Media Section
    st.subheader("🌍 Connect with Me")
    st.markdown("""
    - 📧 **Email**: [n.kelvinnjuguna@gmail.com](mailto:n.kelvinnjuguna@gmail.com)
    - 💼 **LinkedIn**: [Kelvin Njuguna](https://www.linkedin.com/in/kelvin-njuguna-324b10222/)
    - 🔗 **GitHub**: [Kelvin340-cloud](https://github.com/kelvin340-cloud)
    - 🌐 **Portfolio**: [kelvin340-cloud.github.io](https://kelvin340-cloud.github.io/KelvinNjuguna.github.io/)
    """)

    # Footer Section
    st.markdown("---")
    st.write("© 2025 Kelvin Njuguna | All rights reserved.")


# Formspree endpoint (Replace with your actual endpoint)
FORMSPREE_URL = "https://formspree.io/f/moveapyw"

def is_valid_email(email):
    email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(email_pattern, email) is not None

def contact_form():
    st.subheader("Contact Me")

    with st.form("contact_form"):
        name = st.text_input("First Name")
        email = st.text_input("Email Address")
        message = st.text_area("Your Message")
        submit_button = st.form_submit_button("Submit")

    if submit_button:
        if not name:
            st.error("Please provide your name.", icon="🧑")
            st.stop()

        if not email:
            st.error("Please provide your email address.", icon="📨")
            st.stop()

        if not is_valid_email(email):
            st.error("Please provide a valid email address.", icon="📧")
            st.stop()

        if not message:
            st.error("Please provide a message.", icon="💬")
            st.stop()

        # Send the data to Formspree
        data = {"email": email, "name": name, "message": message}
        response = requests.post(FORMSPREE_URL, json=data)

        if response.status_code == 200:
            st.success("Your message has been sent successfully! 🎉", icon="🚀")
        else:
            st.error("There was an error sending your message.", icon="😨")

    
