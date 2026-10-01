from modele_lignes import Gare, LigneExploitation
from service import DAOLigne, ServiceSNCF


class ServiceLigne:
    """Valide les gares et orchestre la gestion des lignes via le DAO."""

    def __init__(self, dao_ligne: DAOLigne, service_sncf: ServiceSNCF) -> None:
        self.dao_ligne = dao_ligne
        self.service_sncf = service_sncf

    def _gares(self, depart_id: str, arrivee_id: str) -> tuple[Gare, Gare]:
        if depart_id == arrivee_id:
            raise ValueError("La gare de départ doit être différente de la gare d'arrivée.")
        depart = self.service_sncf.obtenir_gare(depart_id)
        arrivee = self.service_sncf.obtenir_gare(arrivee_id)
        return depart, arrivee

    def creer_ligne(self, gare_depart_id: str, gare_arrivee_id: str) -> LigneExploitation:
        depart, arrivee = self._gares(gare_depart_id, gare_arrivee_id)
        return self.dao_ligne.creer(LigneExploitation(depart, arrivee))

    def modifier_ligne(
        self, ligne_id: int, gare_depart_id: str, gare_arrivee_id: str
    ) -> LigneExploitation:
        ligne = self.dao_ligne.trouver_par_id(ligne_id)
        if ligne is None:
            raise ValueError(f"Ligne introuvable : {ligne_id}")
        depart, arrivee = self._gares(gare_depart_id, gare_arrivee_id)
        # On crée un nouvel objet : l'objet en mémoire ne change que si le DAO réussit.
        return self.dao_ligne.modifier(LigneExploitation(depart, arrivee, id=ligne.id))

    def supprimer_ligne(self, ligne_id: int) -> None:
        if self.dao_ligne.trouver_par_id(ligne_id) is None:
            raise ValueError(f"Ligne introuvable : {ligne_id}")
        self.dao_ligne.supprimer(ligne_id)

    def lister_lignes(self) -> list[LigneExploitation]:
        return self.dao_ligne.lister()
