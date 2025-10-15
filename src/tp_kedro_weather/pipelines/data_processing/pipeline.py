"""Pipeline de traitement des données météo et modélisation."""

from kedro.pipeline import Pipeline, node
from .nodes import (
    load_weather_data,
    clean_weather_data,
    train_model,
    save_model,
    save_metrics,
)


def create_pipeline(**kwargs) -> Pipeline:
    """
    Créer le pipeline de traitement des données météo.
    
    Returns:
        Pipeline Kedro complet
    """
    return Pipeline(
        [
            # Node 1: Charger les données
            node(
                func=load_weather_data,
                inputs="raw_weather_data",
                outputs="loaded_data",
                name="load_weather_data_node",
            ),
            # Node 2: Nettoyer les données
            node(
                func=clean_weather_data,
                inputs="loaded_data",
                outputs="cleaned_weather_data",
                name="clean_weather_data_node",
            ),
            # Node 3: Entraîner le modèle
            node(
                func=train_model,
                inputs="cleaned_weather_data",
                outputs="training_results",
                name="train_model_node",
            ),
            # Node 4: Sauvegarder le modèle
            node(
                func=save_model,
                inputs="training_results",
                outputs="trained_model",
                name="save_model_node",
            ),
            # Node 5: Sauvegarder les métriques
            node(
                func=save_metrics,
                inputs="training_results",
                outputs="metrics",
                name="save_metrics_node",
            ),
        ]
    )

