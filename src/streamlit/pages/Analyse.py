import streamlit as st
from transformers import pipeline

st.title("📝 Analyse de Sentiment")

sentiment_pipeline = pipeline("sentiment-analysis")
commentaire = st.text_area("Entrez un commentaire ici")
if st.button("Analyser"):
    if commentaire:
        resultat = sentiment_pipeline(commentaire)
        sentiment = resultat[0]['label']
        score = resultat[0]['score']
        st.write(f"Sentiment : {sentiment} (Score: {score:.2f})")
    else:
        st.warning("Entrez un texte.")


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