import unittest
import sqlite3
import os
import pandas as pd
from database_manager import creer_table_stocks, traiter_et_inserer_donnees
from data_processing import corriger_csv  # Import de la fonction

DATABASE_NAME = 'test_stock_manager.db'

class TestTraitementEtInsertion(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Suppression de la base existante pour un environnement propre
        if os.path.exists(DATABASE_NAME):
            os.remove(DATABASE_NAME)
        creer_table_stocks()

    def setUp(self):
        # Réinitialiser la table avant chaque test
        with sqlite3.connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM stocks")
            conn.commit()

    def tearDown(self):
        # Nettoyage après chaque test
        if os.path.exists('test_file.xlsx'):
            os.remove('test_file.xlsx')

    def test_insertion_succes(self):
        """
        Teste l'insertion réussie de données valides depuis un fichier Excel.
        """
        # Préparation des données Excel
        data = pd.DataFrame({
            'id_produit': ['P001', 'P002'],
            'nom_produit': ['Produit1', 'Produit2'],
            'categorie': ['Cat1', 'Cat2'],
            'quantite': [10, 20],
            'prix_unitaire': [100.0, 200.0],
            'date_ajout': ['2024-01-01', '2024-01-02'],
            'source_fichier': ['test_file.xlsx', 'test_file.xlsx']
        })
        fichier_excel = 'test_file.xlsx'
        data.to_excel(fichier_excel, index=False, engine='openpyxl')

        # Exécuter la fonction
        traiter_et_inserer_donnees(fichier_excel)

        # Vérifier que les données sont bien insérées
        with sqlite3.connect(DATABASE_NAME) as conn:
            df = pd.read_sql("SELECT * FROM stocks", conn)
        self.assertEqual(len(df), 2)
        self.assertIn('P001', df['id_produit'].values)
        self.assertIn('P002', df['id_produit'].values)


    def test_insertion_avec_doublons(self):
        """
        Teste que les doublons basés sur 'id_produit' ne sont pas insérés deux fois.
        """
        # Préparation des données Excel avec doublons
        data = pd.DataFrame({
            'id_produit': ['P001', 'P001'],
            'nom_produit': ['Produit1', 'Produit1_Doublon'],
            'categorie': ['Cat1', 'Cat1'],
            'quantite': [10, 20],
            'prix_unitaire': [100.0, 100.0],
            'date_ajout': ['2024-01-01', '2024-01-01'],
            'source_fichier': ['test_file.xlsx', 'test_file.xlsx']
        })
        fichier_excel = 'test_file.xlsx'
        data.to_excel(fichier_excel, index=False, engine='openpyxl')

        # Exécuter la fonction
        traiter_et_inserer_donnees(fichier_excel)

        # Vérifier qu'un seul doublon est inséré
        with sqlite3.connect(DATABASE_NAME) as conn:
            df = pd.read_sql("SELECT * FROM stocks", conn)
        self.assertEqual(len(df), 1)
        self.assertIn('P001', df['id_produit'].values)

    def test_insertion_donnees_vides(self):
        """
        Teste le cas où le fichier Excel ne contient aucune donnée.
        """
        # Créer un fichier Excel vide
        data = pd.DataFrame(columns=['id_produit', 'nom_produit', 'categorie', 'quantite', 'prix_unitaire', 'date_ajout', 'source_fichier'])
        fichier_excel = 'test_file.xlsx'
        data.to_excel(fichier_excel, index=False, engine='openpyxl')

        # Exécuter la fonction
        traiter_et_inserer_donnees(fichier_excel)

        # Vérifier qu'aucune donnée n'a été insérée
        with sqlite3.connect(DATABASE_NAME) as conn:
            df = pd.read_sql("SELECT * FROM stocks", conn)
        self.assertEqual(len(df), 0)

class TestCorrigerCSV(unittest.TestCase):
    def setUp(self):
        # Crée des fichiers CSV de test
        self.fichier_1 = 'test_stock_1.csv'
        self.fichier_2 = 'test_stock_2.csv'
        self.fichier_vide = 'test_stock_vide.csv'

        # Données pour le premier fichier
        data1 = pd.DataFrame({
            'id_produit': ['P001', 'P002', 'P003'],
            'nom_produit': ['Produit1', 'Produit2', 'Produit3'],
            'categorie': ['Cat1', 'Cat2', 'Cat3'],
            'quantite': [10, 20, 30],
            'prix_unitaire': [100.0, 200.0, 300.0],
            'date_ajout': ['2024-01-01', '2024-01-02', '2024-01-03']
        })
        data1.to_csv(self.fichier_1, index=False, encoding='utf-8')

        # Données pour le second fichier avec doublons
        data2 = pd.DataFrame({
            'id_produit': ['P002', 'P003', 'P004'],
            'nom_produit': ['Produit2', 'Produit3', 'Produit4'],
            'categorie': ['Cat2', 'Cat3', 'Cat4'],
            'quantite': [15, 25, 35],
            'prix_unitaire': [200.0, 300.0, 400.0],
            'date_ajout': ['2024-01-04', '2024-01-05', '2024-01-06']
        })
        data2.to_csv(self.fichier_2, index=False, encoding='utf-8')

        # Fichier vide
        pd.DataFrame(columns=['id_produit', 'nom_produit', 'categorie', 'quantite', 'prix_unitaire', 'date_ajout']).to_csv(self.fichier_vide, index=False)

    def tearDown(self):
        # Supprimer les fichiers de test
        for fichier in [self.fichier_1, self.fichier_2, self.fichier_vide, 'stock_consolidated.xlsx']:
            if os.path.exists(fichier):
                os.remove(fichier)

    def test_consolidation_succes(self):
        """
        Teste la consolidation de plusieurs fichiers CSV avec gestion des doublons.
        """
        fichier_resultat = corriger_csv([self.fichier_1, self.fichier_2])
        self.assertTrue(os.path.exists(fichier_resultat))

        # Lire le fichier Excel résultant
        df_resultat = pd.read_excel(fichier_resultat, engine='openpyxl')

        # Vérifier les résultats consolidés
        self.assertEqual(len(df_resultat), 4)  # 4 produits uniques
        self.assertEqual(df_resultat.loc[df_resultat['id_produit'] == 'P002', 'quantite'].values[0], 35)  # Quantité consolidée
        self.assertEqual(df_resultat.loc[df_resultat['id_produit'] == 'P003', 'quantite'].values[0], 55)

    def test_fichier_vide(self):
        """
        Teste la gestion des fichiers vides.
        """
        fichier_resultat = corriger_csv([self.fichier_vide])
        self.assertTrue(os.path.exists(fichier_resultat))
        df_resultat = pd.read_excel(fichier_resultat, engine='openpyxl')
        self.assertTrue(df_resultat.empty)

    def test_fichier_inexistant(self):
        """
        Teste la gestion d'un fichier inexistant.
        """
        fichier_inexistant = 'fichier_inexistant.csv'
        result = corriger_csv([fichier_inexistant])
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()