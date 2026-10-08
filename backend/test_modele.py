from datetime import datetime

from business_object.classe_voyage import ClasseVoyage
from business_object.gare import Gare
from business_object.ligne_exploitation import LigneExploitation
from business_object.passager import Passager
from business_object.reservation import Reservation
from business_object.role import Role
from business_object.statut_reservation import StatutReservation
from business_object.trajet import Trajet
from business_object.utilisateur import Utilisateur


# 1. Un client
client = Utilisateur(
    id=1,
    username="alice",
    password_hash="hash_test",
    role=Role.CLIENT,
)

# 2. Deux gares
rennes = Gare("stop_area:SNCF:87471003", "Rennes")
paris = Gare("stop_area:SNCF:87391003", "Paris")

# 3. Une ligne exploitée par notre compagnie
ligne = LigneExploitation(
    gare_depart=rennes,
    gare_arrivee=paris,
    id=1,
)

# 4. Un trajet proposé sur cette ligne
trajet = Trajet(
    ligne=ligne,
    date_heure_depart=datetime(2026, 10, 15, 8, 0),
    date_heure_arrivee=datetime(2026, 10, 15, 10, 0),
    duree_minutes=120,
    capacite=200,
    tarif_base=40.0,
    id=1,
)

# 5. Un passager
passager = Passager(
    id=1,
    age=25,
    classe_voyage=ClasseVoyage.CLASSIQUE,
    prix=40.0,
)

# 6. Sa réservation
reservation = Reservation(
    utilisateur=client,
    trajet=trajet,
    passagers=[passager],
    date_reservation=datetime.now(),
    statut=StatutReservation.CONFIRMEE,
    prix_total=40.0,
)

print("Client :", reservation.utilisateur.username)
print("Départ :", reservation.trajet.ligne.gare_depart.nom)
print("Arrivée :", reservation.trajet.ligne.gare_arrivee.nom)
print("Nombre de passagers :", len(reservation.passagers))
print("Classe :", reservation.passagers[0].classe_voyage.value)
print("Prix total :", reservation.prix_total)
print("Statut :", reservation.statut.value)
