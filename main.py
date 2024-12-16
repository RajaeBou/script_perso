import argparse
from data_processing import corriger_csv
from database_manager import creer_table_stocks, traiter_et_inserer_donnees
from search import chercher_produits, afficher_contenu_table
from report_generator import generer_rapport_csv

def main():
    parser = argparse.ArgumentParser(description="Application de gestion des stocks.")
    parser.add_argument('--consolider', nargs='+', help='Fichiers CSV à consolider')
    parser.add_argument('--traiter', help='Traiter un fichier Excel ou CSV consolidé')
    parser.add_argument('--chercher', nargs=2, help='Critères de recherche : categorie prix_max')
    parser.add_argument('--rapport', choices=['csv'], help='Générer un rapport CSV')
    parser.add_argument('--afficher', action='store_true', help="Afficher le contenu de la table 'stocks'")

    args = parser.parse_args()

    if args.consolider:
        fichier_consolide = corriger_csv(args.consolider)
        if fichier_consolide:
            print(f"Fichier consolidé : {fichier_consolide}")

    if args.traiter:
        creer_table_stocks()
        traiter_et_inserer_donnees(args.traiter)

    if args.chercher:
        creer_table_stocks()  # S'assurer que la table existe
        result = chercher_produits(categorie=args.chercher[0], prix_max=float(args.chercher[1]))
        print("Résultat de la recherche :", result)

    if args.rapport:
        generer_rapport_csv()

    if args.afficher:
        afficher_contenu_table()
if __name__ == "__main__":
    main()
