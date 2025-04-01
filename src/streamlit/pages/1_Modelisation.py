import streamlit as st

st.title("📊 Modélisation")

st.write("Cette page permet de visualiser les différentes étapes de modélisation du projet.")
st.write("Les différentes étapes de modélisation sont les suivantes :")
st.write("- Chargement des données")
st.write("- Prétraitement des données")
st.write("- Entraînement des modèles")
st.write("- Évaluation des modèles")
st.write("- Sélection du modèle final")
st.write("- Sauvegarde du modèle final")

st.header("📈 Performance des modèles")
st.write("Voici un aperçu de la performance des modèles entraînés :")
st.write("Modèle à 5 classes")
st.write("Matrice de confusion :")

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