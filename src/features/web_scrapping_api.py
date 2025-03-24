import requests
import json
import csv
import time
from bs4 import BeautifulSoup

# Base URL for TrustPilot reviews
BASE_URL = "https://www.trustpilot.com/review/{}"

# Base URL used to send commands to the TrustPilot API
BASE_URL_JSON = "https://www.trustpilot.com/_next/data/businessunitprofile-consumersite-{}/review/{}.json?page={}&stars={}&businessUnit={}"

# List of brands scrapped
brand_list = [["www.dfs.co.uk", "www.gettington.com", "roomstogo.com", "theroomplace.com", "www.gardner-white.com", "www.icanvas.com"],
               ["www.raymourflanigan.com", "vivint.com",  "www.bluestoneperennials.com",  'nfm.com', "www.scs.co.uk", "www.made.com"]]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def flatten_json(nested_json, parent_key='', sep='.'):
    """
    Aplatir un JSON imbriqué.
    
    :param nested_json: Le JSON à aplatir (dictionnaire).
    :param parent_key: Clé parent pour le contexte récursif (laisser vide au départ).
    :param sep: Séparateur à utiliser entre les clés (par défaut ".").
    :return: Dictionnaire aplati.
    """
    items = []
    for key, value in nested_json.items():
        new_key = f"{parent_key}{sep}{key}" if parent_key else key
        if isinstance(value, dict):
            # Appel récursif pour aplatir les sous-dictionnaires
            items.extend(flatten_json(value, new_key, sep=sep).items())
        elif isinstance(value, list):
            # Si la valeur est une liste, la gérer différemment si nécessaire
            for i, item in enumerate(value):
                items.extend(flatten_json({f"{new_key}[{i}]": item}, '', sep=sep).items())
        else:
            items.append((new_key, value))
    return dict(items)

