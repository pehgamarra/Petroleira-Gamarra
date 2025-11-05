import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX
from prophet import Prophet
from sklearn.metrics import mean_absolute_error, mean_squared_error, mean_absolute_percentage_error
import os

def train_sarima(df, target_col):
    df = df.set_index("data").asfreq("MS")
    df[target_col] = df[target_col].interpolate()

    train = df.loc[:'2023-12-01']
    test = df.loc['2024-01-01':]

    model = SARIMAX(train[target_col], order=(1,1,1), seasonal_order=(1,1,1,12))
    results = model.fit(disp=False)
    forecast = results.predict(start=test.index[0], end=test.index[-1])

    metrics = {
        "target": target_col,
        "modelo": "SARIMA",
        "MAE": mean_absolute_error(test[target_col], forecast),
        "RMSE": mean_squared_error(test[target_col], forecast, squared=False),
        "MAPE": mean_absolute_percentage_error(test[target_col], forecast)
    }

    return metrics

def train_prophet(df, target_col):
    df_prophet = df[["data", target_col]].rename(columns={"data": "ds", target_col: "y"})
    train = df_prophet[df_prophet["ds"] <= "2023-12-01"]
    test = df_prophet[df_prophet["ds"] >= "2024-01-01"]

    model = Prophet()
    model.fit(train)
    forecast = model.predict(test)

    metrics = {
        "target": target_col,
        "modelo": "Prophet",
        "MAE": mean_absolute_error(test["y"], forecast["yhat"]),
        "RMSE": mean_squared_error(test["y"], forecast["yhat"], squared=False),
        "MAPE": mean_absolute_percentage_error(test["y"], forecast["yhat"])
    }

    return metrics

def train_time_series_models(dataset_path):
    df = pd.read_csv(dataset_path)
    df["data"] = pd.to_datetime(df["data"])

    results = []
    for target_col in ["target_producao_next", "target_receita_next"]:
        if target_col not in df.columns:
            continue

        results.append(train_sarima(df.copy(), target_col))
        results.append(train_prophet(df.copy(), target_col))

    os.makedirs("models", exist_ok=True)
    pd.DataFrame(results).to_csv("models/time_series_metrics.csv", index=False)

    return pd.DataFrame(results)
