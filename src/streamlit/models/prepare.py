##############################################
# Import libraries
##############################################

import pandas as pd
import numpy as np
import textblob as tb
from collections import Counter

import spacy
from spacy.cli import download
import re
import joblib
import os
import nltk

###############################################
# Download necessary NLTK data files
###############################################
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('brown')
nltk.download('wordnet')
##############################################
# Load the spaCy model
##############################################

download("en_core_web_sm")
nlp = spacy.load("en_core_web_sm")



##############################################
# Functions
##############################################

def load_tfidf_vectorizer():
    '''
    This function loads the TF-IDF vectorizer from a pickle file
    Returns:
        The loaded TF-IDF vectorizer
    '''
    # Récupère le chemin absolu vers le dossier courant (où se trouve prepare.py)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    vectorizer_path = os.path.join(current_dir, 'tfidf', 'tfidf_vectorizer.pkl')
    return joblib.load(vectorizer_path)

def load_tfidf_vectorizer_multiclass():
    '''
    This function loads the TF-IDF vectorizer from a pickle file
    Returns:
        The loaded TF-IDF vectorizer
    '''
    # Récupère le chemin absolu vers le dossier courant (où se trouve prepare.py)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    vectorizer_path = os.path.join(current_dir, 'tfidf', 'tfidf_vectorizer_multiclass.pkl')
    return joblib.load(vectorizer_path)

def extract_polarity_words(text):
    '''
    This function extracts the adjectives and verbs from a text

    Args:
        text: The input text
    
    Returns:
        The extracted adjectives and verbs
    '''
    blob = tb.TextBlob(text)
    words_with_tags = blob.tags  # Liste de tuples (mot, tag)

    # Extraire les adjectifs (JJ) et les verbes (VB)
    polarity_words = [word for word, tag in words_with_tags if tag.startswith("JJ") or tag.startswith("VB")]

    return polarity_words if polarity_words else None

def clean_text(text):
    '''
    This function cleans the text by removing stopwords, punctuation, numbers, and short words

    Args:
        text: The input text

    Returns:
        The cleaned text
    '''
    text = text.lower()  # Convertir en minuscule
    text = re.sub(r"\b\w*\d\w*\b", "", text)  # Supprimer les mots contenant des chiffres
    text = re.sub(r"[^\w\s]", "", text)  # Supprimer la ponctuation
    text = re.sub(r"(.)\1{2,}", r"\1", text)  # Supprimer les répétitions de lettres ex: 'aaaa' -> 'a'
    text = " ".join([word for word in text.split() if len(word) > 2])  # Supprimer les mots courts (moins de 3 lettres)
    return text.strip()

def remove_proper_nouns(text):
    '''
    This function removes proper nouns from the text
    
    Args:
        text: The input text
    
    Returns:
        The text without proper nouns
    '''
    doc = nlp(text)
    filtered_words = [token.text for token in doc if token.pos_ != "PROPN"]  # Supprimer les noms propres
    return " ".join(filtered_words)

def keep_only_key_pos(text):
    '''
    This function keeps only the key parts of speech (NOUN, VERB, ADJ) from the text

    Args:
        text: The input text

    Returns:
        The text with only the key parts of speech
    '''
    doc = nlp(text)
    filtered_words = [token.text for token in doc if token.pos_ in ["NOUN", "VERB", "ADJ"]]
    return " ".join(filtered_words)


def clean_text_exclude_stopwords(text):
    '''
    This function cleans the text by removing stopwords, punctuation, numbers, and short words

    Args:
        text: The input text
    
    Returns:
        The cleaned text
    '''
    doc = nlp(text.lower())  # Tokenisation et minuscule
    filtered_words = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
    return filtered_words

def lemmatize_text(text):
    '''
    This function lemmatizes the text
    
    Args:
        text: The input text
        
    Returns:
        The lemmatized text
    '''
    if not isinstance(text, str):  # Vérifier si `text` est bien une chaîne de caractères
        return []  # Retourner une liste vide si `text` est NaN ou float
    doc = nlp(text.lower())  # Tokenisation + minuscule
    lemmatized_words = [token.lemma_ for token in doc if not token.is_stop]
    return lemmatized_words  # Retourne une liste de mots lemmatisés

##############################################

tfidf_vectorizer = load_tfidf_vectorizer()
tfidf_vectorizer_multiclass = load_tfidf_vectorizer_multiclass()

def prepare(df, model=tfidf_vectorizer):
    '''
    Prépare les données pour la prédiction.

    Args:
        df (pd.DataFrame): données brutes avec colonnes Content, dates.experiencedDate, dates.publishedDate
        model: vecteur TF-IDF entraîné

    Returns:
        np.ndarray : données prêtes à être injectées dans le modèle
    '''

    # Vérification des colonnes requises
    df['polarity'] = df['Content'].apply(lambda x: tb.TextBlob(str(x)).sentiment.polarity)
    df['subjectivity'] = df['Content'].apply(lambda x: tb.TextBlob(str(x)).sentiment.subjectivity)
    df['polarity_words'] = df['Content'].apply(extract_polarity_words)

    # Dates + jours entre les deux
    df["dates.experiencedDate"] = pd.to_datetime(df["dates.experiencedDate"], errors="coerce").dt.date
    df["dates.publishedDate"] = pd.to_datetime(df["dates.publishedDate"], errors="coerce").dt.date
    df["days_diff"] = (pd.to_datetime(df["dates.publishedDate"]) - pd.to_datetime(df["dates.experiencedDate"])).dt.days

    # Nettoyage + NLP
    df["Content_cleaned"] = df["Content"].apply(lambda x: clean_text(str(x)))
    df["Content_cleaned"] = df["Content_cleaned"].apply(remove_proper_nouns)
    df["Content_cleaned"] = df["Content_cleaned"].apply(keep_only_key_pos)

    df['punctuation'] = df['Content'].apply(lambda x: re.findall(r'[^\w\s]', str(x)))
    df['tokenized'] = df['Content_cleaned'].apply(clean_text_exclude_stopwords)
    df['lemmatized'] = df['Content_cleaned'].apply(lemmatize_text)

    # 🧠 Convertir la liste en string pour vectorisation
    df["lemmatized_str"] = df["lemmatized"].apply(lambda x: " ".join(x) if isinstance(x, list) else str(x))
    df["word_count"] = df["Content_cleaned"].apply(lambda x: len(str(x).split()))
    df["Content_cleaned"] = df["Content_cleaned"].fillna("")

    # TF-IDF vectorisation
    tfidf_matrix = model.transform(df["lemmatized_str"])
    df["vectorized"] = list(tfidf_matrix.toarray())
    df["vectorized_sum"] = df["vectorized"].apply(np.sum)

    X_vectorized = np.vstack(df["vectorized"].values)
    num_features = ["polarity", "subjectivity", "word_count", "days_diff", "vectorized_sum"]
    X_num = df[num_features].fillna(0).values
    X_final = np.hstack([X_vectorized, X_num])

    return X_final