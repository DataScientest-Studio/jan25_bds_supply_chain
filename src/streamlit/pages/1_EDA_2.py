import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from sklearn.preprocessing import MinMaxScaler
import textblob as tb
import spacy
import en_core_web_sm


# Fonction 1 : Chargement des données depuis un fichier CSV
# @st.cache_data mémorise le résultat pour ne pas refaire les calculs à chaque fois
@st.cache_data      
def load_data():     
    df = pd.read_csv("src/reviews_FINAL.csv")
    df.rename(columns={'text': 'Content', 'rating': 'Rating', 'language': 'Language'}, inplace=True)
    suppr = ['pending', 'filtered','labels.merged.businessIdentifyingName', 'labels.verification.hasDachExclusion', 'location.id', 
             'location.name', 'location.urlFormattedName','Language','labels.verification.isVerified','title', 'consumer.id', 
             'consumer.isVerified','consumer.displayName', 'consumer.imageUrl','consumer.numberOfReviews','consumer.countryCode',
             'consumer.hasImage','reply.message', 'reply.publishedDate','reply.updatedDate','consumersReviewCountOnSameDomain',
             'consumersReviewCountOnSameLocation', 'Brand','dates.updatedDate',"id", "hasUnhandledReports", "labels.verification.verificationSource",
             "labels.verification.createdDateTime", "labels.verification.reviewSourceName", "labels.verification.verificationLevel", "report"]
    df = df.drop(columns=suppr)
    return df

# Fonction 2 : Conversion en format datetime
# on appellera
# df = prepare_dates(df,'dates.publishedDate')
# df = prepare_dates(df, 'dates.experiencedDate')
@st.cache_data
def prepare_dates(df,col):
    df[col] = pd.to_datetime(df[col])
    return df

# Fonction 3 : Calcul de la longueur des commentaires en nombre de mots
# on appellera :
# df = add_comment_length(df, 'Content')
@st.cache_data
def add_comment_length(df,col):
    # Nb de mot par avis
    df['len'] = df[col].apply(lambda x: len(x.split())) 
    return df

# Fonction 4 : Différence en jours entre deux dates (publication et expérience)
# on appellera :
# df = compute_day_diff(df, "dates.publishedDate", "dates.experiencedDate", "day_diff" )
@st.cache_data
def compute_day_diff(df, col1, col2, col_result):
    df[col_result] = pd.to_datetime(df[col1]) - pd.to_datetime(df[col2])
    df[col_result] = df[col_result].fillna(pd.Timedelta(0))
    df[col_result] = df[col_result].dt.days
    return df




# tb.TextBlob(): 
# Bibliothèque pour effectuer analyse de sentiment sur le texte.

# Fonction 5 : Calcul de la polarité des commentaires
# # La polarité varie entre -1 (très négatif) et 1 (très positif)
# on appellera :
# # df = compute_polarity(df, 'Content', 'polarity')
@st.cache_data
def compute_polarity(df, col, col_result):
    df[col_result] = df[col].apply(lambda x: tb.TextBlob(x).sentiment.polarity)
    return df


# Fonction 6 : Calcul de la subjectivité des commentaires
# subjectivité varie entre 0 (très objectif) et 1 (très subjectif)
 # on appellera :
 # df = compute_subjectivity(df, 'Content', 'subjectivity')
@st.cache_data
def compute_subjectivity(df, col, col_result):
    df[col_result] = df[col].apply(lambda x: tb.TextBlob(x).sentiment.subjectivity)
    return df


# Fonction 7 : Calcul des statistiques mensuelles
@st.cache_data
def compute_monthly_stats(df):
    # colonne qui combine année et mois :
    df['Year_Month'] = df['dates.publishedDate'].dt.to_period('M')
    monthly_avg_length = df.groupby('Year_Month')['len'].mean()
    monthly_avg_rating = df.groupby('Year_Month')['Rating'].mean()
    monthly_stats = pd.DataFrame({
        'Avg_Content_Length': monthly_avg_length,
        'Avg_Rating': monthly_avg_rating}).reset_index()
    monthly_stats['Year_Month'] = monthly_stats['Year_Month'].astype(str)
    return monthly_stats



#  Chargement des données 

