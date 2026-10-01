class Gare:
    def __init__(self, id_sncf: str, nom: str):
        self.id_sncf = id_sncf
        self.nom = nom


if __name__ == "__main__":
    gare = Gare("stop_area:SNCF:87471003", "Rennes")

    print(gare.id_sncf)
    print(gare.nom)