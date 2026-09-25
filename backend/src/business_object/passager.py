from backend.src.business_object.classe_voyage import ClasseVoyage

class Passager:
    """
    Classe métier représentant un passager associé à une réservation.
    
    Attributs:
        id (int): Identifiant unique du passager.
        age (int): Âge du passager utilisé pour le calcul tarifaire.
        classe_voyage (ClasseVoyage): Choix de la classe (CLASSIQUE ou PREMIUM.
        prix (float): Prix individuel définitif pour ce passager.
    """
    
    def __init__(self, id: int, age: int, classe_voyage: ClasseVoyage, prix: float):
        self.id = id
        self.age = age
        self.classe_voyage = classe_voyage
        self.prix = prix