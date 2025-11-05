import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error
from statsmodels.tsa.statespace.sarimax import SARIMAX
from prophet import Prophet
import warnings
warnings.filterwarnings("ignore")

def mean_absolute_percentage_error(y_true, y_pred):
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

# =========================================================
# 1) Modelo SARIMA
# =========================================================
def train_sarima(path_dataset, target_col="target_producao_next"):
    """
    Treina modelo SARIMA sobre série agregada de produção.
    Retorna previsões e métricas.
    """
    print("Treinando modelo SARIMA...")

    df = pd.read_csv(path_dataset, parse_dates=["data"]).sort_values("data")
    df = df.dropna(subset=[target_col])

    # Série temporal univariada
    ts = df.set_index("data")[target_col]

    # Divisão temporal (train até 2023, test 2024–2025)
    ts_train = ts[ts.index.year <= 2023]
    ts_test = ts[ts.index.year > 2023]

    # Ajustar modelo simples SARIMA
    model = SARIMAX(ts_train, order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))
    results = model.fit(disp=False)

    # Previsões
    forecast = results.get_forecast(steps=len(ts_test))
    pred = forecast.predicted_mean

    # Avaliar
    mae = mean_absolute_error(ts_test, pred)
    rmse = mean_squared_error(ts_test, pred, squared=False)
    mape = mean_absolute_percentage_error(ts_test, pred)

    metrics = {
        "modelo": "SARIMA(1,1,1)(1,1,1,12)",
        "MAE": mae,
        "RMSE": rmse,
        "MAPE": mape
    }

    # Salvar previsões
    df_pred = pd.DataFrame({"data": ts_test.index, "real": ts_test.values, "previsto": pred.values})
    df_pred.to_csv("data/processed/predictions_sarima.csv", index=False)

    return metrics


# =========================================================
# 2) Modelo Prophet
# =========================================================
def train_prophet(path_dataset, target_col="target_producao_next"):
    """
    Treina modelo Prophet sobre a série agregada de produção.
    Retorna métricas de desempenho.
    """
    print("Treinando modelo Prophet...")

    df = pd.read_csv(path_dataset, parse_dates=["data"]).sort_values("data")
    df = df.dropna(subset=[target_col])

    # Preparar formato exigido pelo Prophet
    df_prophet = df_
