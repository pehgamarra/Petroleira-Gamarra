import pandas as pd
import numpy as np
import os
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split


def train_sarima(df, target_col):
    """Treina um modelo SARIMA simples para a coluna especificada"""
    df_local = df[['data', target_col]].dropna().copy()
    df_local['data'] = pd.to_datetime(df_local['data'])
    df_local = df_local.set_index('data').asfreq('MS')

    train_size = int(len(df_local) * 0.8)
    train, test = df_local.iloc[:train_size], df_local.iloc[train_size:]

    try:
        model = SARIMAX(train[target_col], order=(1,1,1), seasonal_order=(1,1,1,12), enforce_stationarity=False)
        results = model.fit(disp=False)
        forecast = results.forecast(steps=len(test))

        mae = mean_absolute_error(test[target_col], forecast)
        rmse = np.sqrt(mean_squared_error(test[target_col], forecast))
        r2 = r2_score(test[target_col], forecast)

        return {
            'target': target_col,
            'model': 'SARIMA',
            'mae': mae,
            'rmse': rmse,
            'r2': r2
        }, forecast
    except Exception as e:
        return None, str(e)


def train_rf_fallback(df, target_col):
    """Fallback com RandomForest se SARIMA falhar"""
    df_local = df[['data', target_col]].dropna().copy()
    df_local['data'] = pd.to_datetime(df_local['data'])
    df_local['month'] = df_local['data'].dt.month
    df_local['year'] = df_local['data'].dt.year

    X = df_local[['month', 'year']]
    y = df_local[target_col]

    X_train, X_test, y_train, y_test = train_test_split(X, y, shuffle=False, test_size=0.2)

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    mae = mean_absolute_error(y_test, preds)
    rmse = np.sqrt(mean_squared_error(y_test, preds))
    r2 = r2_score(y_test, preds)

    return {
        'target': target_col,
        'model': 'RandomForestFallback',
        'mae': mae,
        'rmse': rmse,
        'r2': r2
    }, pd.Series(preds, index=X_test.index)


def train_time_series_models(df):
    """
    Treina modelos SARIMA para cada coluna target_* do dataset.
    Retorna DataFrame com métricas e previsões futuras.
    """
    df = df.copy()
    df['data'] = pd.to_datetime(df['data'])
    df = df.sort_values('data')

    targets = [c for c in df.columns if c.startswith('target_')]
    metrics = []
    forecasts = pd.DataFrame()

    for target_col in targets:
        res, forecast = train_sarima(df, target_col)
        if res is None:
            res, forecast = train_rf_fallback(df, target_col)
        metrics.append(res)

        # monta dataframe de previsão
        if isinstance(forecast, pd.Series):
            forecast_df = pd.DataFrame({
                'data': df['data'].iloc[-len(forecast):].values,
                'forecast': forecast.values,
                'target': target_col
            })
            forecasts = pd.concat([forecasts, forecast_df], ignore_index=True)

    os.makedirs("../models", exist_ok=True)
    os.makedirs("../data/processed", exist_ok=True)

    metrics_df = pd.DataFrame(metrics)
    metrics_df.to_csv("../models/time_series_metrics.csv", index=False, mode='w')
    forecasts.to_csv("../data/processed/predictions_time_series.csv", index=False, mode='w')

    return metrics_df, forecasts
