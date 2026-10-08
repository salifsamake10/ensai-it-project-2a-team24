
from business_object.gare import Gare
from business_object.ligne_exploitation import LigneExploitation
from dao.db_connection import get_connection


class LigneDAO:
    """DAO permettant de gérer les lignes d'exploitation dans PostgreSQL."""

    def create_ligne(self, ligne: LigneExploitation) -> LigneExploitation:
        """Insère une ligne dans la base et récupère son identifiant."""
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO ligne_exploitation
                        (gare_depart_id, gare_arrivee_id)
                    VALUES (%s, %s)
                    RETURNING id
                    """,
                    (ligne.gare_depart.id_sncf, ligne.gare_arrivee.id_sncf),
                )
                ligne.id = cursor.fetchone()[0]

        return ligne

    def get_ligne_by_id(self, id_ligne: int) -> LigneExploitation | None:
        """Récupère une ligne à partir de son identifiant."""
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        l.id,
                        gd.id_sncf, gd.nom,
                        ga.id_sncf, ga.nom
                    FROM ligne_exploitation l
                    JOIN gare gd ON l.gare_depart_id = gd.id_sncf
                    JOIN gare ga ON l.gare_arrivee_id = ga.id_sncf
                    WHERE l.id = %s
                    """,
                    (id_ligne,),
                )
                resultat = cursor.fetchone()

        if resultat is None:
            return None

        gare_depart = Gare(resultat[1], resultat[2])
        gare_arrivee = Gare(resultat[3], resultat[4])

        return LigneExploitation(
            gare_depart=gare_depart,
            gare_arrivee=gare_arrivee,
            id=resultat[0],
        )

    def get_all_lignes(self) -> list[LigneExploitation]:
        """Récupère toutes les lignes d'exploitation."""
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        l.id,
                        gd.id_sncf, gd.nom,
                        ga.id_sncf, ga.nom
                    FROM ligne_exploitation l
                    JOIN gare gd ON l.gare_depart_id = gd.id_sncf
                    JOIN gare ga ON l.gare_arrivee_id = ga.id_sncf
                    ORDER BY l.id
                    """
                )
                resultats = cursor.fetchall()

        lignes = []

        for resultat in resultats:
            gare_depart = Gare(resultat[1], resultat[2])
            gare_arrivee = Gare(resultat[3], resultat[4])

            ligne = LigneExploitation(
                gare_depart=gare_depart,
                gare_arrivee=gare_arrivee,
                id=resultat[0],
            )
            lignes.append(ligne)

        return lignes

    def update_ligne(self, ligne: LigneExploitation) -> bool:
        """Modifie les gares d'une ligne existante."""
        if ligne.id is None:
            return False

        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE ligne_exploitation
                    SET gare_depart_id = %s,
                        gare_arrivee_id = %s
                    WHERE id = %s
                    """,
                    (
                        ligne.gare_depart.id_sncf,
                        ligne.gare_arrivee.id_sncf,
                        ligne.id,
                    ),
                )
                return cursor.rowcount > 0

    def delete_ligne(self, id_ligne: int) -> bool:
        """Supprime une ligne à partir de son identifiant."""
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    DELETE FROM ligne_exploitation
                    WHERE id = %s
                    """,
                    (id_ligne,),
                )
                return cursor.rowcount > 0
