# Guide d'Utilisation - TP Kedro Weather

## Démarrage Rapide

### 1. Installation

```bash
# Activer l'environnement virtuel
venv\Scripts\activate   # Windows
# source venv/bin/activate  # Mac/Linux

# Installer les dépendances
pip install -r requirements.txt
```

### 2. Exécution du Pipeline

```bash
# Se placer dans le dossier du projet
cd tp-kedro-weather

# Exécuter le pipeline complet
kedro run
```

### 3. Visualiser le Pipeline

```bash
# Lancer l'interface de visualisation
kedro viz
```

Cela ouvrira une interface web interactive sur `http://localhost:4141` où vous pourrez :
- Visualiser le graphe du pipeline
- Explorer les dépendances entre les nodes
- Voir les datasets utilisés

## Comprendre le Pipeline

### Vue d'Ensemble

Le pipeline `data_processing` contient 5 étapes :

1. **Chargement** : Lecture du fichier CSV brut
2. **Nettoyage** : Traitement des valeurs manquantes et conversion de types
3. **Entraînement** : Création d'un modèle de régression linéaire
4. **Sauvegarde du modèle** : Stockage du modèle entraîné
5. **Sauvegarde des métriques** : Stockage des performances

### Données Générées

Le projet contient des données synthétiques générées aléatoirement :
- **100 observations** avec 3 variables (humidity, windspeed, temperature)
- **Valeurs manquantes** : 7 dans humidity, 6 dans windspeed
- **Valeurs incohérentes** : Strings dans des colonnes numériques

## Commandes Kedro Utiles

### Exécution Partielle

```bash
# Exécuter jusqu'à un node spécifique
kedro run --to-nodes=clean_weather_data_node

# Exécuter depuis un node spécifique
kedro run --from-nodes=train_model_node

# Exécuter uniquement certains nodes
kedro run --nodes=load_weather_data_node,clean_weather_data_node
```

### Gestion du Catalogue

```bash
# Lister tous les datasets
kedro catalog list

# Créer un nouveau dataset
# Éditer conf/base/catalog.yml
```

### Debugging

```bash
# Exécuter en mode verbeux
kedro run --log-level=DEBUG

# Afficher le pipeline sans l'exécuter
kedro registry describe --pipeline=__default__
```

## Structure des Fichiers de Sortie

### Données Nettoyées
- **Fichier** : `data/02_intermediate/cleaned_weather_data.csv`
- **Format** : CSV avec 100 lignes, 3 colonnes
- **Contenu** : Données sans valeurs manquantes

### Modèle Entraîné
- **Fichier** : `data/04_models/modele.pkl`
- **Format** : Pickle (scikit-learn LinearRegression)
- **Utilisation** : Peut être chargé avec `pickle.load()`

### Métriques
- **Fichier** : `data/04_models/metrics.pkl`
- **Format** : Dictionnaire Python sérialisé
- **Contenu** : 
  - MSE train/test
  - R² train/test
  - Coefficients du modèle

## Exemple d'Utilisation du Modèle

```python
import pickle
import pandas as pd

# Charger le modèle
with open('data/04_models/modele.pkl', 'rb') as f:
    model = pickle.load(f)

# Faire une prédiction
new_data = pd.DataFrame({
    'humidity': [60.0],
    'windspeed': [15.0]
})

temperature = model.predict(new_data)
print(f"Température prédite : {temperature[0]:.2f}°C")
```

## Modifier le Pipeline

### Ajouter un Nouveau Node

1. **Créer la fonction** dans `src/tp_kedro_weather/pipelines/data_processing/nodes.py` :

```python
def ma_nouvelle_fonction(df: pd.DataFrame) -> pd.DataFrame:
    # Votre code ici
    return df_transforme
```

2. **Ajouter le node** dans `src/tp_kedro_weather/pipelines/data_processing/pipeline.py` :

```python
node(
    func=ma_nouvelle_fonction,
    inputs="cleaned_weather_data",
    outputs="nouvelles_donnees",
    name="mon_nouveau_node",
)
```

3. **Définir le dataset** dans `conf/base/catalog.yml` :

```yaml
nouvelles_donnees:
  type: pandas.CSVDataset
  filepath: data/02_intermediate/nouvelles_donnees.csv
```

### Modifier les Paramètres

Éditer `conf/base/parameters.yml` pour ajouter des paramètres configurables :

```yaml
model_params:
  test_size: 0.2
  random_state: 42
```

Puis utiliser dans les nodes :

```python
def train_model(df: pd.DataFrame, parameters: Dict) -> Dict:
    test_size = parameters['model_params']['test_size']
    # ...
```

## Bonnes Pratiques

### 1. Organisation des Données

Suivez la convention Kedro pour organiser vos données :
- `01_raw` : Données brutes, jamais modifiées
- `02_intermediate` : Données en cours de traitement
- `03_primary` : Données principales traitées
- `04_models` : Modèles entraînés
- `05_model_output` : Prédictions et résultats

### 2. Naming Convention

- **Datasets** : snake_case (ex: `cleaned_weather_data`)
- **Nodes** : descriptif avec suffixe `_node` (ex: `clean_weather_data_node`)
- **Fonctions** : verbes descriptifs (ex: `clean_weather_data`)

### 3. Documentation

- Documenter chaque fonction avec des docstrings
- Expliquer les paramètres d'entrée et de sortie
- Ajouter des commentaires pour la logique complexe

### 4. Tests

Créer des tests unitaires pour chaque node :

```python
# tests/pipelines/data_processing/test_nodes.py
def test_clean_weather_data():
    df_input = pd.DataFrame({
        'humidity': [50, None, 'error'],
        'windspeed': [10, 15, 20],
        'temperature': [25, 26, 27]
    })
    
    df_output = clean_weather_data(df_input)
    
    assert df_output.isnull().sum().sum() == 0
    assert len(df_output) == 3
```

## Dépannage

### Erreur "Dataset not found"

Vérifiez que le dataset est bien défini dans `conf/base/catalog.yml`

### Erreur d'import

Assurez-vous que l'environnement virtuel est activé et que toutes les dépendances sont installées :

```bash
pip install -r requirements.txt
```

### Pipeline ne se lance pas

Vérifiez la structure du projet avec :

```bash
kedro info
```

## Ressources

- **Documentation Kedro** : https://docs.kedro.org
- **Kedro Viz** : https://github.com/kedro-org/kedro-viz
- **Tutoriels** : https://docs.kedro.org/en/stable/tutorial/tutorial_template.html

## Support

Pour toute question sur ce projet, référez-vous à :
- README_EXERCICE.md : Documentation complète du projet
- Code source dans `src/tp_kedro_weather/`
- Configuration dans `conf/base/`

