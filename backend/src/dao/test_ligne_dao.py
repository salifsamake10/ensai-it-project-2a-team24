from business_object.gare import Gare
from business_object.ligne_exploitation import LigneExploitation
from dao.db_connection import get_connection
from dao.ligne_dao import LigneDAO

# 1. Création de deux objets Gare
gare_depart = Gare("stop_area:SNCF:87471003", "Rennes")
gare_arrivee = Gare("stop_area:SNCF:87391003", "Paris Montparnasse")


# 2. Enregistrement des gares dans PostgreSQL
with get_connection() as conn:
    with conn.cursor() as cursor:
        for gare in [gare_depart, gare_arrivee]:
            cursor.execute(
                """
                INSERT INTO gare (id_sncf, nom)
                VALUES (%s, %s)
                ON CONFLICT (id_sncf) DO NOTHING
                """,
                (gare.id_sncf, gare.nom),
            )


# 3. Création de l'objet LigneExploitation
ligne = LigneExploitation(
    gare_depart=gare_depart,
    gare_arrivee=gare_arrivee,
)


# 4. Insertion de la ligne dans PostgreSQL
ligne_dao = LigneDAO()
ligne_creee = ligne_dao.create_ligne(ligne)


# 5. Vérification du résultat
print("Identifiant de la ligne :", ligne_creee.id)
print("Gare de départ :", ligne_creee.gare_depart.nom)
print("Gare d'arrivée :", ligne_creee.gare_arrivee.nom)

assert ligne_creee.id is not None
print("test réussi")

dao = LigneDAO()

# Test de récupération par identifiant
ligne = dao.get_ligne_by_id(ligne_creee.id)

assert ligne is not None
assert ligne.gare_depart.id_sncf == gare_depart.id_sncf
assert ligne.gare_arrivee.id_sncf == gare_arrivee.id_sncf

print("Récupération par ID : OK")

# Test de récupération de toutes les lignes
lignes = dao.get_all_lignes()

assert any(l.id == ligne_creee.id for l in lignes)

print("Récupération de toutes les lignes : OK")

# Test de modification
gare_nantes = Gare("stop_area:SNCF:87481002", "Nantes")

with get_connection() as conn:
    with conn.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO gare (id_sncf, nom)
            VALUES (%s, %s)
            ON CONFLICT (id_sncf) DO NOTHING
            """,
            (gare_nantes.id_sncf, gare_nantes.nom),
        )

ligne_creee.gare_arrivee = gare_nantes

assert dao.update_ligne(ligne_creee) is True

ligne_modifiee = dao.get_ligne_by_id(ligne_creee.id)
assert ligne_modifiee.gare_arrivee.id_sncf == gare_nantes.id_sncf

print("Modification : OK")

# Test de suppression
assert dao.delete_ligne(ligne_creee.id) is True
assert dao.get_ligne_by_id(ligne_creee.id) is None

print("Suppression : OK")
print("Tous les tests LigneDAO ont réussi !")
