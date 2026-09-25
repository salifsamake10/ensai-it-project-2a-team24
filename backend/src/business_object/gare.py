class Gare:
    """Gare du réseau SNCF, identifiée par son identifiant Navitia."""

    def __init__(self, idSNCF: str, nom: str) -> None:
        if not isinstance(idSNCF, str) or not idSNCF.strip():
            raise ValueError("L'identifiant SNCF de la gare est obligatoire.")
        if not isinstance(nom, str) or not nom.strip():
            raise ValueError("Le nom de la gare est obligatoire.")
        self.idSNCF = idSNCF
        self.nom = nom
