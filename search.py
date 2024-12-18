import sqlite3
import pandas as pd
from database_manager import creer_table_stocks  # Assurez-vous que la fonction est importée

DATABASE_NAME = 'stock_manager.db'

def afficher_contenu_table():
    """
    Affiche le contenu complet de la table 'stocks'.

    Préconditions :
        - La base de données 'stock_manager.db' doit être accessible dans le chemin spécifié.
        - La table 'stocks' doit exister dans la base de données.

    Postconditions :
        - Affiche les lignes de la table 'stocks' si elles existent.
        - Affiche un message si la table est vide.

    Raises :
        - Exception : En cas d'erreur d'accès à la base de données ou d'affichage des données.
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

    Préconditions :
        - La base de données 'stock_manager.db' doit être accessible.
        - La table 'stocks' doit contenir les colonnes suivantes :
            * 'categorie' (type TEXT)
            * 'prix_unitaire' (type REAL)
        - 'categorie' doit être une chaîne non vide.
        - 'prix_max' doit être un nombre positif (float ou int).

    Postconditions :
        - Retourne un DataFrame contenant les produits correspondant aux critères de recherche.
        - Si aucun produit ne correspond, retourne un DataFrame vide.

    Raises :
        - ValueError : Si 'categorie' est vide ou 'prix_max' est invalide.
        - Exception : Pour toute autre erreur liée à la base de données ou à l'exécution de la requête.

    Returns :
        - pandas.DataFrame : Les produits correspondant aux critères de recherche.
    """
    try:
        if not categorie or not isinstance(prix_max, (int, float)):
            raise ValueError("Paramètres invalides : 'categorie' doit être une chaîne non vide et 'prix_max' un nombre positif.")

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
    except ValueError as ve:
        print(f"Erreur de validation des paramètres : {ve}")
        return pd.DataFrame()
    except Exception as e:
        print(f"Erreur lors de la recherche : {e}")
        return pd.DataFrame()
