import pandas as pd
import numpy as np
import os
from sklearn.metrics import mean_absolute_error, mean_squared_error, mean_absolute_percentage_error

def train_baseline_models(path_dataset):
    """
    Cria modelos baseline de persistência e média móvel
    para produção e receita.
    Salva previsões e métricas.
    """
    df = pd.read_csv(path_dataset)
    metrics = []

    for target_col in ["target_producao_next", "target_receita_next"]:
        if target_col not in df.columns:
            continue

        # Baselines simples
        df[f"{target_col}_persistencia"] = df[target_col].shift(1)
        df[f"{target_col}_media3m"] = df[target_col].rolling(3).mean().shift(1)

        # Remover NaNs
        df.dropna(subset=[target_col, f"{target_col}_persistencia", f"{target_col}_media3m"], inplace=True)

        # Avaliar cada baseline
        for pred_col in [f"{target_col}_persistencia", f"{target_col}_media3m"]:
            mae = mean_absolute_error(df[target_col], df[pred_col])
            rmse = np.sqrt(mean_squared_error(df[target_col], df[pred_col]))
            mape = mean_absolute_percentage_error(df[target_col], df[pred_col])

            metrics.append({
                "target": target_col,
                "modelo": pred_col.replace(target_col + "_", ""),
                "MAE": mae,
                "RMSE": rmse,
                "MAPE": mape
            })

    # Garantir diretórios
    os.makedirs("../data/processed", exist_ok=True)
    os.makedirs("../reports", exist_ok=True)
    os.makedirs("../models", exist_ok=True)

    # Salvar previsões e métricas
    df.to_csv("../data/processed/predictions_baseline.csv", index=False)
    pd.DataFrame(metrics).to_excel("../reports/performance_baseline.xlsx", index=False)

    return pd.DataFrame(metrics)
