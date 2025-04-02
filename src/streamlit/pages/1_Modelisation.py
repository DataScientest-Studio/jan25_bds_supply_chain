import streamlit as st

import streamlit as st

st.title("📊 Modélisation des modèles de Machine Learning et de Deep Learning")

st.write("XGBOOST - Binaire")
with st.expander("📌 **Résumé de la performance du modèle**", expanded=False):
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🔢 Distribution des classes")
        st.write("Répartition stable dans les datasets `train` et `test` :")
        st.markdown("- **60%** de **négatifs** (0)  \n- **40%** de **positifs** (1)")
        st.image("src/streamlit/img/distribution.png", caption="Distribution des classes dans y_test_bin", use_container_width=True)

    with col2:
        st.markdown("### 📈 Matrice de confusion - Modèle XGBoost binaire")
        st.image("src/streamlit/img/XGBoost - Binaire_confusion_matrix.png", caption="Matrice de confusion", use_container_width=True)
        st.markdown("> ✅ Modèle entraîné sur un dataset à 2 classes.")

    st.markdown("---")

    st.markdown("### 📊 Métriques principales")

    st.code("""accuracy  : 0.862
roc_auc   : 0.929
f1_score  : 0.832""", language="python")

with st.expander("⚙️ Optimisation des hyperparamètres", expanded=False):
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🔍 Hyperparamètres testés via `GridSearchCV`")
        st.markdown("""
- `n_estimators` : 50, 100, 200  
- `max_depth` : 3, 6, 9  
- `learning_rate` : 0.01, 0.1, 0.3
        """)

    with col2:
        st.markdown("### ✅ Meilleurs paramètres trouvés :")
        st.markdown("""
- `n_estimators` : **200**  
- `max_depth` : **9**  
- `learning_rate` : **0.1**
        """)
        st.markdown("🎯 **Best Accuracy** : `0.9248`")

with st.expander("🎚️ Seuil de décision (`threshold`) personnalisé", expanded=False):
    st.markdown("Le modèle retourne une **probabilité** de classe positive (1).")
    st.markdown("Par défaut, le seuil est fixé à `0.5`. Mais on peut l'ajuster selon l'objectif :")

    st.markdown("""
- 🔺 **Augmenter le seuil** → Moins de faux positifs  
- 🔻 **Réduire le seuil** → Moins de faux négatifs  
- 🎯 **Trouver le seuil optimal F1**
    """)

    st.image("src/streamlit/img/XGBoost - Binaire_fp_fn_threshold.png", caption="Évolution de la précision, du rappel et du F1 Score selon le seuil", use_container_width=True)

    st.markdown("#### ✅ Seuil optimal trouvé : `0.41`")
    
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