# Fonction 1
df = load_data()
# Fonction 2
df = prepare_dates(df,'dates.publishedDate')
df = prepare_dates(df, 'dates.experiencedDate')
# Fonction 3
df = add_comment_length(df, 'Content')
# Fonction 4
df = compute_day_diff(df, "dates.publishedDate", "dates.experiencedDate", "day_diff" )
# Fonction 5
df = compute_polarity(df, 'Content', 'polarity')
# Fonction 6
df = compute_subjectivity(df, 'Content', 'subjectivity')
# Fonction 7
monthly_stats = compute_monthly_stats(df)


#  Interface STREAMLIT 

st.title("Visualisation")
st.sidebar.title("Sommaire")

pages=["DataVizualization", "Modélisation"]
page=st.sidebar.radio("Aller vers", pages)

if page == pages[0] : 
    st.write("Datavisualisation")
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Dataframe", "Evolutions", "Likes", "Jours d'attente", "Polarité et Subjectivité"])

with tab1:
    st.dataframe(df.head(10))

    if st.checkbox("Rappel Describe") :
        st.write("Shape: ", df.shape)
        st.write("Nombre de NaN : ")
        st.dataframe(df.isna().sum())
        st.write("Describe: ")
        st.dataframe(df.describe())

# 1. Distribution de la longueur des commentaires
    st.subheader("1. Distribution de la longueur des commentaires")
    max_len = int(df['len'].max())
    selected_max_len = st.slider("Choisir la longueur maximum des commentaires :", min_value=10, max_value=max_len, value=600)
    df_len_filtered = df[df['len'] <= selected_max_len]
    fig1, ax1 = plt.subplots(figsize=(6, 3))
    sns.histplot(df_len_filtered['len'], bins=50, kde=True, ax=ax1)
    ax1.set_xlim(0, selected_max_len)
    ax1.set_title("Distribution de la longueur des commentaires")
    ax1.set_xlabel("Nb de mots par commentaire")
    ax1.set_ylabel("Nb d'avis")
    st.pyplot(fig1)


# 2. Nombre de mots par note
    st.subheader("2.a. Distribution de la longueur des commentaires par note")
    mesure = st.selectbox(" Choisir Moyen par note ou Médian par note:", options=["Moyenne", "Médiane"])
    if mesure == "Moyenne":
        grouped = df.groupby("Rating")["len"].mean().reset_index()
    else:
        grouped = df.groupby("Rating")["len"].median().reset_index()
    fig2 = plt.figure(figsize=(6, 3))
    sns.barplot(x=grouped["Rating"], y=grouped["len"])
    plt.title(f"Nombre de mots par note ")
    plt.ylabel("Nb de mots par commentaire")   
    plt.xlabel("Note")     
    st.pyplot(fig2)

# 3. Relation entre Rating et longueur des commentaires
    st.subheader("2.b Distribution de la longueur des commentaires par note")
    max_y = st.slider("Choisir la longueur des commentaires :", min_value=100, max_value=1000, value=600, step=50)
    fig3 = plt.figure(figsize=(4, 4))
    sns.boxplot(x=df['Rating'], y=df['len'])
    plt.ylim(0, max_y)
    plt.title('Relation entre Rating et longueur des commentaires')
    plt.ylabel("Nb de mots par commentaire")        
    plt.xlabel("Note")     
    st.pyplot(fig3)

with tab2:

# 4. Évolution du nombre de commentaires par mois 
    st.subheader("3. Évolution du nombre de commentaires par mois par note")
    df['dates.publishedDate'] = pd.to_datetime(df['dates.publishedDate'])
    df["Year"] = df["dates.publishedDate"].dt.year
    df["Month"] = df["dates.publishedDate"].dt.month
    df["Day"] = df["dates.publishedDate"].dt.dayofweek + 1 
    ratings = sorted(df["Rating"].dropna().unique())
    selected_ratings = st.multiselect("Filtrer par note (Rating) :", ratings, default=ratings)
    filtered_df = df[df["Rating"].isin(selected_ratings)]
    fig4 = plt.figure(figsize=(7, 3))
    sns.histplot(
        x=filtered_df['dates.publishedDate'],
        hue=filtered_df['Rating'],
        bins=30,
        palette='viridis')
    plt.title("Nombre d'avis postés depuis 2016")
    plt.xlabel("Année")
    plt.ylabel("Nb d'avis")
    st.pyplot(fig4)

