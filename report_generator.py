import sqlite3
import pandas as pd

DATABASE_NAME = "stock_manager.db"

def generer_rapport_csv():
    """
    Générer un rapport des stocks par catégorie au format CSV.

    Préconditions :
        - La base de données 'stock_manager.db' doit exister dans le chemin spécifié.
        - La table 'stocks' doit contenir les colonnes suivantes :
            * 'categorie' (type TEXT)
            * 'quantite' (type INTEGER)
        - Les données dans 'stocks' doivent être correctement formatées (pas de valeurs nulles ou invalides pour les champs utilisés).

    Postconditions :
        - Crée un fichier CSV nommé 'rapport_stock.csv' contenant les catégories et leurs quantités totales, si des données existent.
        - Affiche un message indiquant si le rapport a été généré ou si aucune donnée n'était disponible.

    Raises :
        - Exception : En cas de problème de connexion à la base de données, de requête SQL ou d'écriture du fichier CSV.

    """
    try:
        print("INFO: Connexion à la base de données...")
        with sqlite3.connect(DATABASE_NAME) as conn:
            print("INFO: Début de la génération du rapport.")

            # Requête pour regrouper les stocks par catégorie
            query = """
                SELECT categorie, SUM(quantite) AS total_quantite
                FROM stocks
                GROUP BY categorie
            """
            print("INFO: Exécution de la requête SQL...")
            df = pd.read_sql_query(query, conn)

            # Affichage des résultats pour débogage
            print("INFO: Résultats de la requête SQL :")
            print(df)

            # Vérifier si des données sont disponibles
            if df.empty:
                print("Aucune donnée disponible pour générer le rapport CSV.")
            else:
                # Écrire les résultats dans un fichier CSV
                rapport_csv = 'rapport_stock.csv'
                df.to_csv(rapport_csv, index=False, encoding='utf-8-sig', sep=';')
                print(f"Rapport CSV généré avec succès : {rapport_csv}")
    except Exception as e:
        print(f"Erreur lors de la génération du rapport CSV : {e}")


if __name__ == "__main__":
    # Exemple d'utilisation pour tester les fonctions
    generer_rapport_csv()
