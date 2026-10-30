import os
import pandas as pd
from recombee_api_client.api_client import RecombeeClient, Region
from recombee_api_client.api_requests import SetItemValues, Batch

# TODO 1: Configurare credentiale Recombee (la fel ca la Lab 02)
DB_NAME = 'denisacorfu-sdr-dev'
PRIVATE_TOKEN = os.environ['RECOMBEE_PRIVATE_TOKEN']
REGION = Region.EU_WEST

client = RecombeeClient(DB_NAME, PRIVATE_TOKEN, region=REGION)

# TODO 2: Incarcarea aceluiasi dataset folosit la Lab 02
PATH_DATASET = 'imdb_top_1000.csv'

def send_batch(requests):
    """Trimite un lot si opreste scriptul daca Recombee a respins vreun item"""
    raspunsuri = client.send(Batch(requests))
    erori = [r for r in raspunsuri if r['code'] not in (200, 201)]
    if erori:
        raise SystemExit(f"Eroare: {len(erori)} item-uri au fost respinse: {erori}")

def send_items():
    """Functie care citeste dataset-ul si trimite item-urile in Recombee"""
    df = pd.read_csv(PATH_DATASET)
    # In CSV, filmul Apollo 13 are valoarea 'PG' in coloana Released_Year
    df.loc[df['Series_Title'] == 'Apollo 13', 'Released_Year'] = 1995
    print(f"Se trimit {len(df)} item-uri in Recombee...")

    requests = []

    for index, row in df.iterrows():
        # TODO 3: Extrageti ID-ul unic al produsului din coloana corespunzatoare din CSV
        # Coloana item_id a fost adaugata in CSV, deoarece dataset-ul original nu are o coloana de ID
        item_id = str(row['item_id'])

        # TODO 4: Mapati proprietatile definite anterior cu valorile din randul curent
        properties = {
            "title": str(row['Series_Title']),
            "year": int(row['Released_Year']),
            "rating": float(row['IMDB_Rating']),
            "genre": str(row['Genre']),
            "director": str(row['Director']),
            "votes": int(row['No_of_Votes'])
        }

        # Adaugam request-ul de setare a valorilor pentru item
        # (SetItemValues creează automat item-ul dacă acesta nu există)
        requests.append(SetItemValues(item_id, properties, cascade_create=True))

        # Trimitem in loturi (batch) de cate 100 pentru eficienta
        if len(requests) == 100:
            send_batch(requests)
            requests = []
            print("S-a trimis un lot de 100 item-uri...")

    # Trimitem si restul ramanase (daca numarul total nu e multiplu de 100)
    if requests:
        send_batch(requests)
        print("S-a trimis ultimul lot de item-uri.")

    print("Toate item-urile au fost trimise cu succes!")

if __name__ == "__main__":
    send_items()
