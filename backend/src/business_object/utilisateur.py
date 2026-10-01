<<<<<<< HEAD
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
=======
from business_object.role import Role


class Utilisateur:
    def __init__(
        self,
        username: str,
        password_hash: str,
        role: Role,
        id: int | None = None,
    ) -> None:
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.role = role


if __name__ == "__main__":
    utilisateur = Utilisateur(
        id=1,
        username="alice",
        password_hash="hash_test",
        role=Role.CLIENT
    )

    print(utilisateur.id)
    print(utilisateur.username)
    print(utilisateur.password_hash)
    print(utilisateur.role)
>>>>>>> 20a66599f4f4671739fb5c834c9ccea366ed32fb
