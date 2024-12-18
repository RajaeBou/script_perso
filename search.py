import sqlite3
import pandas as pd
from database_manager import creer_table_stocks  # Assurez-vous que la fonction est importée

DATABASE_NAME = 'stock_manager.db'

def afficher_contenu_table():
    """
    Affiche le contenu complet de la table 'stocks'.
    """
    try:
        creer_table_stocks()  # S'assurer que la table existe
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM stocks")
        rows = cursor.fetchall()
        if rows:
            print("Contenu actuel de la table 'stocks':")
            for row in rows:
                print(row)
        else:
            print("La table 'stocks' est vide.")
        conn.close()
    except Exception as e:
        print(f"Erreur lors de l'affichage du contenu : {e}")


def chercher_produits(categorie=None, prix_max=None):
    """
    Recherche des produits selon les critères fournis.
    """
    try:
        creer_table_stocks()  # S'assurer que la table existe
        conn = sqlite3.connect(DATABASE_NAME)

        # Construire et exécuter la requête
        query = "SELECT * FROM stocks WHERE LOWER(categorie) = LOWER(?) AND prix_unitaire <= ?"
        params = (categorie.strip(), prix_max)
        print("Requête SQL exécutée :", query)
        print("Paramètres :", params)
        df = pd.read_sql_query(query, conn, params=params)

        conn.close()
        return df
    except Exception as e:
        print(f"Erreur lors de la recherche : {e}")
        return pd.DataFrame()