# 4.a. Évolution de la longueur moyenne des avis par note
    st.subheader("4.a. Évolution de la longueur moyenne des avis par note")
    fig5a = plt.figure(figsize=(18, 8))
    sns.scatterplot(x=monthly_stats['Year_Month'], y=monthly_stats['Avg_Content_Length'], size=monthly_stats['Avg_Rating'], sizes=(10, 200), legend=True)
    plt.xticks(rotation=90)  
    plt.title("Évolution de la longueur moyenne des commentaires par mois")
    plt.xlabel("Année-Mois")
    plt.ylabel("Longueur moyenne du commentaire")
    plt.grid()
    plt.legend(title="Moyenne du Rating", loc="upper left")
    st.pyplot(fig5a)


    # 4.b. Évolution interactive de la longueur moyenne des avis
    scaler = MinMaxScaler(feature_range=(10, 200))
    monthly_stats['Bubble_Size'] = scaler.fit_transform(monthly_stats[['Avg_Rating']])
    fig = px.scatter(
        data_frame=monthly_stats,
        x="Year_Month",
        y="Avg_Content_Length",
        size="Bubble_Size",  # On utilise ici la taille des bulles comme indicateur de la note moyenne
        hover_name="Year_Month",
        hover_data={"Avg_Content_Length": True, "Avg_Rating": True},
        title="4.b. Évolution interactive de la longueur moyenne des commentaires par mois",
        labels={"Avg_Content_Length": "Longueur moyenne du commentaire", "Avg_Rating": "Note moyenne"},
        height=600)
    fig.update_layout(
        xaxis_title="Année-Mois",
        yaxis_title="Longueur moyenne du commentaire",
        xaxis_tickangle=90,
        plot_bgcolor="white",
        legend_title_text="Taille des bulles = Note moyenne")
    st.plotly_chart(fig, use_container_width=True)



with tab3:

# 5.a. Nombre de likes par note
    st.subheader("5.a. Nombre de likes par note")
    fig7, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(x="Rating", y="likes", data=df, ax=ax)
    ax.set_title("Nombre de likes en fonction de la note")
    ax.set_xlabel("Note")
    ax.set_ylabel("Nombre de likes")
    st.pyplot(fig7)
    # 5.a.
    # Pour une note 1, ce graphique montre la moyenne du nombre de likes 
    # qui tourne autour de 0,11
    # avec un intervalle de confiance très faible ce qui signifie 
    # qu'il y a une très faible variabilité dans le nombre de likes donné.

# 5.b. Nombre de likes pour chaque note
    st.subheader("5.b. Nombre de likes pour chaque note")
    min_likes, max_likes = st.slider(
        "Filtrer la plage de likes :", 
        min_value=int(df['likes'].min()), 
        max_value=int(df['likes'].max()), 
        value=(int(df['likes'].min()), int(df['likes'].max())))
    filtered_df = df[(df['likes'] >= min_likes) & (df['likes'] <= max_likes)]
    fig8, ax = plt.subplots(figsize=(8, 6))
    sns.countplot(data=filtered_df, x='likes', hue='Rating', ax=ax)
    ax.set_title(f"Nombre de likes pour chaque note (entre {min_likes} et {max_likes})")
    ax.set_xlabel("Likes")
    ax.set_ylabel("Nombre d'avis")
    st.pyplot(fig8)
    # 5.b.
    # On voit bien que la plupart des avis ne reçoivent aucun likes.
    # et que les avis notés 5 sont ceux qui ont le plus de 0 likes (donc abcense de likes).
    # Pour les avis ayant 1 like ou plus, et ils sont peu, on voit 
    # # on voit que ce sont, à l'inverse, les avis notés 1 qui reçoivent le plus 1 like, et 2 likes et 3 likes.




with tab4: 

