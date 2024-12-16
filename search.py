import sqlite3
import pandas as pd

DATABASE_NAME = 'stock_manager.db'

def afficher_contenu_table():
    """
    Affiche le contenu complet de la table 'stocks'.
    """
    try:
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
    Rechercher des produits selon des critères spécifiques.
    """
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()

        # Vérifier si la table existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='stocks';")
        if not cursor.fetchone():
            print("Erreur : La table 'stocks' n'existe pas.")
            return pd.DataFrame()

        # Construire la requête
        query = "SELECT * FROM stocks WHERE 1=1"
        params = []
        if categorie:
            query += " AND LOWER(categorie) = LOWER(?)"
            params.append(categorie.strip())
        if prix_max:
            query += " AND prix_unitaire <= ?"
            params.append(prix_max)

        result = pd.read_sql_query(query, conn, params=params)
        conn.close()

        # Vérifier si le DataFrame est vide
        if result.empty:
            print("Aucun produit ne correspond aux critères de recherche.")
        else:
            print(f"{len(result)} produit(s) trouvé(s) correspondant aux critères.")
            print(result.to_string(index=False))  # Afficher les résultats sous forme lisible

        return result
    except Exception as e:
        print(f"Erreur lors de la recherche : {e}")
        return pd.DataFrame()

if __name__ == "__main__":
    # Exemple d'utilisation pour tester la recherche
    # Utiliser afficher_contenu_table() pour afficher tout le contenu si nécessaire
    afficher_contenu_table()

    resultat = chercher_produits(categorie="Meubles", prix_max=500)
    # Affichage simplifié uniquement si des résultats existent
    if not resultat.empty:
        print("Résultat de la recherche :")
        print("\n" + resultat.to_string(index=False))
