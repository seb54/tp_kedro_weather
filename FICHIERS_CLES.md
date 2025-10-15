# Fichiers Clés du Projet - TP Kedro Weather

## 📄 Documentation

| Fichier | Description |
|---------|-------------|
| `README_EXERCICE.md` | Documentation complète du projet avec objectifs et résultats détaillés |
| `GUIDE_UTILISATION.md` | Guide pratique d'utilisation avec commandes et exemples |
| `RESUME_EXERCICE.md` | Résumé de l'exercice avec status de chaque étape |
| `FICHIERS_CLES.md` | Ce fichier - Liste des fichiers importants |

## 🔧 Configuration

| Fichier | Description |
|---------|-------------|
| `conf/base/catalog.yml` | **IMPORTANT** - Définition de tous les datasets (6 datasets configurés) |
| `conf/base/parameters.yml` | Paramètres du projet (vide par défaut) |
| `requirements.txt` | Liste des dépendances Python |
| `pyproject.toml` | Configuration du projet Python |

## 💻 Code Source

| Fichier | Description |
|---------|-------------|
| `src/tp_kedro_weather/pipeline_registry.py` | Enregistrement des pipelines |
| `src/tp_kedro_weather/pipelines/data_processing/nodes.py` | **IMPORTANT** - 5 nodes du pipeline |
| `src/tp_kedro_weather/pipelines/data_processing/pipeline.py` | **IMPORTANT** - Définition du pipeline |

## 📊 Données

| Fichier | Description |
|---------|-------------|
| `data/01_raw/weather_data.csv` | **INPUT** - Données brutes (100 observations avec valeurs manquantes) |
| `data/02_intermediate/cleaned_weather_data.csv` | Données nettoyées sans valeurs manquantes |
| `data/04_models/modele.pkl` | **OUTPUT** - Modèle de régression linéaire entraîné |
| `data/04_models/metrics.pkl` | **OUTPUT** - Métriques de performance (MSE, R²) |

## 🎯 Fichiers à Consulter en Premier

1. **README_EXERCICE.md** - Pour comprendre le projet
2. **GUIDE_UTILISATION.md** - Pour utiliser le projet
3. **conf/base/catalog.yml** - Pour voir la configuration des données
4. **src/tp_kedro_weather/pipelines/data_processing/nodes.py** - Pour voir le code des traitements
5. **data/04_models/** - Pour voir les résultats

## ⚡ Commandes Rapides

```bash
# Voir le catalogue
kedro catalog list

# Exécuter le pipeline
kedro run

# Visualiser le pipeline
kedro viz

# Afficher les informations du projet
kedro info
```

## 📈 Outputs du Pipeline

Après exécution de `kedro run`, vous trouverez :

1. **cleaned_weather_data.csv** : 100 lignes sans valeurs manquantes
2. **modele.pkl** : Modèle LinearRegression de scikit-learn
3. **metrics.pkl** : Dictionnaire avec MSE et R² sur train et test

## 🔍 Pour Vérifier que Tout Fonctionne

```bash
cd tp-kedro-weather
kedro run
```

Si vous voyez :
```
✅ Completed 5 out of 5 tasks
✅ Pipeline execution completed successfully
```

C'est que tout fonctionne parfaitement ! 🎉

## 📝 Notes

- Les fichiers `__pycache__` sont générés automatiquement par Python (ne pas modifier)
- Le dossier `.viz` contient les données de visualisation Kedro Viz
- Les fichiers `.gitkeep` maintiennent les dossiers vides dans Git

