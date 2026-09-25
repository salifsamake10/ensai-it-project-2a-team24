from datetime import date, datetime

from fastapi import HTTPException

from business_object.trajet import Trajet
from dao.trajet_dao import TrajetDao
from dao.ligne_exploitation_dao import LigneExploitationDao
from utils.log_utils import log


class TrajetService:

    @log
    def get_trajet_by_id(self, id_trajet: int) -> Trajet:
        """Retourne un trajet à partir de son identifiant."""

        trajet = TrajetDao().find_by_id(id_trajet)

        if not trajet:
            raise HTTPException(status_code=404, detail="Trajet inconnu")

        return trajet

    @log
    def delete_trajet(self, id_trajet: int):
        """Supprime un trajet à partir de son identifiant."""

        trajet = TrajetDao().find_by_id(id_trajet)

        if not trajet:
            raise HTTPException(status_code=404, detail="Trajet inconnu")

        TrajetDao().delete(id_trajet)