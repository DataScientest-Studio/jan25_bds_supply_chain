import requests
import json
import pandas as pd
from bs4 import BeautifulSoup
import streamlit as st

# Liste des sites disponibles
BRANDS = ["www.dfs.co.uk", "www.gettington.com", "roomstogo.com", "theroomplace.com", "www.gardner-white.com"]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

BASE_URL = "https://www.trustpilot.com/review/{}"

def fetch_reviews(brand):
    url = BASE_URL.format(brand)
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code != 200:
        st.error(f"Impossible de récupérer les avis pour {brand} (code {response.status_code}).")
        return pd.DataFrame()
    
    soup = BeautifulSoup(response.text, "html.parser")
    script = soup.find("script", {"id": "__NEXT_DATA__"})
    
    if not script:
        st.error("Aucune donnée JSON trouvée sur cette page.")
        return pd.DataFrame()
    
    data = json.loads(script.string)
    reviews = data.get("props", {}).get("pageProps", {}).get("reviews", [])
    
    if not reviews:
        st.warning("Aucun avis trouvé.")
        return pd.DataFrame()
    
    df = pd.json_normalize(reviews)
    return df[["title", "text", "rating", "dates.publishedDate", "consumer.displayName"]]