def fetch_reviews_from_jsonld(brand_list, BASE_URL_JSON = BASE_URL_JSON,
                              BASE_URL = BASE_URL,
                              version = "2.3286.0"):
    REGULAR_KEYS = ['id', 'filtered', 'pending', 'text', 'rating', 'labels.merged.businessIdentifyingName', 'labels.verification.isVerified', 'labels.verification.createdDateTime', 'labels.verification.reviewSourceName',
                    'labels.verification.verificationSource', 'labels.verification.verificationLevel', 'labels.verification.hasDachExclusion', 'title', 'likes', 'dates.experiencedDate', 'dates.publishedDate',
                    'dates.updatedDate', 'report.reasons[0]', 'report.reason', 'report.reviewVisibility', 'report.createdDateTime', 'report.source', 'hasUnhandledReports', 'consumer.id', 'consumer.displayName', 'consumer.imageUrl', 'consumer.numberOfReviews', 'consumer.countryCode', 'consumer.hasImage',
                    'consumer.isVerified', 'reply.message' , 'reply.publishedDate', 'reply.updatedDate','consumersReviewCountOnSameDomain', 'consumersReviewCountOnSameLocation', 'language', 'Brand',
                    'location.id', 'location.name', 'location.urlFormattedName']
    """Récupère les avis en extrayant les données JSON-LD des pages."""
    count = 0
    for j, brand_li in enumerate(brand_list):
        for i, brand in enumerate(brand_li): # Lister sur les différents site
            print(f"Récupération du numbres d'avis pour la marque {brand} ...")
            paginated_url = BASE_URL.format(brand)
            response = requests.get(paginated_url, headers=HEADERS)

            if response.status_code != 200:
                print(f"Erreur : impossible de se connecter à {paginated_url} (code {response.status_code}). Arrêt.")
                break

            soup = BeautifulSoup(response.text, "html.parser")
            
            # Recherche du script contenant le JSON-LD
            script = soup.find("script", {'data-business-unit-json-ld-dataset':"true"})
            if not script:
                print("Aucune donnée data-business-unit-json-ld-dataset trouvée sur cette page.")
                break
            data = json.loads(script.string)
            star_list = list()
            for star in range(0,6):
                star_list.append(int(data["@graph"]["mainEntity"]["csvw:tableSchema"]["csvw:columns"][star]["csvw:cells"][0]["csvw:value"]))
            max_reviews = int(min(star_list))
            count += max_reviews

            print("On ne gardera que les {} premiers avis, le limitant est le {} étoiles (total : {})".format(max_reviews,star_list.index(max_reviews)+1, count))
            time.sleep(0.1) # Pause pour éviter de surcharger le site
            for star in range(1,6):
                current_page = 1
                n_reviews = 0
                tried = 0
                print(f"Récupération des avis de la page {current_page} pour les avis de note {star}..")
                while (n_reviews < max_reviews):
                    
                    if current_page == 1:
                        paginated_url = BASE_URL.format(brand) + "?stars={}".format(star)
                    else:
                        paginated_url = BASE_URL_JSON.format(version, brand, current_page, star, brand)
                    response = requests.get(paginated_url, headers=HEADERS)

                    if response.status_code != 200:
                        print(f"Erreur : impossible de se connecter à {paginated_url} (code {response.status_code}). Arrêt.")
                        tried +=1 # Tempo longue en cas d'erreur, maximum 2 tentatives
                        time.sleep(30)
                        if tried == 1:
                            continue
                        elif tried == 2:
                            current_page += 1
                            continue
                        else:
                            break
                    tried = 0

                    soup = BeautifulSoup(response.text, "html.parser")
                    
                    # Recherche du script contenant le JSON-LD
                    script = soup.find("script", {"id": "__NEXT_DATA__"})
                    if not script:
                        print("Aucune donnée JSON-LD trouvée sur cette page.")
                        break

                    try:
                        data = json.loads(script.string)
                        # Vérifie si les avis sont présents
                        if (n_reviews == 0) & (i==0) & (star==1):
                            first_line = True
                        else:
                            first_line = False
                        for rev in data["props"]["pageProps"]["reviews"]:
                            reviews = flatten_json(rev)
                            reviews["Brand"] = brand
                            if "reply" in reviews.keys(): # Renommage de paramètre qui n'apparaissent que sur certains avis
                                del reviews["reply"]
                                reviews["reply.message"] = ""
                                reviews["reply.publishedDate"] = ""
                                reviews["reply.updatedDate"] = ""
                            if "location" in reviews.keys():
                                del reviews["location"]
                                reviews["location.id"] = ""
                                reviews["location.name"] = ""
                                reviews["location.urlFormattedName"] = ""
                            if 'labels.merged' in reviews.keys():
                                del reviews['labels.merged']
                                reviews['labels.merged.businessIdentifyingName'] = ""
                            if "report" in reviews.keys():
                                del reviews["report"]
                                reviews["report.reasons[0]"] = ""
                                reviews["report.reason"] = ""
                                reviews["report.reviewVisibility"] = ""
                                reviews["report.createdDateTime"] = ""
                                reviews["report.source"] = ""
                            if set(reviews.keys()) != set(REGULAR_KEYS):
                                print("Erreur dans les clés du dictionnaire")
                                print(f"On a en trop les clefs : {[key for key in reviews.keys() if key not in REGULAR_KEYS]}")
                                print(f"On a en moins les clefs : {[key for key in REGULAR_KEYS if key not in reviews.keys()]}")
                            save_reviews_to_csv(reviews, REGULAR_KEYS, filename=f"./reviews_folder/reviews_test_final_{j}.csv", first_line=first_line)
                            first_line = False
                            n_reviews += 1
                            if n_reviews == max_reviews:
                                break

                    except json.JSONDecodeError as e:
                        print(f"Erreur lors de la lecture des données JSON : {e}")
                        break

                    current_page += 1
                    time.sleep(0.1)  # Pause pour éviter de surcharger le site

    return reviews

def save_reviews_to_csv(reviews, REGULAR_KEYS, filename="reviews.csv", first_line=True):
    """Enregistre les avis dans un fichier CSV."""
    if first_line:
        with open(filename, mode="w", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=REGULAR_KEYS)
            writer.writeheader()
            writer.writerow(reviews)
    else:
        with open(filename, mode="a", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=REGULAR_KEYS)
            writer.writerow(reviews)

if __name__ == "__main__":
    print("Démarrage de la récupération des avis...")
    reviews = fetch_reviews_from_jsonld(brand_list)
