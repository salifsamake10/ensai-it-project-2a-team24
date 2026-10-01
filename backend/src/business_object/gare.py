class Gare:
    """Gare du réseau SNCF, identifiée par son identifiant Navitia."""

    def __init__(self, id_sncf: str, nom: str) -> None:
        if not isinstance(id_sncf, str) or not id_sncf.strip():
            raise ValueError("L'identifiant SNCF de la gare est obligatoire.")
        if not isinstance(nom, str) or not nom.strip():
            raise ValueError("Le nom de la gare est obligatoire.")
        self.id_sncf = id_sncf
        self.nom = nom
