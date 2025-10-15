# TP Kedro Weather - Prédiction de Température

## Description du Projet

Ce projet Kedro implémente un pipeline complet de machine learning pour prédire la température à partir de l'humidité et de la vitesse du vent. Il démontre l'utilisation de Kedro pour structurer un projet de data science avec des pipelines reproductibles.

## Objectifs Accomplis

✅ **Structurer un projet avec Kedro**
- Création d'un projet Kedro organisé avec une structure claire
- Définition d'un pipeline avec plusieurs nodes interconnectés

✅ **Définir et utiliser un catalogue de datasets**
- Configuration du catalogue pour gérer les fichiers de données
- Utilisation de différents types de datasets (CSV, Pickle, Memory)

✅ **Gérer les données avec Kedro**
- Chargement d'un jeu de données avec valeurs manquantes et incohérences
- Nettoyage automatisé des données dans des nodes dédiés

✅ **Entraîner et évaluer un modèle ML**
- Pipeline de modélisation pour prédire `temperature` à partir de `humidity` et `windspeed`
- Calcul et sauvegarde des métriques de performance

✅ **Sauvegarder les résultats avec Kedro**
- Stockage du modèle entraîné dans un dataset dédié
- Traçabilité et reproductibilité des expériences

## Structure du Projet

```
tp-kedro-weather/
├── conf/                          # Configuration du projet
│   └── base/
│       ├── catalog.yml           # Définition des datasets
│       └── parameters.yml        # Paramètres du pipeline
├── data/                         # Données du projet
│   ├── 01_raw/                  # Données brutes
│   │   └── weather_data.csv
│   ├── 02_intermediate/         # Données nettoyées
│   │   └── cleaned_weather_data.csv
│   └── 04_models/              # Modèles et métriques
│       ├── modele.pkl
│       └── metrics.pkl
├── src/
│   └── tp_kedro_weather/
│       └── pipelines/
│           └── data_processing/ # Pipeline principal
│               ├── __init__.py
│               ├── nodes.py     # Fonctions de traitement
│               └── pipeline.py  # Définition du pipeline
└── notebooks/                   # Notebooks Jupyter (optionnel)
```

## Pipeline Kedro

Le pipeline contient 5 nodes :

1. **load_weather_data_node** : Charge les données brutes depuis `weather_data.csv`
2. **clean_weather_data_node** : Nettoie les données (conversion numérique, imputation)
3. **train_model_node** : Entraîne un modèle de régression linéaire
4. **save_model_node** : Sauvegarde le modèle entraîné
5. **save_metrics_node** : Sauvegarde les métriques de performance

### Flux de Données

```
raw_weather_data → load_weather_data → loaded_data
                                            ↓
                                    clean_weather_data → cleaned_weather_data
                                                              ↓
                                                        train_model → training_results
                                                                           ↓
                                                    ┌─────────────────────┴────────────┐
                                                    ↓                                  ↓
                                              save_model                         save_metrics
                                                    ↓                                  ↓
                                            trained_model                          metrics
```

## Résultats Obtenus

### Nettoyage des Données
- **Valeurs manquantes avant nettoyage** :
  - humidity: 7 valeurs manquantes
  - windspeed: 6 valeurs manquantes
  - temperature: 0 valeur manquante

- **Méthode de nettoyage** :
  - Conversion des colonnes en numériques avec `pd.to_numeric(errors='coerce')`
  - Imputation des valeurs manquantes par la moyenne de chaque colonne

### Performance du Modèle

Le modèle de régression linéaire a été entraîné avec les résultats suivants :

- **MSE (train)** : 46.03
- **MSE (test)** : 83.55
- **R² (train)** : 0.1253
- **R² (test)** : -0.4983

**Coefficients du modèle** :
- humidity: -0.1191
- windspeed: -0.1596
- intercept: 31.6127

> ⚠️ **Note** : Le R² négatif sur le test set indique que le modèle ne performe pas bien. Cela est attendu car les données ont été générées aléatoirement sans relation réelle entre les variables. Dans un cas réel avec des données météo authentiques, les résultats seraient bien meilleurs.

## Installation et Exécution

### Prérequis

1. **Créer un environnement virtuel** :
   ```bash
   python -m venv venv
   ```

2. **Activer l'environnement virtuel** :
   - Windows : `venv\Scripts\activate`
   - Mac/Linux : `source venv/bin/activate`

3. **Installer les dépendances** :
   ```bash
   pip install kedro pandas numpy scikit-learn kedro-viz kedro-datasets
   ```

### Exécution du Pipeline

1. **Se placer dans le dossier du projet** :
   ```bash
   cd tp-kedro-weather
   ```

2. **Exécuter le pipeline complet** :
   ```bash
   kedro run
   ```

3. **Visualiser le pipeline** (optionnel) :
   ```bash
   kedro viz
   ```
   Cette commande ouvre une interface web interactive pour visualiser le pipeline et ses dépendances.

## Catalogue de Datasets

Le catalogue (`conf/base/catalog.yml`) définit les datasets suivants :

- **raw_weather_data** : Données météo brutes (CSV)
- **loaded_data** : Données chargées en mémoire (MemoryDataset)
- **cleaned_weather_data** : Données nettoyées (CSV)
- **training_results** : Résultats d'entraînement en mémoire (MemoryDataset)
- **trained_model** : Modèle entraîné (Pickle)
- **metrics** : Métriques de performance (Pickle)

## Nodes Implémentés

### 1. load_weather_data()
Charge les données météo depuis le fichier CSV et affiche des statistiques de base.

### 2. clean_weather_data(df)
- Convertit les colonnes `humidity` et `windspeed` en numériques
- Gère les erreurs avec `errors='coerce'`
- Remplace les valeurs manquantes par la moyenne

### 3. train_model(df)
- Utilise `humidity` et `windspeed` comme features
- Utilise `temperature` comme target
- Split train/test (80/20)
- Entraîne une régression linéaire
- Calcule MSE et R² sur train et test

### 4. save_model(results)
Extrait et retourne le modèle pour sauvegarde.

### 5. save_metrics(results)
Extrait et retourne les métriques pour sauvegarde.

## Améliorations Possibles

1. **Données réelles** : Utiliser des données météo réelles avec corrélations
2. **Modèles avancés** : Tester d'autres algorithmes (Random Forest, XGBoost)
3. **Validation croisée** : Implémenter une validation croisée
4. **Feature engineering** : Créer de nouvelles features (interactions, polynomiales)
5. **Hyperparameter tuning** : Optimiser les hyperparamètres
6. **Monitoring** : Ajouter des hooks pour surveiller le pipeline
7. **Tests unitaires** : Ajouter des tests pour chaque node

## Commandes Utiles Kedro

```bash
# Lister tous les pipelines
kedro registry list

# Exécuter un pipeline spécifique
kedro run --pipeline=data_processing

# Exécuter jusqu'à un node spécifique
kedro run --to-nodes=clean_weather_data_node

# Exécuter depuis un node spécifique
kedro run --from-nodes=train_model_node

# Visualiser le pipeline
kedro viz

# Créer un nouveau pipeline
kedro pipeline create <pipeline_name>
```

## Auteur

Projet réalisé dans le cadre d'un exercice Kedro pour l'apprentissage des bonnes pratiques en data science.

## Date

15 Octobre 2025

