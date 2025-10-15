"""Nodes pour le traitement des données météo et la modélisation."""

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from typing import Dict, Any


def load_weather_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Charger les données météo.
    
    Args:
        df: DataFrame chargé depuis le catalogue
        
    Returns:
        DataFrame brut
    """
    print(f"Données chargées : {len(df)} lignes")
    print(f"Colonnes : {list(df.columns)}")
    return df


def clean_weather_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Nettoyer les données météo.
    
    Convertit les colonnes en numériques et remplace les valeurs manquantes
    par la moyenne de chaque colonne.
    
    Args:
        df: DataFrame brut
        
    Returns:
        DataFrame nettoyé
    """
    # Copier le DataFrame pour éviter de modifier l'original
    df_clean = df.copy()
    
    # Convertir les colonnes humidity et windspeed en numériques
    df_clean['humidity'] = pd.to_numeric(df_clean['humidity'], errors='coerce')
    df_clean['windspeed'] = pd.to_numeric(df_clean['windspeed'], errors='coerce')
    
    # Compter les valeurs manquantes avant nettoyage
    missing_before = df_clean.isnull().sum()
    print(f"\nValeurs manquantes avant nettoyage :")
    print(missing_before)
    
    # Remplacer les valeurs manquantes par la moyenne de chaque colonne
    df_clean['humidity'] = df_clean['humidity'].fillna(df_clean['humidity'].mean())
    df_clean['windspeed'] = df_clean['windspeed'].fillna(df_clean['windspeed'].mean())
    df_clean['temperature'] = df_clean['temperature'].fillna(df_clean['temperature'].mean())
    
    # Compter les valeurs manquantes après nettoyage
    missing_after = df_clean.isnull().sum()
    print(f"\nValeurs manquantes après nettoyage :")
    print(missing_after)
    
    print(f"\nDonnées nettoyées : {len(df_clean)} lignes")
    
    return df_clean


def train_model(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Entraîner un modèle de régression linéaire.
    
    Utilise humidity et windspeed comme features pour prédire temperature.
    
    Args:
        df: DataFrame nettoyé
        
    Returns:
        Dictionnaire contenant le modèle et les métriques
    """
    # Préparer les features et la target
    X = df[['humidity', 'windspeed']]
    y = df['temperature']
    
    # Diviser les données en train/test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Entraîner le modèle
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # Faire des prédictions
    y_pred_train = model.predict(X_train)
    y_pred_test = model.predict(X_test)
    
    # Calculer les métriques
    mse_train = mean_squared_error(y_train, y_pred_train)
    mse_test = mean_squared_error(y_test, y_pred_test)
    r2_train = r2_score(y_train, y_pred_train)
    r2_test = r2_score(y_test, y_pred_test)
    
    metrics = {
        'mse_train': mse_train,
        'mse_test': mse_test,
        'r2_train': r2_train,
        'r2_test': r2_test,
        'coefficients': {
            'humidity': model.coef_[0],
            'windspeed': model.coef_[1],
            'intercept': model.intercept_
        }
    }
    
    print(f"\n=== Résultats du modèle ===")
    print(f"MSE (train) : {mse_train:.4f}")
    print(f"MSE (test)  : {mse_test:.4f}")
    print(f"R² (train)  : {r2_train:.4f}")
    print(f"R² (test)   : {r2_test:.4f}")
    print(f"\nCoefficients :")
    print(f"  humidity   : {model.coef_[0]:.4f}")
    print(f"  windspeed  : {model.coef_[1]:.4f}")
    print(f"  intercept  : {model.intercept_:.4f}")
    
    return {'model': model, 'metrics': metrics}


def save_model(results: Dict[str, Any]) -> Any:
    """
    Extraire le modèle pour la sauvegarde.
    
    Args:
        results: Dictionnaire contenant le modèle et les métriques
        
    Returns:
        Le modèle entraîné
    """
    return results['model']


def save_metrics(results: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extraire les métriques pour la sauvegarde.
    
    Args:
        results: Dictionnaire contenant le modèle et les métriques
        
    Returns:
        Les métriques de performance
    """
    return results['metrics']

