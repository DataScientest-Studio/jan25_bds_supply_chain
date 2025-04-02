import streamlit as st
from PIL import Image


st.set_page_config(
    page_title="Accueil",
    page_icon="🏠",
    layout="wide"
)

st.title("Home - Trustpilot Project")

st.write("Welcome to our Streamlit application!")
st.write("You can navigate through the different pages using the navigation bar on the left.")

st.header("About")
st.write("This application was created as part of the Machine Learning Engineer certification project by DataScientest and École des Mines de Paris. Its purpose is to apply the knowledge acquired during the training. The goal is to create a data visualization application using Streamlit.")

st.header("Features")
st.write("Here are the features of the application:")
st.write("- Sentiment Analysis: Analyze the sentiment of a comment.")
st.write("- Analysis History: View the history of sentiment analyses.")

st.header("Technologies")
st.write("The technologies used for this project are:")
st.write("- Python")
st.write("- Torch")
st.write("- Bert")
st.write("- TextBlob")
st.write("- Scikit-learn")
st.write("- XGBoost")
st.write("- Streamlit")
st.write("- Matplotlib")
st.write("- Seaborn")
st.write("- Pandas")
st.write("- Numpy")

st.header("Team")
st.write("This application was developed by:")
st.write("- Baptiste Audroin")
st.write("- Jean-Claude Nguyen")
st.write("- Steffen Morvan")

st.header("Contact")
st.write("For any questions or information, you can contact us on Slack.")
st.write("Thank you for visiting!")



# Footer with modern style
st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background-color: #f8f9fa;
        text-align: center;
        padding: 10px 0;
        font-size: 14px;
        color: #6c757d;
        border-top: 1px solid #dee2e6;
        box-shadow: 0 -2px 5px rgba(0, 0, 0, 0.1);
        z-index: 1000;
    }
    .footer a {
        color: #007bff;
        text-decoration: none;
    }
    .footer a:hover {
        text-decoration: underline;
    }
    </style>
    <div class="footer">
        Created by <a href="">Baptiste Audroin</a>, <a href="">Jean-Claude Nguyen</a> and <a href="">Steffen Morvan</a>
    </div>
    """,
    unsafe_allow_html=True
)