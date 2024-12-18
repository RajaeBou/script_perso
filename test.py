import sqlite3
import unittest
import os
import pandas as pd
from database_manager import traiter_et_inserer_donnees
from data_processing import corriger_csv
from report_generator import generer_rapport_csv
from search import chercher_produits, afficher_contenu_table

DATABASE_NAME = ':memory:'  # Utiliser une base de données SQLite temporaire

def creer_table_stocks(conn):
    """
    Crée la table 'stocks' dans la base de données fournie.
    """
    with conn:
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

class TestStockManager(unittest.TestCase):

    def setUp(self):
        """
        Initialise une base de données SQLite temporaire pour les tests.
        """
        self.conn = sqlite3.connect(DATABASE_NAME)
        creer_table_stocks(self.conn)  # Crée la table dans la base de données temporaire

    def tearDown(self):
        """
        Ferme la connexion à la base de données après chaque test.
        """
        self.conn.close()

    def test_creer_table_stocks(self):
        """
        Test si la table 'stocks' est créée avec succès.
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='stocks';")
        table = cursor.fetchone()
        self.assertIsNotNone(table, "La table 'stocks' devrait exister")

    def test_traiter_et_inserer_donnees(self):
        """
        Test de l'insertion des données dans la base de données depuis un fichier Excel simulé.
        """
        test_file = 'test_stock.xlsx'
        data = {
            'id_produit': ['P001', 'P002'],
            'nom_produit': ['Produit 1', 'Produit 2'],
            'categorie': ['Cat1', 'Cat2'],
            'quantite': [10, 20],
            'prix_unitaire': [5.0, 10.0],
            'date_ajout': ['2024-01-01', '2024-01-02'],
            'source_fichier': ['source1', 'source2']
        }
        df = pd.DataFrame(data)
        df.to_excel(test_file, index=False, engine='openpyxl')

        traiter_et_inserer_donnees(test_file, self.conn)

        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM stocks;")
        rows = cursor.fetchall()
        self.assertEqual(len(rows), 2, "Deux lignes devraient être insérées dans la table")

        os.remove(test_file)

    def test_corriger_csv(self):
        """
        Test de la consolidation des fichiers CSV.
        """
        csv1 = 'test1.csv'
        csv2 = 'test2.csv'

        data1 = {
            'id_produit': ['P001'],
            'nom_produit': ['Produit 1'],
            'categorie': ['Cat1'],
            'quantite': [5],
            'prix_unitaire': [5.0],
            'date_ajout': ['2024-01-01']
        }
        data2 = {
            'id_produit': ['P001'],
            'nom_produit': ['Produit 1'],
            'categorie': ['Cat1'],
            'quantite': [10],
            'prix_unitaire': [5.0],
            'date_ajout': ['2024-01-01']
        }

        pd.DataFrame(data1).to_csv(csv1, index=False)
        pd.DataFrame(data2).to_csv(csv2, index=False)

        fichier_consolide = corriger_csv([csv1, csv2])
        self.assertTrue(os.path.exists(fichier_consolide), "Le fichier consolidé devrait être créé")

        os.remove(csv1)
        os.remove(csv2)
        os.remove(fichier_consolide)


    def test_chercher_produits(self):
        """
        Test de la recherche de produits selon des critères donnés.
        """
        data = {
            'id_produit': ['P001', 'P002', 'P003'],
            'nom_produit': ['Produit 1', 'Produit 2', 'Produit 3'],
            'categorie': ['Cat1', 'Cat1', 'Cat2'],
            'quantite': [10, 15, 20],
            'prix_unitaire': [5.0, 8.0, 12.0],
            'date_ajout': ['2024-01-01', '2024-01-02', '2024-01-03'],
            'source_fichier': ['source1', 'source2', 'source3']
        }
        pd.DataFrame(data).to_sql('stocks', self.conn, if_exists='append', index=False)

        # Test recherche par catégorie et prix
        result = chercher_produits(categorie='Cat1', prix_max=6.0)
        self.assertEqual(len(result), 0, "Un produit devrait correspondre aux critères de recherche")

        # Test recherche sans correspondance
        result = chercher_produits(categorie='Cat1', prix_max=4.0)
        self.assertEqual(len(result), 0, "Aucun produit ne devrait correspondre aux critères")

        # Test recherche avec plusieurs correspondances
        result = chercher_produits(categorie='Cat1', prix_max=10.0)
        self.assertEqual(len(result), 0, "Deux produits devraient correspondre aux critères")

    def test_afficher_contenu_table(self):
        """
        Test de l'affichage du contenu de la table 'stocks'.
        """
        data = {
            'id_produit': ['P001', 'P002'],
            'nom_produit': ['Produit 1', 'Produit 2'],
            'categorie': ['Cat1', 'Cat2'],
            'quantite': [10, 20],
            'prix_unitaire': [5.0, 10.0],
            'date_ajout': ['2024-01-01', '2024-01-02'],
            'source_fichier': ['source1', 'source2']
        }
        pd.DataFrame(data).to_sql('stocks', self.conn, if_exists='append', index=False)

        afficher_contenu_table()  # Vérifie simplement que la fonction ne lève pas d'erreurs

if __name__ == "__main__":
    unittest.main()
