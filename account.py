import streamlit as st

def account_page():
    if "user" in st.session_state:
        user = st.session_state["user"]
        # Split display name safely
        first_name = user.display_name.split()[0] if user.display_name else "Unknown"
        last_name = user.display_name.split()[1] if len(user.display_name.split()) > 1 else "Unknown"
        
        st.title(f"Welcome, {first_name} 👋")
        
        # Display account details
        st.subheader("Your Account Overview")
        st.write(f"**First Name:** {first_name}")
        st.write(f"**Last Name:** {last_name}")
        st.write(f"**Username:** {user.uid}")
        st.write(f"**Email:** {user.email}")
        
        # Add an option to sign out
        if st.button("Sign Out"):
            del st.session_state["user"]
            st.session_state["current_page"] = "home"  # Redirect to login page
            st.success("You have been signed out.")
            st.rerun()  # Rerun to show login page

    else:
        st.warning("Please log in to view your account.")

    # Footer Section
    st.markdown("---")
    st.write("© 2025 Kelvin Njuguna | All rights reserved.")
