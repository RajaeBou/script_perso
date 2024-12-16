import sqlite3
import pandas as pd
#from fpdf import FPDF

DATABASE_NAME = "stock_manager.db"

def generer_rapport_csv():
    """
    Générer un rapport des stocks par catégorie au format CSV.
    """
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        df = pd.read_sql_query(
            "SELECT categorie, SUM(quantite) AS total_quantite FROM stocks GROUP BY categorie",
            conn
        )
        rapport_csv = 'rapport_stock.csv'
        df.to_csv(rapport_csv, index=False, encoding='utf-8-sig', sep=';')
        conn.close()
        print(f"Rapport CSV généré : {rapport_csv}")
    except Exception as e:
        print(f"Erreur lors de la génération du rapport CSV : {e}")
'''
def generer_rapport_pdf():
    """
    Générer un rapport des stocks par catégorie au format PDF.
    """
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, 'Rapport de Stock', ln=True)

        conn = sqlite3.connect(DATABASE_NAME)
        df = pd.read_sql_query(
            "SELECT categorie, SUM(quantite) AS total_quantite FROM stocks GROUP BY categorie",
            conn
        )
        conn.close()

        if df.empty:
            pdf.cell(0, 10, "Aucune donnée disponible pour le rapport.", ln=True)
        else:
            for index, row in df.iterrows():
                pdf.cell(0, 10, f"{row['categorie']}: {row['total_quantite']} unités", ln=True)

        rapport_pdf = 'rapport_stock.pdf'
        pdf.output(rapport_pdf)
        print(f"Rapport PDF généré : {rapport_pdf}")
    except Exception as e:
        print(f"Erreur lors de la génération du rapport PDF : {e}")
    '''

if __name__ == "__main__":
    # Exemple d'utilisation pour tester les fonctions
    generer_rapport_csv()
    #generer_rapport_pdf()
