from enum import Enum

<<<<<<< HEAD
class StatutReservation(Enum):
    CONFIRMEE = "CONFIRMEE"
    ANNULEE = "ANNULEE"
=======

class StatutReservation(str, Enum):
    CONFIRMEE = "CONFIRMEE"
    ANNULEE = "ANNULEE"

if __name__ == "__main__":
    statut = StatutReservation.CONFIRMEE

    print(statut)
    print(statut.value)
>>>>>>> 20a66599f4f4671739fb5c834c9ccea366ed32fb
