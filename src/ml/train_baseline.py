import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error

def mean_absolute_percentage_error(y_true, y_pred):
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

def train_baseline_models(path_dataset, target_col="target_producao_next"):
    """
    Cria modelos de baseline (persistência e média móvel)
    e retorna DataFrame com previsões + métricas.
    """
    df = pd.read_csv(path_dataset, parse_dates=["data"])
    df = df.sort_values("data")

    # Filtrar apenas dados com target válido
    df = df.dropna(subset=[target_col])

    # Persistência: previsão = valor atual
    df["pred_persistencia"] = df[target_col].shift(1)

    # Média móvel (últimos 3 meses)
    df["pred_media3m"] = df[target_col].shift(1).rolling(window=3).mean()

    # Remover NaNs iniciais
    df = df.dropna(subset=["pred_persistencia", "pred_media3m"])

    # Calcular métricas
    metrics = []
    for col in ["pred_persistencia", "pred_media3m"]:
        mae = mean_absolute_error(df[target_col], df[col])
        rmse = mean_squared_error(df[target_col], df[col], squared=False)
        mape = mean_absolute_percentage_error(df[target_col], df[col])
        metrics.append({
            "modelo": col,
            "MAE": mae,
            "RMSE": rmse,
            "MAPE": mape
        })

    # Salvar previsões e métricas
    df.to_csv("data/processed/predictions_baseline.csv", index=False)
    pd.DataFrame(metrics).to_excel("reports/performance_baseline.xlsx", index=False)

    return df, metrics
