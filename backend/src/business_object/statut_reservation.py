from enum import Enum


class StatutReservation(str, Enum):
    CONFIRMEE = "CONFIRMEE"
    ANNULEE = "ANNULEE"


if __name__ == "__main__":
    statut = StatutReservation.CONFIRMEE

    print(statut)
    print(statut.value)
