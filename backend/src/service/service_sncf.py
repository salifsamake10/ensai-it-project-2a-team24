import requests
import psycopg

TOKEN_SNCF = "ca7d129f-404d-4871-9e88-6af15fc22309"
URL_BASE = "https://api.sncf.com/v1"


def recuperer_gares():
    url = f"{URL_BASE}/coverage/sncf/stop_areas"

    toutes_les_gares = []
    start_page = 0

    while True:
        parametres = {
            "count": 100,
            "start_page": start_page
        }

        reponse = requests.get(
            url,
            params=parametres,
            auth=(TOKEN_SNCF, "")
        )

        reponse.raise_for_status()

        resultat = reponse.json()

        gares = resultat["stop_areas"]
        toutes_les_gares.extend(gares)

        if len(gares) < 100:
            break

        start_page += 1

    return toutes_les_gares


if __name__ == "__main__":
    gares = recuperer_gares()

    print("Nombre total de gares :", len(gares))
    print(gares[0])


def enregistrer_gares(gares):
    connexion = psycopg.connect(
        host="10.233.126.1",
        port=5432,
        dbname="defaultdb",
        user="user-lauraaimond",
        password="kxm4m7qw0kysmpx9ejvd"
    )

    curseur = connexion.cursor()

    for gare in gares:

        curseur.execute(
            """
            INSERT INTO public.station
                (id_sncf, nom)
            VALUES
                (%s, %s)
            ON CONFLICT (id_sncf) DO NOTHING
            """,
            (
                gare["id"],
                gare["name"]
            )
        )

    connexion.commit()

    curseur.close()
    connexion.close()

    print("Les gares ont été enregistrées !")


if __name__ == "__main__":
    gares = recuperer_gares()

    print("Nombre total de gares :", len(gares))

    enregistrer_gares(gares)
