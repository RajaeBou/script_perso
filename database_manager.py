import sqlite3
import pandas as pd
import os

DATABASE_NAME = 'stock_manager.db'

def creer_table_stocks():
    """
    Crée la table 'stocks' dans la base de données si elle n'existe pas.
    """
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        cursor.execute('''
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
        ''')
        conn.commit()
        print("INFO: La table 'stocks' a été créée ou existe déjà.")
    except sqlite3.Error as e:
        print(f"ERROR: Erreur lors de la création de la table 'stocks' : {e}")
    finally:
        if conn:
            conn.close()

def traiter_et_inserer_donnees(fichier_consolide):
    """
    Traite un fichier Excel consolidé et insère les données dans la table 'stocks'.
    """
    if not os.path.exists(fichier_consolide):
        print(f"ERROR: Le fichier '{fichier_consolide}' n'existe pas.")
        return

    try:
        # Lire les données en fonction du type de fichier
        data = pd.read_excel(fichier_consolide, engine='openpyxl')
        data['categorie'] = data['categorie'].astype(str).str.strip()  # Supprimer les espaces
        data['nom_produit'] = data['nom_produit'].astype(str).str.strip()

        # Supprimer les doublons sur id_produit
        data = data.drop_duplicates(subset=['id_produit'])

        # Connexion à la base de données et insertion des données
        conn = sqlite3.connect(DATABASE_NAME)
        data.to_sql('stocks', conn, if_exists='append', index=False, dtype={
            'id_produit': 'TEXT',
            'nom_produit': 'TEXT',
            'categorie': 'TEXT',
            'quantite': 'INTEGER',
            'prix_unitaire': 'REAL',
            'date_ajout': 'TEXT',
            'source_fichier': 'TEXT'
        })
        print("INFO: Données insérées avec succès dans la table 'stocks'.")
    except Exception as e:
        print(f"ERROR: Erreur lors de l'insertion des données : {e}")
    finally:
        if 'conn' in locals():
            conn.close()

