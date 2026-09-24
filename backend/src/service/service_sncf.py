import requests


TOKEN_SNCF = "ca7d129f-404d-4871-9e88-6af15fc22309"

URL_BASE = "https://api.sncf.com/v1"


def rechercher_gares(recherche: str):

    url = f"{URL_BASE}/coverage/sncf/places"

    parametres = {
        "q": recherche,
        "type[]": "stop_area"
    }

    reponse = requests.get(
        url,
        params=parametres,
        auth=(TOKEN_SNCF, "")
    )

    return reponse.json()



if __name__ == "__main__":
    resultat = rechercher_gares("Rennes")

    print(resultat)