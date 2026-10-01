from enum import Enum


class Role(str, Enum):
    CLIENT = "CLIENT"
    COLLABORATEUR = "COLLABORATEUR"
    ADMIN = "ADMIN"


if __name__ == "__main__":
    role = Role.CLIENT

    print(role)
    print(role.value)