# 6. Nombre de jours d'attente par note
    st.subheader("6. Nombre de jours d'attente par note")
    df["day_diff"] = pd.to_datetime(df["dates.publishedDate"]) - pd.to_datetime(df["dates.experiencedDate"])
    df["day_diff"] = df["day_diff"].fillna(pd.Timedelta(0))
    df["day_diff"] = df["day_diff"].dt.days

    min_day, max_day = st.slider(
        "Filtrer la plage de jours entre l'expérience et la publication :",
        min_value=int(df["day_diff"].min()),
        max_value=int(df["day_diff"].max()),
        value=(int(df["day_diff"].min()), int(df["day_diff"].max())),
        key="slider1" )
    filtered_df = df[(df["day_diff"] >= min_day) & (df["day_diff"] <= max_day)]
    fig9a, ax = plt.subplots(figsize=(6, 4))
    sns.histplot(
        data=filtered_df,
        x='day_diff',
        hue='Rating',
        bins=50,
        multiple="stack",
        ax=ax)
    ax.set_title("Nombre de jours d'attente pour chaque note")
    ax.set_xlabel("Jours d'attente")
    ax.set_ylabel("Nombre d'avis")
    st.pyplot(fig9a)

# 6. Nombre de jours d'attente par note
    st.subheader("6. Comparaison")
    df["day_diff"] = pd.to_datetime(df["dates.publishedDate"]) - pd.to_datetime(df["dates.experiencedDate"])
    df["day_diff"] = df["day_diff"].fillna(pd.Timedelta(0))
    df["day_diff"] = df["day_diff"].dt.days

    min_day, max_day = st.slider(
        "Filtrer la plage de jours entre l'expérience et la publication :",
        min_value=int(df["day_diff"].min()),
        max_value=int(df["day_diff"].max()),
        value=(int(df["day_diff"].min()), int(df["day_diff"].max())),
        key="slider2" )
    filtered_df = df[(df["day_diff"] >= min_day) & (df["day_diff"] <= max_day)]
    fig9a, ax = plt.subplots(figsize=(6, 4))
    sns.histplot(
        data=filtered_df,
        x='day_diff',
        hue='Rating',
        bins=50,
        multiple="stack",
        ax=ax)
    ax.set_title("Nombre de jours d'attente pour chaque note")
    ax.set_xlabel("Jours d'attente")
    ax.set_ylabel("Nombre d'avis")
    st.pyplot(fig9a)




with tab5:

# 7.a. Polarité moyenne par note
    st.subheader("7.a. Polarité moyenne par note")
    fig10, ax = plt.subplots(figsize=(6, 3))
    df.groupby('Rating')['polarity'].mean().plot(kind='bar', ax=ax)
    ax.set_title("Polarité moyenne par note")
    ax.set_xlabel("Note")
    ax.set_ylabel("Polarité (sentiment)")
    ax.grid(True)
    st.pyplot(fig10)

# 7.b. Subjectivité moyenne par note
    st.subheader("7.b. Subjectivité moyenne par note")
    fig11, ax = plt.subplots(figsize=(6, 3))
    df.groupby('Rating')['subjectivity'].mean().plot(kind='bar', ax=ax)
    ax.set_title("Subjectivité moyenne par note")
    ax.set_xlabel("Note")
    ax.set_ylabel("Subjectivité")
    ax.grid(True)
    st.pyplot(fig11)


# 8.a. Distribution de la polarité par commentaire par note 
    st.subheader("8.a. Distribution de la polarité par commentaire par note")
    ratings = sorted(df["Rating"].dropna().unique())
    selected_ratings = st.multiselect("Sélectionner les notes (Ratings) à afficher :", ratings, default=ratings, key="filter_polarity")
    filtered_df = df[df["Rating"].isin(selected_ratings)]
    fig_polarity, ax = plt.subplots(figsize=(8, 6))
    sns.histplot(data=filtered_df, x='polarity', hue='Rating', bins=30, multiple='stack', palette="viridis", ax=ax)
    ax.set_title("Distribution de la polarité par commentaire en fonction des notes sélectionnées")
    ax.set_xlabel("Polarité")
    ax.set_ylabel("Nombre de commentaires")
    st.pyplot(fig_polarity)
    # histogramme empilé.
    # -1 représente un avis très négatif et 1 un avis très positif.
    # neutre le plus de commentaires 
    # La majorité des commentaires notés 5 et 4 sont positifs ce qui est logique
    # mais La majorité des commentaires notés 1 sont un peu négatifs voire neutres
    # cad que les consommateurs emploient un ton plutôt neutre voire positif 
    # alors qu'ils ne sont vraiment pas contents...


