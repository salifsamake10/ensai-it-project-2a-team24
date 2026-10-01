<<<<<<< HEAD
class Reservation:
    def __init__(self, date_reservation, statut, prix_total, id_reservation = None):
        self.date_reservation = date_reservation
        self.statut = statut
        self.prix_total = prix_total
        self.id_reservation = id_reservation
=======
from datetime import datetime

from business_object.passager import Passager
from business_object.statut_reservation import StatutReservation
from business_object.trajet import Trajet
from business_object.utilisateur import Utilisateur

class Reservation:
    def __init__(
        self,
        utilisateur: Utilisateur,
        trajet: Trajet,
        passagers: list[Passager],
        date_reservation: datetime,
        statut: StatutReservation,
        prix_total: float,
        id: int | None = None,
    ) -> None:
        self.id = id
        self.utilisateur = utilisateur
        self.trajet = trajet
        self.passagers = passagers
        self.date_reservation = date_reservation
        self.statut = statut
        self.prix_total = prix_total
>>>>>>> 20a66599f4f4671739fb5c834c9ccea366ed32fb
