import sqlite3
import pandas as pd
import os

DATABASE_NAME = 'stock_manager.db'

def creer_table_stocks():
    """
    Crée la table 'stocks' si elle n'existe pas déjà dans la base de données.

    Préconditions :
        - Une connexion valide à la base de données SQLite peut être établie.
        - La base de données doit être accessible en écriture.

    Postconditions :
        - Une table nommée 'stocks' est créée dans la base de données si elle n'existe pas déjà.
        - La structure de la table contient les colonnes nécessaires :
            * id : INTEGER PRIMARY KEY AUTOINCREMENT
            * id_produit : TEXT UNIQUE
            * nom_produit : TEXT
            * categorie : TEXT
            * quantite : INTEGER
            * prix_unitaire : REAL
            * date_ajout : TEXT
            * source_fichier : TEXT

    Raises :
        - sqlite3.DatabaseError : Si une erreur se produit lors de la création de la table.
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


def traiter_et_inserer_donnees(fichier_consolide, conn):
    """
    Traite un fichier Excel consolidé et insère les données dans la table 'stocks'.

    Préconditions :
        - Le fichier 'fichier_consolide' doit exister et être un fichier Excel valide.
        - Le fichier doit contenir les colonnes suivantes :
            * 'id_produit'
            * 'nom_produit'
            * 'categorie'
            * 'quantite'
            * 'prix_unitaire'
            * 'date_ajout'
            * 'source_fichier'
        - La connexion 'conn' doit être une connexion SQLite valide et ouverte.

    Postconditions :
        - Les données du fichier Excel sont insérées dans la table 'stocks' sans doublons sur 'id_produit'.
        - Les espaces superflus dans les colonnes 'categorie' et 'nom_produit' sont supprimés.
        - Un message de confirmation est affiché indiquant le nombre de lignes insérées.

    Raises :
        - FileNotFoundError : Si le fichier 'fichier_consolide' n'existe pas.
        - ValueError : Si le fichier Excel est invalide ou manque des colonnes requises.
        - sqlite3.DatabaseError : Si une erreur se produit lors de l'insertion dans la base de données.
        - pandas.errors.ExcelFileError : Si le fichier Excel ne peut pas être lu.
        - Exception : Pour toute autre erreur lors du traitement des données.
    """
    if not os.path.exists(fichier_consolide):
        print(f"ERROR: Le fichier '{fichier_consolide}' n'existe pas.")
        raise FileNotFoundError(f"Le fichier '{fichier_consolide}' n'existe pas.")

    try:
        # Lire les données depuis le fichier Excel
        data = pd.read_excel(fichier_consolide, engine='openpyxl').drop_duplicates(subset=['id_produit'])
        data['categorie'] = data['categorie'].str.strip()
        data['nom_produit'] = data['nom_produit'].str.strip()

        # Insérer les données dans la base
        data.to_sql('stocks', conn, if_exists='append', index=False)
        print(f"INFO: {len(data)} ligne(s) insérée(s) avec succès dans la table 'stocks'.")
    except FileNotFoundError as fnfe:
        print(f"ERROR: Fichier non trouvé : {fnfe}")
        raise
    except ValueError as ve:
        print(f"ERROR: Erreur de validation des données : {ve}")
        raise
    except sqlite3.DatabaseError as db_error:
        print(f"ERROR: Erreur lors de l'insertion des données dans la base : {db_error}")
        raise
    except Exception as e:
        print(f"ERROR: Une erreur inattendue s'est produite : {e}")
        raise
