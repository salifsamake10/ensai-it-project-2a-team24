from datetime import datetime

from business_object.ligne_exploitation import LigneExploitation
from business_object.statut_trajet import StatutTrajet


class Trajet:
    """
    Business object représentant un trajet programmé
    sur une ligne d'exploitation.
    """

    def __init__(
        self,
        ligne: LigneExploitation,
        date_heure_depart: datetime,
        date_heure_arrivee: datetime,
        duree_minutes: int,
        capacite: int,
        tarif_base: float,
        statut: StatutTrajet = StatutTrajet.PLANIFIE,
        id_trajet: int | None = None,
        places_reservees: int = 0,
    ) -> None:
        self.id_trajet = id_trajet
        self.ligne = ligne
        self.date_heure_depart = date_heure_depart
        self.date_heure_arrivee = date_heure_arrivee
        self.duree_minutes = duree_minutes
        self.capacite = capacite
        self.places_reservees = places_reservees
        self.tarif_base = tarif_base
        self.statut = statut

    def __str__(self) -> str:
        return (
            f"Trajet {self.id_trajet} : de {self.date_heure_depart} "
            f"à {self.date_heure_arrivee} "
            f"({self.duree_minutes} min, {self.capacite} places, "
            f"{self.tarif_base}€)"
        )
