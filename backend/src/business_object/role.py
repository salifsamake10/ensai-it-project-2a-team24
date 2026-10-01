from enum import Enum

<<<<<<< HEAD
class Role(Enum):
    CLIENT = "CLIENT"
    COLLABORATEUR = "COLLABORATEUR"
    ADMIN = "ADMIN"
=======

class Role(str, Enum):
    CLIENT = "CLIENT"
    COLLABORATEUR = "COLLABORATEUR"
    ADMIN = "ADMIN"


if __name__ == "__main__":
    role = Role.CLIENT

    print(role)
    print(role.value)
>>>>>>> 20a66599f4f4671739fb5c834c9ccea366ed32fb
