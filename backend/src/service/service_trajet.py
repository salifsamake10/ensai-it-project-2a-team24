from datetime import datetime, timedelta

from fastapi import HTTPException

from business_object.trajet import Trajet
from dao.trajet_dao import TrajetDao
from dao.ligne_exploitation_dao import LigneExploitationDao


class TrajetService:

    def creer_trajet(
        self,
        ligne_id: int,
        date_depart: datetime,
        capacite: int,
        prix_de_base: float
    ) -> Trajet:
        """Créer un nouveau trajet."""

        if capacite <= 0:
            raise HTTPException(status_code=400, detail="La capacité doit être strictement positive.")

        if prix_de_base < 0:
            raise HTTPException(status_code=400, detail="Le prix de base ne peut pas être négatif.")

        ligne = LigneExploitationDao().find_by_id(ligne_id)

        if not ligne:
            raise HTTPException(status_code=404, detail="Ligne d'exploitation inconnue")

        # Récupère la durée du trajet
        duree_minutes = ServiceSNFC().get_duree_trajet(      # dépend du nom de serviceSNCF, à adapter
            ligne.gare_depart,
            ligne.gare_arrivee,
            date_depart
        )

        # Calcule la date et l'heure d'arrivée
        date_arrivee = (
            date_depart
            + timedelta(minutes=duree_minutes) 
        )

        trajet = Trajet(
            ligne=ligne,
            date_heure_depart=date_depart,
            date_heure_arrivee=date_arrivee,
            duree_minutes=duree_minutes,
            capacite=capacite,
            tarif_base=prix_de_base
        )

        TrajetDao().create(trajet)

        return trajet

    def get_trajet_by_id(self, id_trajet: int) -> Trajet:
        """Retourne un trajet à partir de son identifiant."""

        trajet = TrajetDao().find_by_id(id_trajet)

        if not trajet:
            raise HTTPException(status_code=404, detail="Trajet inconnu")

        return trajet

    def delete_trajet(self, id_trajet: int):
        """Supprime un trajet à partir de son identifiant."""

        trajet = TrajetDao().find_by_id(id_trajet)

        if not trajet:
            raise HTTPException(status_code=404, detail="Trajet inconnu")

        TrajetDao().delete(id_trajet)
    
    def update_trajet(self, id_trajet: int, trajet: Trajet) -> Trajet:
        """Modifie un trajet existant."""

        trajet_existant = TrajetDao().find_by_id(id_trajet)

        if not trajet_existant:
            raise HTTPException(
                status_code=404,
                detail="inconnu"
            )

        if trajet.capacite <= 0:
            raise HTTPException(
                status_code=400,
                detail="La capacité doit être strictement positive."
            )

        if trajet.tarif_base < 0:
            raise HTTPException(
                status_code=400,
                detail="Le prix de base ne peut pas être négatif."
            )

        trajet.id_trajet = id_trajet

        TrajetDao().update(trajet)

        return trajet