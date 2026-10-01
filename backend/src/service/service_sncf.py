import os
from datetime import datetime

import requests
from modele_lignes import Gare


class ServiceSNCF:
    """Centralise les appels HTTP à l'API SNCF/Navitia."""

    def __init__(
        self,
        token: str | None = None,
        couverture: str = "sncf",
        session: requests.Session | None = None,
    ) -> None:
        self.token = token if token is not None else os.getenv("TOKEN_SNCF")
        if not self.token:
            raise ValueError("Définir TOKEN_SNCF ou fournir un token au constructeur.")
        self.url_base = f"https://api.sncf.com/v1/coverage/{couverture}"
        self.session = session if session is not None else requests.Session()

    def _get(self, chemin: str, params: dict) -> dict:
        reponse = self.session.get(
            f"{self.url_base}/{chemin}",
            params=params,
            auth=(self.token, ""),
            timeout=15,
        )
        reponse.raise_for_status()
        return reponse.json()

    def rechercher_gares(self, query: str) -> list[Gare]:
        """Recherche de gares pour l'autocomplétion."""
        if not query or not query.strip():
            return []
        donnees = self._get("places", {"q": query.strip(), "type[]": "stop_area"})
        return [
            Gare(place["stop_area"]["id"], place["stop_area"]["name"])
            for place in donnees.get("places", [])
            if place.get("stop_area")
        ]

    def obtenir_gare(self, id_sncF: str) -> Gare:
        """Récupère une gare par identifiant ; lève ValueError si inconnue."""
        if not id_sncF:
            raise ValueError("L'identifiant de gare est obligatoire.")
        reponse = self.session.get(
            f"{self.url_base}/stop_areas/{id_sncF}",
            auth=(self.token, ""),
            timeout=15,
        )
        if reponse.status_code == 404:
            raise ValueError(f"Gare SNCF inconnue : {id_sncF}")
        reponse.raise_for_status()
        gares = reponse.json().get("stop_areas", [])
        if not gares:
            raise ValueError(f"Gare SNCF inconnue : {id_sncF}")
        return Gare(gares[0]["id"], gares[0]["name"])

    def _trajets(self, depart_id: str, arrivee_id: str, date_depart: datetime) -> list[dict]:
        if depart_id == arrivee_id:
            return []
        if not isinstance(date_depart, datetime):
            raise TypeError("date_depart doit être un datetime.")
        donnees = self._get(
            "journeys",
            {
                "from": depart_id,
                "to": arrivee_id,
                "datetime": date_depart.strftime("%Y%m%dT%H%M%S"),
                "datetime_represents": "departure",
            },
        )
        return [
            trajet for trajet in donnees.get("journeys", [])
            if any(section.get("type") == "public_transport"
                   for section in trajet.get("sections", []))
        ]

    def verifier_trajet_possible(
        self, depart_id: str, arrivee_id: str, date_depart: datetime
    ) -> bool:
        return bool(self._trajets(depart_id, arrivee_id, date_depart))

    def obtenir_duree_trajet(
        self, depart_id: str, arrivee_id: str, date_depart: datetime
    ) -> int:
        """Durée minimale en secondes des trajets proposés comportant un transport."""
        trajets = self._trajets(depart_id, arrivee_id, date_depart)
        if not trajets:
            raise ValueError("Aucun trajet ferroviaire possible à cette date.")
        return min(trajet["duration"] for trajet in trajets)
