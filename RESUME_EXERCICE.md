# Résumé de l'Exercice Kedro - TP Weather

## ✅ Exercice Complété avec Succès !

Ce document résume toutes les étapes réalisées dans le cadre de l'exercice Kedro sur l'analyse de données météorologiques.

---

## 📋 Étapes Réalisées

### ✅ Étape 0 : Préparation de l'Environnement
- [x] Création de l'environnement virtuel Python
- [x] Activation de l'environnement
- [x] Installation de tous les packages nécessaires :
  - kedro
  - kedro-datasets
  - kedro-viz
  - pandas
  - numpy
  - scikit-learn

### ✅ Étape 1 : Création du Projet Kedro
- [x] Création du projet nommé `tp_kedro_weather`
- [x] Vérification de la structure générée :
  - `conf/` : Configuration
  - `data/` : Données
  - `src/` : Code source
  - `notebooks/` : Notebooks (optionnel)

### ✅ Étape 2 : Chargement des Données
- [x] Génération du fichier `weather_data.csv` avec :
  - 100 observations
  - 3 variables (humidity, windspeed, temperature)
  - Valeurs manquantes intentionnelles
  - Valeurs incohérentes (strings dans colonnes numériques)
- [x] Placement du fichier dans `data/01_raw/`
- [x] Configuration du dataset dans `conf/base/catalog.yml`
- [x] Création du node `load_weather_data()`

### ✅ Étape 3 : Nettoyage des Données
- [x] Création du node `clean_weather_data(df)`
- [x] Conversion des colonnes en numériques avec `pd.to_numeric(errors='coerce')`
- [x] Remplacement des valeurs manquantes par la moyenne
- [x] Sauvegarde des données nettoyées
- [x] Résultats :
  - 7 valeurs manquantes dans humidity → corrigées
  - 6 valeurs manquantes dans windspeed → corrigées
  - 3 valeurs incohérentes → converties en NaN puis corrigées

### ✅ Étape 4 : Entraînement du Modèle
- [x] Création du node `train_model(df)`
- [x] Utilisation de `humidity` et `windspeed` comme features
- [x] Utilisation de `temperature` comme target
- [x] Division train/test (80/20)
- [x] Entraînement d'un modèle de régression linéaire
- [x] Calcul des métriques :
  - MSE train : 46.03
  - MSE test : 83.55
  - R² train : 0.1253
  - R² test : -0.4983
- [x] Calcul des coefficients :
  - humidity : -0.1191
  - windspeed : -0.1596
  - intercept : 31.6127

### ✅ Étape 5 : Sauvegarde des Résultats
- [x] Configuration des datasets dans le catalogue :
  - `trained_model` : pickle.PickleDataset
  - `metrics` : pickle.PickleDataset
- [x] Création des nodes de sauvegarde :
  - `save_model()` : extrait le modèle
  - `save_metrics()` : extrait les métriques
- [x] Sauvegarde dans `data/04_models/` :
  - `modele.pkl` : modèle entraîné
  - `metrics.pkl` : métriques de performance

---

## 📂 Structure Finale du Projet

```
tp-kedro-weather/
├── conf/
│   ├── base/
│   │   ├── catalog.yml          ✅ Catalogue complet des datasets
│   │   └── parameters.yml       ✅ Paramètres du projet
│   └── local/
│       └── credentials.yml      ✅ Credentials (vide)
├── data/
│   ├── 01_raw/
│   │   └── weather_data.csv     ✅ Données brutes générées
│   ├── 02_intermediate/
│   │   └── cleaned_weather_data.csv  ✅ Données nettoyées
│   ├── 03_primary/              ✅ Dossier créé
│   └── 04_models/
│       ├── modele.pkl           ✅ Modèle entraîné
│       └── metrics.pkl          ✅ Métriques sauvegardées
├── src/
│   └── tp_kedro_weather/
│       ├── pipelines/
│       │   ├── __init__.py
│       │   └── data_processing/ ✅ Pipeline créé
│       │       ├── __init__.py
│       │       ├── nodes.py     ✅ 5 nodes implémentés
│       │       └── pipeline.py  ✅ Pipeline configuré
│       ├── __init__.py
│       ├── __main__.py
│       ├── pipeline_registry.py ✅ Pipeline enregistré
│       └── settings.py
├── notebooks/                   ✅ Dossier pour exploration
├── README_EXERCICE.md           ✅ Documentation complète
├── GUIDE_UTILISATION.md         ✅ Guide pratique
├── RESUME_EXERCICE.md           ✅ Ce fichier
├── requirements.txt             ✅ Dépendances à jour
├── pyproject.toml
└── README.md

```

---

## 🎯 Objectifs du TP - Status

| Objectif | Status | Détails |
|----------|--------|---------|
| Structurer un projet avec Kedro | ✅ | Projet créé avec structure complète |
| Créer des pipelines | ✅ | Pipeline `data_processing` avec 5 nodes |
| Définir un catalogue de datasets | ✅ | 6 datasets configurés (CSV, Pickle, Memory) |
| Charger des données avec valeurs manquantes | ✅ | 100 observations avec 13 valeurs manquantes |
| Nettoyer et transformer les données | ✅ | Conversion numérique + imputation par moyenne |
| Entraîner un modèle ML | ✅ | Régression linéaire entraînée |
| Calculer et sauvegarder les métriques | ✅ | MSE et R² calculés et sauvegardés |
| Sauvegarder le modèle entraîné | ✅ | Modèle sauvegardé en pickle |
| Garantir la reproductibilité | ✅ | Pipeline Kedro automatisé |

---

## 📊 Résultats Obtenus

