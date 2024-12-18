import argparse
from data_processing import corriger_csv
from database_manager import creer_table_stocks, traiter_et_inserer_donnees
from search import chercher_produits, afficher_contenu_table
from report_generator import generer_rapport_csv
import os
import sqlite3

print(f"INFO: Connexion à la base de données : {os.path.abspath('stock_manager.db')}")


def main():
    parser = argparse.ArgumentParser(description="Application de gestion des stocks.")
    parser.add_argument('--consolider', nargs='+', help='Fichiers CSV à consolider')
    parser.add_argument('--traiter', help='Traiter un fichier Excel ou CSV consolidé')
    parser.add_argument('--chercher', nargs=2, metavar=('categorie', 'prix_max'),
                        help='Critères de recherche : categorie prix_max')
    parser.add_argument('--rapport', choices=['csv'], help='Générer un rapport CSV')
    parser.add_argument('--afficher', action='store_true', help="Afficher le contenu de la table 'stocks'")

    args = parser.parse_args()

    # Étape 1: Consolidation des fichiers CSV
    if args.consolider:
        print("Étape 1: Consolidation des fichiers CSV...")
        fichier_consolide = corriger_csv(args.consolider)
        if fichier_consolide:
            print(f"INFO: Fichier consolidé créé avec succès : {fichier_consolide}")
        else:
            print("ERREUR: Échec de la consolidation des fichiers.")

    # Étape 2: Traitement et insertion des données
    # Étape 2: Traitement et insertion des données
    if args.traiter:
        print("Étape 2: Traitement et insertion des données dans la base de données...")
        creer_table_stocks()
        try:
            with sqlite3.connect('stock_manager.db') as conn:
                traiter_et_inserer_donnees(args.traiter, conn)
                print("INFO: Données traitées et insérées avec succès.")
        except Exception as e:
            print(f"ERREUR: Problème lors du traitement des données : {e}")

    # Étape 3: Recherche de produits
    if args.chercher:
        print("Étape 3: Recherche de produits...")
        creer_table_stocks()
        try:
            categorie, prix_max = args.chercher[0], float(args.chercher[1])
            result = chercher_produits(categorie=categorie, prix_max=prix_max)
            if not result.empty:
                print("Résultat de la recherche :")
                print("\n" + result.to_string(index=False))
            else:
                print("INFO: Aucun produit trouvé pour ces critères.")
        except Exception as e:
            print(f"ERREUR: Problème lors de la recherche : {e}")

    # Étape 4: Génération du rapport CSV
    if args.rapport:
        print("Étape 4: Génération du rapport CSV...")
        try:
            generer_rapport_csv()
            print("INFO: Rapport CSV généré avec succès.")
        except Exception as e:
            print(f"ERREUR: Problème lors de la génération du rapport : {e}")

    # Étape 5: Affichage du contenu de la base de données
    if args.afficher:
        print("Étape 5: Affichage du contenu de la table 'stocks'...")
        try:
            afficher_contenu_table()
        except Exception as e:
            print(f"ERREUR: Problème lors de l'affichage du contenu : {e}")

# Étape 3: Recherche de produits
    if args.chercher:
        print("Étape 3: Recherche de produits...")
        creer_table_stocks()
        try:
            categorie = args.chercher[0]
            prix_max = args.chercher[1]

            # Validation de prix_max
            if not prix_max.replace('.', '', 1).isdigit():
                raise ValueError("Le deuxième argument (prix_max) doit être un nombre valide.")

            prix_max = float(prix_max)
            result = chercher_produits(categorie=categorie, prix_max=prix_max)

            if not result.empty:
                print("Résultat de la recherche :")
                print("\n" + result.to_string(index=False))
            else:
                print("INFO: Aucun produit trouvé pour ces critères.")
        except ValueError as ve:
            print(f"ERREUR: {ve}")
        except Exception as e:
            print(f"ERREUR: Problème lors de la recherche : {e}")


if __name__ == "__main__":
    main()
