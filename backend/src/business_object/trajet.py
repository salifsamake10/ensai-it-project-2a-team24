from datetime import datetime

from business_object.ligne_exploitation import LigneExploitation


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
        id: int | None = None,
    ) -> None:
        self.id = id
        self.ligne = ligne
        self.date_heure_depart = date_heure_depart
        self.date_heure_arrivee = date_heure_arrivee
        self.duree_minutes = duree_minutes
        self.capacite = capacite
        self.tarif_base = tarif_base

    def __str__(self) -> str:
        return (
            f"Trajet {self.id} : de {self.date_heure_depart} "
            f"à {self.date_heure_arrivee} "
            f"({self.duree_minutes} min, {self.capacite} places, "
            f"{self.tarif_base}€)"
        )