from business_object.role import Role


class Utilisateur:
    def __init__(
        self,
        id: int,
        username: str,
        password_hash: str,
        role: Role
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