import pandas as pd
import numpy as np
import joblib
from pathlib import Path
from sklearn.metrics import mean_absolute_error, mean_squared_error
from math import sqrt

import warnings
warnings.filterwarnings("ignore")

from statsmodels.tsa.statespace.sarimax import SARIMAX
from prophet import Prophet

# Função auxiliar de métricas
def compute_metrics(y_true, y_pred, model_name):
    mae = mean_absolute_error(y_true, y_pred)
    rmse = sqrt(mean_squared_error(y_true, y_pred))
    mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
    return {
        "modelo": model_name,
        "MAE": mae,
        "RMSE": rmse,
        "MAPE": mape
    }


# Modelo SARIMA
def train_sarima(df, target_col="producao_total_brl"):
    df = df.set_index("data").asfreq("MS")
    df[target_col] = df[target_col].interpolate()

    train = df.loc[:'2023-12-01']
    test = df.loc['2024-01-01':]

    model = SARIMAX(train[target_col], order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))
    result = model.fit(disp=False)

    forecast = result.forecast(steps=len(test))
    metrics = compute_metrics(test[target_col], forecast, "SARIMA")

    joblib.dump(result, "models/sarima_model.pkl")
    return metrics

# Modelo Prophet
def train_prophet(df, target_col="producao_total_brl"):
    prophet_df = df[["data", target_col]].rename(columns={"data": "ds", target_col: "y"})
    prophet_df["y"] = prophet_df["y"].interpolate()

    train = prophet_df[prophet_df["ds"] <= "2023-12-01"]
    test = prophet_df[prophet_df["ds"] > "2023-12-01"]

    model = Prophet(yearly_seasonality=True, weekly_seasonality=False, daily_seasonality=False)
    model.fit(train)

    future = model.make_future_dataframe(periods=len(test), freq="MS")
    forecast = model.predict(future)
    forecast = forecast.tail(len(test))

    metrics = compute_metrics(test["y"].values, forecast["yhat"].values, "Prophet")

    joblib.dump(model, "models/prophet_model.pkl")
    return metrics


# Função principal chamada pelo notebook
def train_time_series_models(dataset_path: str):
    """
    Treina e avalia modelos de séries temporais (SARIMA e Prophet)
    Retorna métricas de ambos os modelos.
    """
    df = pd.read_csv(dataset_path)
    df["data"] = pd.to_datetime(df["data"])

    sarima_metrics = train_sarima(df)
    prophet_metrics = train_prophet(df)

    return sarima_metrics, prophet_metrics
