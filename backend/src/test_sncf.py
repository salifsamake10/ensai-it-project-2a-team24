from datetime import datetime

from service.service_sncf import ServiceSNCF


service_sncf = ServiceSNCF()

depart_id = "stop_area:SNCF:87471003"
arrivee_id = "stop_area:SNCF:87391003"

date_depart = datetime(2026, 10, 15, 8, 0)

possible = service_sncf.verifier_trajet_possible(
    depart_id,
    arrivee_id,
    date_depart,
)

print("Trajet possible :", possible)

if possible:
    duree = service_sncf.obtenir_duree_trajet(
        depart_id,
        arrivee_id,
        date_depart,
    )

    print("Durée :", duree, "minutes")