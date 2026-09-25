from role import Role

class Utilisateur:
    def __init__(self, username, password, role, id_user = None):
        self.id_user = id_user
        self.id_user = username
        self.password = password
        self.role = role

    def verifier_mot_de_passe(
        self,
        mot_de_passe: str
    ) -> bool:
        pass

    def changer_role(
        self,
        nouveau_role: Role
    ) -> None:
        pass