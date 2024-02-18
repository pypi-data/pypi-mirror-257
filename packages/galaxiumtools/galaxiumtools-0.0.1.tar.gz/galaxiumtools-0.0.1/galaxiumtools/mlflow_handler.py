"""
mlflow_handler module
A Python package to handle MLFlow experiments tracking.
"""

import mlflow


class MLFlowHandler:
    """
    MLFlowHandler class
    Provides methods to interact with MLFlow experiments tracking.
    """

    def __init__(self, tracking_uri=None):
        """
        Initialize MLFlowHandler with an optional tracking URI.
        """
        if tracking_uri:
            mlflow.set_tracking_uri(tracking_uri)

    def start_run(self, run_name=None):
        """
        Start an MLFlow run.
        """
        mlflow.start_run(run_name=run_name)

    def log_param(self, key, value):
        """
        Log a parameter in the active MLFlow run.
        """
        mlflow.log_param(key, value)

    def log_metric(self, key, value):
        """
        Log a metric in the active MLFlow run.
        """
        mlflow.log_metric(key, value)

    def log_artifact(self, local_path, artifact_path=None):
        """
        Log an artifact in the active MLFlow run.
        """
        mlflow.log_artifact(local_path, artifact_path)

    def end_run(self):
        """
        End the active MLFlow run.
        """
        mlflow.end_run()
