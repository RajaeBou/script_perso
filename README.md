# script_perso

# Gestion des Stocks

## Description
Ce programme permet de consolider, gérer et rechercher des données de stocks provenant de plusieurs fichiers CSV. Il offre également des fonctionnalités pour générer des rapports au format CSV.

## Fonctionnalités principales
- **Consolidation des fichiers CSV** : Combine plusieurs fichiers CSV et gère les doublons en additionnant les quantités.
- **Insertion dans une base de données SQLite** : Traite un fichier consolidé et insère les données dans une base de données.
- **Recherche de produits** : Recherche les produits selon une catégorie et un prix maximum.
- **Affichage du contenu de la base** : Affiche toutes les données de la table `stocks`.
- **Génération de rapports** : Génère un rapport CSV des stocks regroupés par catégorie.

## Installation

### Prérequis
1. Python 3.7 ou version ultérieure
2. Les bibliothèques suivantes (installables via `pip`):
   - `pandas`
   - `openpyxl`

### Étapes d'installation
1. Clonez ce dépôt :
   ```
   git clone https://github.com/nom_utilisateur/projet_stocks.git
   cd projet_stocks
   ```
2. Installez les dépendances :
   ```
   pip install -r requirements.txt
   ```

## Utilisation

### Commandes principales
Le programme est structuré pour être exécuté via des arguments de ligne de commande.

#### 1. Consolidation des fichiers CSV
```
python main.py --consolider fichier1.csv fichier2.csv
```
- **Description** : Consolide les fichiers CSV donnés en entrée et crée un fichier Excel consolidé.

#### 2. Insertion dans la base de données
```
python main.py --traiter stock_consolidated.xlsx
```
- **Description** : Insère les données du fichier Excel consolidé dans la base SQLite.

#### 3. Recherche de produits
```
python main.py --chercher categorie prix_max
```
- **Description** : Affiche les produits correspondant à la catégorie et au prix maximum.
- **Exemple** :
  ```
  python main.py --chercher Meubles 500
  ```

#### 4. Génération de rapports
```
python main.py --rapport csv
```
- **Description** : Génère un rapport CSV des stocks regroupés par catégorie.

#### 5. Affichage du contenu de la base de données
```
python main.py --afficher
```
- **Description** : Affiche le contenu actuel de la table `stocks` dans la base de données.

## Structure du projet
```
projet_stocks/
├── main.py                # Fichier principal pour exécuter les commandes
├── data_processing.py     # Gestion de la consolidation des fichiers CSV
├── database_manager.py    # Gestion de la base de données SQLite
├── search.py              # Fonctions de recherche et d'affichage
├── report_generator.py    # Génération de rapports CSV
├── test_all.py            # Tests unitaires
├── stock_1.csv            # Exemple de fichier CSV
├── stock_2.csv            # Exemple de fichier CSV
└── README.md              # Documentation
```





