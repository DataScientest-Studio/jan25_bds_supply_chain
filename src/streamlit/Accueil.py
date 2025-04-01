import streamlit as st
from PIL import Image


st.set_page_config(
    page_title="Accueil",
    page_icon="🏠",
    layout="wide"
)

st.title("Accueil - Projet Trustpilot")

st.write("Bienvenue sur notre application Streamlit !")
st.write("Vous pouvez naviguer dans les différentes pages grâce à la barre de navigation sur la gauche.")

st.header("À propos")
st.write("Cette application a été créée dans le cadre du projet de certification Machine Learning Engineer de DataScientest et l'École des mines de Paris. Elle a pour but de mettre en pratique les connaissances acquises durant la formation. L'objectif est de créer une application de visualisation de données en utilisant Streamlit.")

st.header("Fonctionnalités")
st.write("Voici les fonctionnalités de l'application :")
st.write("- Analyse de sentiment : Analyser le sentiment d'un commentaire.")
st.write("- Historique des analyses : Visualiser l'historique des analyses de sentiment.")

st.header("Technologies")
st.write("Les technologies utilisées pour ce projet sont :")
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


st.header("Équipe")
st.write("Cette application a été développée par :")
st.write("- Baptiste Audroin")
st.write("- Jean-Claude Nguyen")
st.write("- Steffen Morvan")

st.header("Contact")
st.write("Pour toute question ou information, vous pouvez nous contacter sur Slack")
st.write("Merci de votre visite !")



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
        Créé par <a href="">Baptiste Audroin</a>, <a href="">Jean-Claude Nguyen<a/> et <a href="">Steffen Morvan</a>
    </div>
    """,
    unsafe_allow_html=True
)