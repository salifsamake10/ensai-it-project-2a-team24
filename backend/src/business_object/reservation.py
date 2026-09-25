class Reservation:
    def __init__(self, date_reservation, statut, prix_total, id_reservation = None):
        self.date_reservation = date_reservation
        self.statut = statut
        self.prix_total = prix_total
        self.id_reservation = id_reservation
