import streamlit as st

def app():
    st.title("🏡 PriceScope")
    st.caption("Smarter Real Estate Decisions. Anytime. Anywhere.")

    # --- PROJECT OVERVIEW ---
    with st.expander("📌 **Project Overview**", expanded=True):
        st.write(
            """
            **PriceScope** is a **proptech startup** dedicated to transforming how property 
            decisions are made in the **Kenyan housing market**.  

            House hunting is often time-consuming, stressful, and expensive — buyers and renters 
            are forced to move from one neighborhood to another in search of the right property.  
            PriceScope reduces this burden by providing **data-driven property valuations** and 
            **real-time insights** that bring clarity and transparency to the process.  

            **✨ Key Offerings:**
            - 🏠 **Predictive Pricing Models** powered by Random Forest, Decision Trees & SVM  
            - 📊 **Comprehensive Valuation Reports** with current and projected property values  
            - 🔄 **What-If Scenario Analysis** to forecast impacts of neighborhood or economic changes  
            - 🌍 **User-Friendly Web App** built with Streamlit for easy accessibility  
            """
        )

    # --- ABOUT THE COMPANY ---
    st.subheader("🏢 About PriceScope")
    col1, col2 = st.columns([1, 2], gap="medium")

    with col1:
        st.image("./img/Logo1.png", width=180)  # Replace with your startup logo

    with col2:
        st.write(
            """
            ### **Driving Transparency in Real Estate**
            PriceScope was founded to make **property valuation transparent, reliable, and 
            accessible**. By combining **machine learning models** with **market data**, 
            we empower Kenyans to make informed housing decisions without endless physical 
            house hunting.  

            **🌍 Our Impact:**  
            - 🎯 Accurate guidance for **homebuyers & renters**  
            - 🏢 Data-driven tools for **agents & developers**  
            - 📈 Forecasting long-term **investment trends**  
            - 🛡️ Market transparency for **policymakers & regulators**  
            """
        )

    # --- ABOUT THE DEVELOPER ---
    st.subheader("👨‍💻 About the Developer")
    with st.expander("🔹 **Developer Background**", expanded=False):
        st.write(
            """
            ### **Njoroge Kelvin Njuguna**  
            📊 **Data Scientist | Data Analyst | Machine Learning Enthusiast**  

            I am passionate about building **data-driven solutions** that optimize decision-making 
            and drive sustainability. PriceScope reflects my vision of using technology to solve 
            real-world challenges in the housing market.  

            **Skills & Interests:**  
            - 📈 Data Visualization & Predictive Modeling  
            - 🗄️ Database Management  
            - 🌎 Web App Development  

            **🌐 [Portfolio Website](https://kelvin340-cloud.github.io/KelvinNjuguna.github.io/)**  
            """
        )

    # --- FOOTER ---
    st.markdown("---")
    st.write("© 2025 PriceScope | Built by Kelvin Njuguna")
