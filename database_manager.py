import sqlite3
import pandas as pd
import os

DATABASE_NAME = 'stock_manager.db'

def creer_table_stocks():
    """
    Crée la table 'stocks' si elle n'existe pas déjà dans la base de données.
    """
    with sqlite3.connect(DATABASE_NAME) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS stocks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_produit TEXT UNIQUE,
                nom_produit TEXT,
                categorie TEXT,
                quantite INTEGER,
                prix_unitaire REAL,
                date_ajout TEXT,
                source_fichier TEXT
            )
        """)
        print("INFO: Table 'stocks' créée ou déjà existante.")


def traiter_et_inserer_donnees(fichier_consolide):
    """
    Traite un fichier Excel consolidé et insère les données dans la table 'stocks'.
    """
    if not os.path.exists(fichier_consolide):
        print(f"ERROR: Le fichier '{fichier_consolide}' n'existe pas.")
        return

    try:
        # Lire les données depuis le fichier Excel
        data = pd.read_excel(fichier_consolide, engine='openpyxl').drop_duplicates(subset=['id_produit'])
        data['categorie'] = data['categorie'].str.strip()
        data['nom_produit'] = data['nom_produit'].str.strip()

        # Insérer les données dans la base
        with sqlite3.connect(DATABASE_NAME) as conn:
            data.to_sql('stocks', conn, if_exists='append', index=False)
            print(f"INFO: {len(data)} ligne(s) insérée(s) avec succès dans la table 'stocks'.")
    except Exception as e:
        print(f"ERROR: Erreur lors de l'insertion des données : {e}")