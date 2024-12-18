import unittest
import sqlite3
import os
import pandas as pd
from database_manager import creer_table_stocks, traiter_et_inserer_donnees
from search import chercher_produits, afficher_contenu_table
from report_generator import generer_rapport_csv
from search import afficher_contenu_table, chercher_produits


DATABASE_NAME = 'test_stock_manager.db'

class TestProject(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        if os.path.exists(DATABASE_NAME):
            os.remove(DATABASE_NAME)
        creer_table_stocks()  # Crée la table 'stocks'

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(DATABASE_NAME):
            try:
                os.remove(DATABASE_NAME)
            except PermissionError:
                print(f"Impossible de supprimer {DATABASE_NAME}. Vérifiez les connexions ouvertes.")

    def setUp(self):
        self.conn = sqlite3.connect(DATABASE_NAME)
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM stocks")  # Réinitialise la table
        self.conn.commit()

    def tearDown(self):
        self.conn.close()

    def test_generer_rapport_csv(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO stocks (id_produit, nom_produit, categorie, quantite, prix_unitaire, date_ajout, source_fichier)
            VALUES ('P005', 'Produit5', 'Cat5', 50, 500.0, '2024-01-05', 'test_stock_3.csv')
        """)
        self.conn.commit()

        generer_rapport_csv()
        self.assertTrue(os.path.exists('rapport_stock.csv'))

        df_rapport = pd.read_csv('rapport_stock.csv', sep=';')
        self.assertIn('Cat5', df_rapport['categorie'].values)
        os.remove('rapport_stock.csv')

    def test_recherche(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO stocks (id_produit, nom_produit, categorie, quantite, prix_unitaire, date_ajout, source_fichier)
            VALUES ('P005', 'Produit5', 'Cat5', 50, 500.0, '2024-01-05', 'test_stock_3.csv')
        """)
        self.conn.commit()

        result = chercher_produits(categorie='Cat5', prix_max=600.0)
        self.assertEqual(len(result), 1)

    def test_chercher_produits_aucun_resultat(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO stocks (id_produit, nom_produit, categorie, quantite, prix_unitaire, date_ajout, source_fichier)
            VALUES ('P001', 'Produit1', 'Meubles', 30, 300.0, '2024-01-01', 'test_stock_1.csv')
        """)
        self.conn.commit()

        result = chercher_produits(categorie='Éclairage', prix_max=100)
        self.assertTrue(result.empty)

    def test_afficher_contenu_table(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO stocks (id_produit, nom_produit, categorie, quantite, prix_unitaire, date_ajout, source_fichier)
            VALUES 
            ('P001', 'Produit1', 'Meubles', 30, 300.0, '2024-01-01', 'test_stock_1.csv'),
            ('P002', 'Produit2', 'Décoration', 20, 100.0, '2024-01-02', 'test_stock_2.csv')
        """)
        self.conn.commit()

        from io import StringIO
        import sys

        captured_output = StringIO()
        sys.stdout = captured_output
        afficher_contenu_table()
        sys.stdout = sys.__stdout__

        output = captured_output.getvalue()
        self.assertIn("Produit1", output)
        self.assertIn("Produit2", output)

    def test_afficher_contenu_table_vide(self):
        from io import StringIO
        import sys

        captured_output = StringIO()
        sys.stdout = captured_output
        afficher_contenu_table()
        sys.stdout = sys.__stdout__

        output = captured_output.getvalue()
        self.assertIn("La table 'stocks' est vide.", output)

    def test_traiter_donnees_fichier_inexistant(self):
        fichier_inexistant = 'fichier_inexistant.xlsx'
        with self.assertLogs(level='ERROR') as log:
            traiter_et_inserer_donnees(fichier_inexistant)
            self.assertIn("ERROR", log.output[0])

    def test_main_recherche(self):
        os.system("python main.py --chercher Meubles 500")
        # Vérifiez les sorties attendues


class TestTraitementDonnees(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if os.path.exists(DATABASE_NAME):
            os.remove(DATABASE_NAME)
        creer_table_stocks()

    def setUp(self):
        # Réinitialiser la base avant chaque test
        with sqlite3.connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM stocks")
            conn.commit()

    def test_traiter_donnees_succes(self):
        """
        Teste l'insertion réussie de données valides.
        """
        # Créer un fichier Excel de test
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

        # Tester la fonction
        traiter_et_inserer_donnees(fichier_excel)

        # Vérifier que les données ont été insérées
        with sqlite3.connect(DATABASE_NAME) as conn:
            df = pd.read_sql("SELECT * FROM stocks", conn)
        self.assertEqual(len(df), 2)
        self.assertIn('P001', df['id_produit'].values)
        self.assertIn('P002', df['id_produit'].values)

        # Nettoyer le fichier de test
        os.remove(fichier_excel)

    def test_traiter_donnees_fichier_inexistant(self):
        """
        Teste le cas où le fichier n'existe pas.
        """
        fichier_inexistant = 'fichier_inexistant.xlsx'
        with self.assertLogs(level='INFO') as log:
            traiter_et_inserer_donnees(fichier_inexistant)
        self.assertIn("ERROR: Le fichier", log.output[0])

    def test_traiter_donnees_avec_doublons(self):
        """
        Teste l'insertion avec des doublons d'id_produit.
        """
        # Créer un fichier Excel avec des doublons
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

        # Tester la fonction
        traiter_et_inserer_donnees(fichier_excel)

        # Vérifier que seul un enregistrement a été inséré (UNIQUE constraint)
        with sqlite3.connect(DATABASE_NAME) as conn:
            df = pd.read_sql("SELECT * FROM stocks", conn)
        self.assertEqual(len(df), 1)
        self.assertIn('P001', df['id_produit'].values)

        # Nettoyer le fichier de test
        os.remove(fichier_excel)



class TestGenererRapportCSV(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Préparer une base de données propre pour les tests
        if os.path.exists(DATABASE_NAME):
            os.remove(DATABASE_NAME)
        with sqlite3.connect(DATABASE_NAME) as conn:
            conn.execute("""
                CREATE TABLE stocks (
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

    def setUp(self):
        # Nettoyer la table avant chaque test
        with sqlite3.connect(DATABASE_NAME) as conn:
            conn.execute("DELETE FROM stocks")

    def test_generer_rapport_csv_succes(self):
        """
        Teste la génération du rapport CSV avec des données valides.
        """
        # Ajouter des données de test
        with sqlite3.connect(DATABASE_NAME) as conn:
            conn.execute("""
                INSERT INTO stocks (id_produit, nom_produit, categorie, quantite, prix_unitaire, date_ajout, source_fichier)
                VALUES
                ('P001', 'Produit1', 'Meubles', 10, 100.0, '2024-01-01', 'test1.csv'),
                ('P002', 'Produit2', 'Meubles', 20, 150.0, '2024-01-02', 'test2.csv'),
                ('P003', 'Produit3', 'Décoration', 15, 50.0, '2024-01-03', 'test3.csv')
            """)

        # Appeler la fonction à tester
        generer_rapport_csv()

        # Vérifier le contenu du fichier généré
        self.assertTrue(os.path.exists('rapport_stock.csv'))
        df = pd.read_csv('rapport_stock.csv', sep=';')
        self.assertIn('Meubles', df['categorie'].values)
        self.assertIn('Décoration', df['categorie'].values)
        self.assertEqual(df.loc[df['categorie'] == 'Meubles', 'total_quantite'].values[0], 30)
        self.assertEqual(df.loc[df['categorie'] == 'Décoration', 'total_quantite'].values[0], 15)

        # Nettoyer le fichier après test
        os.remove('rapport_stock.csv')

    def test_generer_rapport_csv_vide(self):
        """
        Teste la génération du rapport CSV lorsque la table est vide.
        """
        with patch('builtins.print') as mock_print:
            generer_rapport_csv()
            mock_print.assert_any_call("Aucune donnée disponible pour générer le rapport CSV.")
        self.assertFalse(os.path.exists('rapport_stock.csv'))

    def test_generer_rapport_csv_erreur(self):
        """
        Teste la gestion des erreurs lors de la génération du rapport CSV.
        """
        with patch('sqlite3.connect', side_effect=Exception("Erreur de connexion")):
            with patch('builtins.print') as mock_print:
                generer_rapport_csv()
                mock_print.assert_any_call("Erreur lors de la génération du rapport CSV : Erreur de connexion")

class TestSearch(unittest.TestCase):

    def test_afficher_contenu_table_vide(self):
        """
        Teste l'affichage lorsque la table 'stocks' est vide.
        """
        with patch('builtins.print') as mock_print:
            afficher_contenu_table()
            mock_print.assert_any_call("La table 'stocks' est vide.")

    def test_afficher_contenu_table_remplie(self):
        """
        Teste l'affichage lorsque la table 'stocks' contient des données.
        """
        with sqlite3.connect(DATABASE_NAME) as conn:
            conn.execute("""
                INSERT INTO stocks (id_produit, nom_produit, categorie, quantite, prix_unitaire, date_ajout, source_fichier)
                VALUES ('P001', 'Produit1', 'Meubles', 10, 100.0, '2024-01-01', 'test_stock_1.csv')
            """)

        with patch('builtins.print') as mock_print:
            afficher_contenu_table()
            mock_print.assert_any_call("Contenu actuel de la table 'stocks':")
            mock_print.assert_any_call((1, 'P001', 'Produit1', 'Meubles', 10, 100.0, '2024-01-01', 'test_stock_1.csv'))

    def test_chercher_produits_avec_resultat(self):
        """
        Teste la recherche de produits avec des résultats valides.
        """
        with sqlite3.connect(DATABASE_NAME) as conn:
            conn.execute("""
                INSERT INTO stocks (id_produit, nom_produit, categorie, quantite, prix_unitaire, date_ajout, source_fichier)
                VALUES ('P002', 'Produit2', 'Meubles', 20, 150.0, '2024-01-02', 'test_stock_2.csv')
            """)

        result = chercher_produits(categorie="Meubles", prix_max=200)
        self.assertFalse(result.empty)
        self.assertIn('P002', result['id_produit'].values)

    def test_chercher_produits_aucun_resultat(self):
        """
        Teste la recherche de produits sans résultat.
        """
        result = chercher_produits(categorie="Décoration", prix_max=50)
        self.assertTrue(result.empty)

    def test_chercher_produits_entree_invalide(self):
        """
        Teste la gestion d'une catégorie vide ou d'un prix_max nul.
        """
        result = chercher_produits(categorie=None, prix_max=200)
        self.assertTrue(result.empty)



if __name__ == "__main__":
    unittest.main()
