import streamlit as st
import pandas as pd

st.title("📝 Objectivité des commentaires")
st.subheader("Notre modèle s'est entraîné et a été testé sur plusieurs milliers d'avis, mais ces derniers sont-ils toujours objectifs ?")

df = pd.read_csv("src/check_predict.csv")
tab1, tab2 = st.tabs(["Tests", "Conclusion"])
with tab1:
    # Interface de sélection
    colh1, colh2, colh3, colh4, colh5 = st.columns([10, 10, 5, 5, 10])
    mode1 = "Écart réel/prédit"
    mode2 = "Valeur réelle et prédite direct"

    with colh1:
        n_avis = st.number_input("Nombre de commentaires", min_value=1, max_value=10, value=2)

    with colh2:
        mode = st.selectbox("", [mode1, mode2])

    if mode == mode1:
        with colh3:
            try_pred = st.checkbox("Prédire soi-même")

        with colh4:
            is_abs = st.checkbox(label_visibility="hidden", label="")

        with colh5:
            ecart = st.number_input(
                "Écart absolu" if is_abs else "Écart",
                min_value=0 if is_abs else -4,
                max_value=4,
                value=3 if is_abs else -2
            )

    elif mode == mode2:
        with colh3:
            real = st.number_input("Note réelle", min_value=1, max_value=5, value=2)

        with colh4:
            pred = st.number_input("Note prédite", min_value=1, max_value=5, value=4)

    # Gestion de l'affichage des commentaires en mode 1
    if mode == mode1:
        # Vérification si les commentaires sont déjà stockés dans session_state
        if "fixed_comments" not in st.session_state or st.session_state.get("last_mode") != mode or st.session_state.get("n_avis") != n_avis or st.session_state.get("ecart") != ecart:
            df_check = df[abs(df["pred_error"]) == abs(ecart)] if is_abs else df[df["pred_error"] == ecart]
            st.session_state.fixed_comments = df_check.sample(n=min(n_avis, len(df_check))).to_dict(orient="records") if not df_check.empty else []
            st.session_state.last_mode = mode
            st.session_state.n_avis = n_avis
            st.session_state.ecart = ecart


        # print("WOWO ", st.session_state.estime)
        for index, row in enumerate(st.session_state.fixed_comments):
            col1, col2, col3 = st.columns([1, 1, 1])
            
            if try_pred:
                with col2:
                    # if st.session_state.estime:
                    note_estime = st.selectbox(
                        "Note estimée :", [1, 2, 3, 4, 5],
                        key=f"pred_{index}",
                        index = None,
                        placeholder="Estimer la note vous-même"
                        )
            else :
                note_estime = 10

            with col1:
                if try_pred & (note_estime == None):
                    text_real = st.write(f"⭐ Note réelle : ❓")
                else:
                    text_real = st.write(f"⭐ Note réelle : {row['real']}")

            
                
                # # Si la note estimée n'est pas vide, on affiche les notes réelle et prédite
                # if note_estime != "":
                #     with col1:
                #         text_real = st.write(f"⭐ Note réelle : {row['real']}")

                #     with col3:
                #         text_pred = st.write(f"🔮 Note prédite : {row['predict']}")

            with col3:
                if try_pred & (note_estime == None)  :
                    text_pred = st.write(f"🔮 Note prédite : ❓")
                else:
                    text_pred =st.write(f"🔮 Note prédite : {row['predict']}")

            st.write(f"**Commentaire :** {row['text']}")
            st.divider()

    # Gestion de l'affichage des commentaires en mode 2 (Dynamique)
    elif mode == mode2:
        df_check = df[(df["real"] == real) & (df["predict"] == pred)]
        for index, row in df_check.sample(n=min(n_avis, len(df_check))).iterrows():
            col1, col2 = st.columns([1, 1])

            with col1:
                a = st.write(f"⭐ Note réelle : {row['real']}")

            with col2:
                st.write(f"🔮 Note prédite : {row['predict']}")

            st.write(f"**Commentaire :** {row['text']}")
            st.divider()

with tab2:
    st.write("Nous avons pu observer que les notes prédites sont souvent très proches des notes réelles, mais il y a tout de même des cas où la note prédite est très éloignée de la note réelle.")
    st.write("Cela peut être dû à plusieurs facteurs :")
    st.write("- Le modèle n'a pas été entraîné sur suffisamment d'avis pour apprendre les nuances du langage.")
    st.write("- Les avis sont parfois biaisés ou peu représentatifs.")
    st.write("- Le modèle peut avoir des difficultés à comprendre le contexte ou l'ironie dans certains commentaires.")
    st.write("Il est donc important de garder à l'esprit que même si le modèle est performant, il peut encore faire des erreurs.")

    st.write("")
    st.write("Cependant, pour des écarts prédiction/réel importants, notre modèle semble plus proche de la réalité.")
    st.write("Ainsi ce dernier peut être efficace pour détecter des avis dont la note n'est pas représentative.")

# Footer
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
        Créé par <a href="">Baptiste Audroin</a>, <a href="">Jean-Claude Nguyen</a> et <a href="">Steffen Morvan</a>
    </div>
    """,
    unsafe_allow_html=True
)
