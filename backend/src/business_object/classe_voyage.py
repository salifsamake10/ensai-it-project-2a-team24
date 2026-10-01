from enum import Enum

class ClasseVoyage(str, Enum):
    """
    Énumération représentant les différents niveaux de service d'un trajet[cite: 7].
    
    L'héritage de `str` facilite la conversion depuis le JSON reçu par le Controller.
    """
    CLASSIQUE = "CLASSIQUE"
    PREMIUM = "PREMIUM"