# 8.b. Distribution de la subjectivité par commentaire par note 
    # bleu violet
    # cyan
    # vert clair
    # jaune
    st.subheader("8.b. Distribution de la subjectivité par commentaire par note")
    ratings = sorted(df["Rating"].dropna().unique())
    selected_ratings = st.multiselect("Sélectionner les notes (Ratings) à afficher :", ratings, default=ratings, key="filter_subjectivity")
    filtered_df = df[df["Rating"].isin(selected_ratings)]
    fig_subjectivity, ax = plt.subplots(figsize=(8, 6))
    sns.histplot(data=filtered_df, x='subjectivity', hue='Rating', bins= 60, multiple='stack', palette="viridis", ax=ax)
    ax.set_title("Distribution de la subjectivité par commentaire en fonction des notes sélectionnées")
    ax.set_xlabel("Subjectivité")
    ax.set_ylabel("Nombre de commentaires")
    st.pyplot(fig_subjectivity)
    # histogramme empilé
    # 0 représente un avis objectif. 1 : subjectif.
    # Toutes les notes sont bien réparties autour de 0,5 

#  Graphique 9 : Relation entre Polarité et Subjectivité par note 
    # beige
    # rose
    # violet rose
    # violet
    # bleu marine
    st.subheader("9. Relation entre Polarité et Subjectivité par note")
    selected_ratings_graph16 = st.multiselect("Filtrer par note (Rating) :", ratings, default=ratings, key="filter_16")
    filtered_df_graph16 = df[df["Rating"].isin(selected_ratings_graph16)]
    fig_relation, ax = plt.subplots(figsize=(8, 6))
    sns.scatterplot(data=filtered_df_graph16, x='polarity', y='subjectivity', hue='Rating', ax=ax)
    ax.set_title("Relation entre Polarité et Subjectivité par note")
    ax.set_xlabel("Polarité")
    ax.set_ylabel("Subjectivité")
    st.pyplot(fig_relation)
    
#  Graphique 10 : Comparaison entre Polarité et Subjectivité 
    # violet
    # bleu marine 
    # vert foncé
    # vert
    # vert clair 
    st.subheader("10. Comparaison entre Polarité et Subjectivité")
    polarity_min1, polarity_max1 = st.slider(
        "Filtrer par plage de polarité 1 :",
        min_value=float(df['polarity'].min()),
        max_value=float(df['polarity'].max()),
        value=(float(df['polarity'].min()), 0.0),
        step=0.01,
        key="filter_polarity_17_1")
    polarity_min2, polarity_max2 = st.slider(
        "Filtrer par plage de polarité 2 :",
        min_value=float(df['polarity'].min()),
        max_value=float(df['polarity'].max()),
        value=(0.0, float(df['polarity'].max())),
        step=0.01,
        key="filter_polarity_17_2")
    # Filtrer le DataFrame en fonction des deux plages de polarité sélectionnées
    filtered_df_graph17 = df[((df['polarity'] >= polarity_min1) & (df['polarity'] <= polarity_max1)) |
                            ((df['polarity'] >= polarity_min2) & (df['polarity'] <= polarity_max2))]
    # Calcul de la corrélation
    correlation = filtered_df_graph17[['polarity', 'subjectivity']].corr().iloc[0, 1]
    fig_comparison, ax = plt.subplots(figsize=(7, 5))
    sns.scatterplot(data=filtered_df_graph17, x='subjectivity', y='polarity', alpha=0.9, hue='polarity', palette="viridis", ax=ax)
    ax.set_title(f"Relation entre Subjectivité et Polarité (Corrélation = {correlation:.3f})")
    ax.set_xlabel("Subjectivité (0 = objectif, 1 = subjectif)")
    ax.set_ylabel("Polarité (-1 = négatif, +1 = positif)")
    ax.axhline(0, color='gray', linestyle='dashed', alpha=0.5)
    ax.axvline(0.5, color='gray', linestyle='dashed', alpha=0.5)
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', title="Polarité")
    st.pyplot(fig_comparison)

