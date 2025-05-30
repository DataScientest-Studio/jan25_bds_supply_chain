import streamlit as st
import os
from PIL import Image
from scrapping import fetch_reviews
import pandas as pd

def resize_image(img, target_height):
    img = Image.open(img)
    width, height = img.size
    scale_factor = target_height / height
    new_width = int(width * scale_factor)
    return img.resize((new_width, target_height), Image.LANCZOS)

def resize_image2(img, target_height):
    img = Image.open(img)
    return img.resize((target_height, target_height), Image.LANCZOS)


# Titre et description
st.title("🖥️ Webscrapping")
st.header("Cette page permet de présenter le webscrapping de TrustPilot utilisé afin d'entraîner nos modèles.")
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Présentation", "Déséquilibre", "Solution", "Scrapping", "DF Final"])
with tab1:
    # Création de colonnes
    col1, col2 , col3 = st.columns([1, 1, 3])

    with col1:
        st.write("\n\n\n\n\n\nLangue sélectionnée : Anglais")

    with col2:
        st.image(resize_image("src/streamlit/img/flag_en.jpg", 200), use_container_width=True)

    with col3:
        st.write("\n\n\nUniverselle et répandue sur TrustPilot")

    st.empty()

    # Affichage des logos
    st.write("Nous nous sommes entraînés avec les avis des sites d'entreprises de mobilier suivantes : (entreprises avec beaucoup de notes)")

    logo_folder = "src/streamlit/img/logo_scrapping"
    files = os.listdir(logo_folder)

    # Calculer le nombre de logos et ajuster la taille
    logos_per_row = 7  # Nombre d'images par ligne
    rows = [files[i:i + logos_per_row] for i in range(0, len(files), logos_per_row)]

    # Affichage des images par ligne
    for row in rows:
        cols = st.columns(len(row))  # Créer une colonne pour chaque logo
        for col, file in zip(cols, row):
            with col:
                image = resize_image2(f"{logo_folder}/{file}", 100)  
                st.image(image, use_container_width=False)

with tab2:
    st.text("On peut facilement se rendre compte que les avis sont déséquilibrés avec une majorité de note extrême 1 ou 5, avec une sous \
representation des notes intermédiaires comme 2, 3, et 4.")
    st.image('src/streamlit/img/avis.png')

with tab3:
    st.write("Notre solution a donc été de scrapper le nombre maximum de commentaires de la catégorie la moins représentée pour chaque marque.")
    st.image('src/streamlit/img/equilibre.png')
    st.write("Ainsi notre dataset est équilibré avec le même nombre d'avis par classe.")

with tab4:

    st.subheader("🔍 Scraper les avis TrustPilot")
    st.text("Voici des exemple de scrapping simple que l'on peut réaliser :")
    # Choix du site à scraper
    sites_predefinis = ["www.dfs.co.uk", "www.gettington.com", "roomstogo.com", "theroomplace.com", "www.gardner-white.com", "www.icanvas.com",
               "www.raymourflanigan.com", "vivint.com",  "www.bluestoneperennials.com",  'nfm.com', "www.scs.co.uk", "www.made.com"]

    selection = st.selectbox("Sélectionnez un site :", sites_predefinis + ["Autre"])

    # Si "Autre" est sélectionné, afficher un champ de texte pour entrer un site
    if selection == "Autre":
        site = st.text_input("Entrez un site :", "")
    else:
        site = selection

    # Lancer le scraping
    if st.button("Lancer le scraping"):
        with st.spinner("Scraping en cours..."):
            reviews = fetch_reviews(site)
            st.success(f"{len(reviews)} avis récupérés avec succès.")
            st.write(reviews)
with tab5:
    st.subheader("📊 DataFrame Final")
    st.text("Notre DataFrame final est bien plus complexe avec plus de 58 000 avis\
 et 23  obtenues via l'API TrustPilot.\n\
Voici une version raccourcie :")
    # print(os.getcwd())  # Affiche le chemin du répertoire actuel
    df_short = pd.read_csv(r"src/streamlit/reviews_FINAL_short.csv", index_col=0)
    st.write(df_short)


# Footer avec style moderne
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
