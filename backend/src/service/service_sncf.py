import requests
from dotenv import load_dotenv
import os

load_dotenv()

def rechercher_gares(recherche: str):

    url = f"{os.getenv('URL_BASE')}/coverage/sncf/places"

    parametres = {
        "q": recherche,
        "type[]": "stop_area"
    }

    reponse = requests.get(
        url,
        params=parametres,
        auth=(os.getenv('TOKEN_SNCF'), "")
    )

    return reponse.json()



if __name__ == "__main__":
    resultat = rechercher_gares("Rennes")

    print(resultat)