### Performance du Modèle

```
=== Résultats du Modèle ===
MSE (train) : 46.0267
MSE (test)  : 83.5527
R² (train)  : 0.1253
R² (test)   : -0.4983

Coefficients :
  humidity   : -0.1191
  windspeed  : -0.1596
  intercept  : 31.6127
```

### Nettoyage des Données

```
Valeurs manquantes avant nettoyage :
humidity       7
windspeed      6
temperature    0

Valeurs manquantes après nettoyage :
humidity       0
windspeed      0
temperature    0

Données nettoyées : 100 lignes
```

---

## 🔧 Pipeline Kedro

### Graphe du Pipeline

```
raw_weather_data (CSV)
        ↓
load_weather_data_node
        ↓
loaded_data (Memory)
        ↓
clean_weather_data_node
        ↓
cleaned_weather_data (CSV)
        ↓
train_model_node
        ↓
training_results (Memory)
        ↓
    ┌───┴───┐
    ↓       ↓
save_model  save_metrics
    ↓       ↓
trained_model  metrics
  (Pickle)   (Pickle)
```

### Nodes Implémentés

1. **load_weather_data_node**
   - Input : `raw_weather_data`
   - Output : `loaded_data`
   - Fonction : `load_weather_data()`

2. **clean_weather_data_node**
   - Input : `loaded_data`
   - Output : `cleaned_weather_data`
   - Fonction : `clean_weather_data()`

3. **train_model_node**
   - Input : `cleaned_weather_data`
   - Output : `training_results`
   - Fonction : `train_model()`

4. **save_model_node**
   - Input : `training_results`
   - Output : `trained_model`
   - Fonction : `save_model()`

5. **save_metrics_node**
   - Input : `training_results`
   - Output : `metrics`
   - Fonction : `save_metrics()`

---

## 🚀 Commandes Exécutées

### Installation
```bash
python -m venv venv
venv\Scripts\activate
pip install kedro pandas numpy scikit-learn kedro-viz kedro-datasets
```

### Création du Projet
```bash
kedro new --name tp_kedro_weather --tools none --example=n
```

### Exécution du Pipeline
```bash
cd tp-kedro-weather
kedro run
```

### Résultat de l'Exécution
```
✅ Completed 1 out of 5 tasks - load_weather_data_node
✅ Completed 2 out of 5 tasks - clean_weather_data_node
✅ Completed 3 out of 5 tasks - train_model_node
✅ Completed 4 out of 5 tasks - save_metrics_node
✅ Completed 5 out of 5 tasks - save_model_node

Pipeline execution completed successfully in 0.1 sec.
```

---

## 💡 Points Clés Appris

### 1. Structure d'un Projet Kedro
- Organisation claire des données en layers (raw, intermediate, models)
- Séparation de la configuration (conf/) et du code (src/)
- Utilisation du catalogue pour gérer les datasets

### 2. Création de Pipelines
- Définition de nodes comme fonctions Python pures
- Connexion des nodes via inputs/outputs
- Enregistrement automatique avec `find_pipelines()`

### 3. Gestion des Données
- Utilisation de différents types de datasets (CSV, Pickle, Memory)
- Configuration centralisée dans `catalog.yml`
- Chargement/sauvegarde automatique par Kedro

### 4. Bonnes Pratiques
- Fonctions pures et testables
- Documentation avec docstrings
- Naming conventions cohérentes
- Reproductibilité garantie

---

## 📚 Documentation Créée

1. **README_EXERCICE.md** : Documentation complète du projet avec :
   - Description détaillée
   - Structure du projet
   - Résultats obtenus
   - Guide d'installation
   - Améliorations possibles

2. **GUIDE_UTILISATION.md** : Guide pratique avec :
   - Démarrage rapide
   - Commandes utiles
   - Exemples d'utilisation
   - Bonnes pratiques
   - Dépannage

3. **RESUME_EXERCICE.md** : Ce document résumant l'exercice

4. **requirements.txt** : Liste complète des dépendances

---

## 🎓 Compétences Acquises

✅ Création d'un projet Kedro de A à Z
✅ Configuration du catalogue de données
✅ Implémentation de pipelines avec nodes
✅ Nettoyage de données avec pandas
✅ Entraînement de modèles ML avec scikit-learn
✅ Gestion de la persistance (pickle)
✅ Utilisation de Kedro CLI
✅ Documentation de projet
✅ Bonnes pratiques en Data Science

---

## 📝 Notes Importantes

### Pourquoi R² négatif ?
Le R² négatif sur le test set (-0.4983) est attendu car :
- Les données sont générées **aléatoirement** sans corrélation réelle
- Aucune relation linéaire n'existe entre humidity/windspeed et temperature
- Avec des données météo réelles, le modèle performerait bien mieux

### Améliorations Futures Possibles
1. Utiliser des données météo réelles
2. Tester d'autres algorithmes (Random Forest, XGBoost)
3. Ajouter des features dérivées (interactions, polynomiales)
4. Implémenter la validation croisée
5. Ajouter des tests unitaires
6. Créer des notebooks d'exploration
7. Ajouter la gestion des versions de données

---

## ✨ Conclusion

L'exercice a été **complété avec succès** ! 

Le projet démontre :
- ✅ Maîtrise de Kedro pour structurer un projet ML
- ✅ Capacité à créer des pipelines reproductibles
- ✅ Gestion propre des données et du code
- ✅ Documentation complète et professionnelle

**Le pipeline s'exécute sans erreur et produit tous les résultats attendus.**

---

**Date de réalisation** : 15 Octobre 2025
**Framework** : Kedro 1.0.0
**Python** : 3.12

