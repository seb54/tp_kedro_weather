"""Nodes pour le traitement des données météo et la modélisation."""

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
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
    
    # Convertir toutes les colonnes en numériques (gère les valeurs texte comme 'N/A', 'missing', 'unknown')
    df_clean['temperature'] = pd.to_numeric(df_clean['temperature'], errors='coerce')
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
    Entraîner plusieurs modèles et sélectionner le meilleur.
    
    Teste :
    - Régression linéaire simple
    - Régression linéaire avec features polynomiales
    - Random Forest (capture les relations non-linéaires)
    
    Args:
        df: DataFrame nettoyé
        
    Returns:
        Dictionnaire contenant le meilleur modèle et les métriques
    """
    # Préparer les features de base
    X_base = df[['humidity', 'windspeed']]
    y = df['temperature']
    
    # Diviser les données en train/test
    X_train_base, X_test_base, y_train, y_test = train_test_split(
        X_base, y, test_size=0.2, random_state=42
    )
    
    # Dictionnaire pour stocker tous les résultats
    results = {}
    
    # === Modèle 1 : Régression Linéaire Simple ===
    lr_model = LinearRegression()
    lr_model.fit(X_train_base, y_train)
    y_pred_test_lr = lr_model.predict(X_test_base)
    r2_lr = r2_score(y_test, y_pred_test_lr)
    mse_lr = mean_squared_error(y_test, y_pred_test_lr)
    mae_lr = mean_absolute_error(y_test, y_pred_test_lr)
    
    results['linear_regression'] = {
        'model': lr_model,
        'r2': r2_lr,
        'mse': mse_lr,
        'mae': mae_lr,
        'X_train': X_train_base,
        'X_test': X_test_base
    }
    
    # === Modèle 2 : Régression avec Features Polynomiales ===
    poly = PolynomialFeatures(degree=2, include_bias=False)
    X_train_poly = poly.fit_transform(X_train_base)
    X_test_poly = poly.transform(X_test_base)
    
    ridge_model = Ridge(alpha=1.0)
    ridge_model.fit(X_train_poly, y_train)
    y_pred_test_ridge = ridge_model.predict(X_test_poly)
    r2_ridge = r2_score(y_test, y_pred_test_ridge)
    mse_ridge = mean_squared_error(y_test, y_pred_test_ridge)
    mae_ridge = mean_absolute_error(y_test, y_pred_test_ridge)
    
    results['polynomial_ridge'] = {
        'model': ridge_model,
        'poly': poly,
        'r2': r2_ridge,
        'mse': mse_ridge,
        'mae': mae_ridge,
        'X_train': X_train_poly,
        'X_test': X_test_poly
    }
    
    # === Modèle 3 : Random Forest ===
    rf_model = RandomForestRegressor(
        n_estimators=100,
        max_depth=10,
        min_samples_split=5,
        random_state=42,
        n_jobs=-1
    )
    rf_model.fit(X_train_base, y_train)
    y_pred_test_rf = rf_model.predict(X_test_base)
    r2_rf = r2_score(y_test, y_pred_test_rf)
    mse_rf = mean_squared_error(y_test, y_pred_test_rf)
    mae_rf = mean_absolute_error(y_test, y_pred_test_rf)
    
    results['random_forest'] = {
        'model': rf_model,
        'r2': r2_rf,
        'mse': mse_rf,
        'mae': mae_rf,
        'X_train': X_train_base,
        'X_test': X_test_base
    }
    
    # === Sélectionner le meilleur modèle (plus grand R²) ===
    best_model_name = max(results, key=lambda k: results[k]['r2'])
    best_result = results[best_model_name]
    
    # Calculer les métriques finales sur train et test
    if 'poly' in best_result:
        y_pred_train = best_result['model'].predict(best_result['X_train'])
        y_pred_test = best_result['model'].predict(best_result['X_test'])
    else:
        y_pred_train = best_result['model'].predict(best_result['X_train'])
        y_pred_test = best_result['model'].predict(best_result['X_test'])
    
    mse_train = mean_squared_error(y_train, y_pred_train)
    mse_test = best_result['mse']
    r2_train = r2_score(y_train, y_pred_train)
    r2_test = best_result['r2']
    mae_test = best_result['mae']
    
    # Afficher les résultats
    print(f"\n=== COMPARAISON DES MODÈLES ===")
    print(f"\n1. Régression Linéaire Simple:")
    print(f"   R² test : {results['linear_regression']['r2']:.4f}")
    print(f"   MSE test: {results['linear_regression']['mse']:.4f}")
    
    print(f"\n2. Régression Polynomiale (degré 2):")
    print(f"   R² test : {results['polynomial_ridge']['r2']:.4f}")
    print(f"   MSE test: {results['polynomial_ridge']['mse']:.4f}")
    
    print(f"\n3. Random Forest:")
    print(f"   R² test : {results['random_forest']['r2']:.4f}")
    print(f"   MSE test: {results['random_forest']['mse']:.4f}")
    
    print(f"\n=== MEILLEUR MODÈLE : {best_model_name.upper().replace('_', ' ')} ===")
    print(f"MSE (train) : {mse_train:.4f}")
    print(f"MSE (test)  : {mse_test:.4f}")
    print(f"MAE (test)  : {mae_test:.4f}")
    print(f"R² (train)  : {r2_train:.4f}")
    print(f"R² (test)   : {r2_test:.4f}")
    
    # Feature importance pour Random Forest
    if best_model_name == 'random_forest':
        print(f"\nImportance des features:")
        for feature, importance in zip(['humidity', 'windspeed'], 
                                       best_result['model'].feature_importances_):
            print(f"  {feature:12s} : {importance:.4f}")
    
    # Préparer les métriques
    metrics = {
        'model_type': best_model_name,
        'mse_train': mse_train,
        'mse_test': mse_test,
        'mae_test': mae_test,
        'r2_train': r2_train,
        'r2_test': r2_test,
        'all_models': {
            name: {
                'r2': res['r2'],
                'mse': res['mse'],
                'mae': res['mae']
            }
            for name, res in results.items()
        }
    }
    
    return {'model': best_result['model'], 'metrics': metrics, 'poly': best_result.get('poly')}


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

