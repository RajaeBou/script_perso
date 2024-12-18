import sqlite3
import pandas as pd
#from fpdf import FPDF

DATABASE_NAME = "stock_manager.db"


def generer_rapport_csv():
    """
    Générer un rapport des stocks par catégorie au format CSV.
    """
    try:
        print("INFO: Connexion à la base de données...")
        with sqlite3.connect(DATABASE_NAME) as conn:
            print("INFO: Début de la génération du rapport.")

            query = """
                SELECT categorie, SUM(quantite) AS total_quantite
                FROM stocks
                GROUP BY categorie
            """
            print("INFO: Exécution de la requête SQL...")
            df = pd.read_sql_query(query, conn)

            print("INFO: Résultats de la requête SQL :")
            print(df)

            if df.empty:
                print("Aucune donnée disponible pour générer le rapport CSV.")
            else:
                rapport_csv = 'rapport_stock.csv'
                df.to_csv(rapport_csv, index=False, encoding='utf-8-sig', sep=';')
                print(f"Rapport CSV généré avec succès : {rapport_csv}")
    except Exception as e:
        print(f"Erreur lors de la génération du rapport CSV : {e}")


if __name__ == "__main__":
    # Exemple d'utilisation pour tester les fonctions
    generer_rapport_csv()
    #generer_rapport_pdf()
