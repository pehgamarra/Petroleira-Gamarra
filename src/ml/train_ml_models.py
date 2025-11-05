import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, mean_absolute_percentage_error
import joblib
import os

def train_ml_models(dataset_path):
    df = pd.read_csv(dataset_path)
    df["data"] = pd.to_datetime(df["data"])

    feature_cols = [
        'preco_medio_brl', 'preco_lag_1', 'producao_lag_1',
        'preco_lag_3', 'producao_lag_3', 'preco_lag_6', 'producao_lag_6',
        'producao_roll_3', 'producao_roll_12',
        'shock_2008', 'shock_2014', 'shock_2020', 'shock_2022',
        'mes_sin', 'mes_cos'
    ]

    rf_results = []
    xgb_results = []

    for target_col in ["target_producao_next", "target_receita_next"]:
        if target_col not in df.columns:
            continue

        X = df[feature_cols].fillna(0)
        y = df[target_col].fillna(0)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

        # Random Forest
        rf = RandomForestRegressor(n_estimators=200, random_state=42)
        rf.fit(X_train, y_train)
        rf_preds = rf.predict(X_test)
        rf_mae = mean_absolute_error(y_test, rf_preds)
        rf_rmse = np.sqrt(mean_squared_error(y_test, rf_preds))
        rf_mape = mean_absolute_percentage_error(y_test, rf_preds)
        rf_results.append({
            "target": target_col,
            "modelo": "RandomForest",
            "MAE": rf_mae,
            "RMSE": rf_rmse,
            "MAPE": rf_mape
        })
        joblib.dump(rf, f"../models/RandomForest_{target_col}.pkl")

        # XGBoost
        xgb = XGBRegressor(n_estimators=300, learning_rate=0.05, max_depth=5)
        xgb.fit(X_train, y_train)
        xgb_preds = xgb.predict(X_test)
        xgb_mae = mean_absolute_error(y_test, xgb_preds)
        xgb_rmse = np.sqrt(mean_squared_error(y_test, xgb_preds))
        xgb_mape = mean_absolute_percentage_error(y_test, xgb_preds)
        xgb_results.append({
            "target": target_col,
            "modelo": "XGBoost",
            "MAE": xgb_mae,
            "RMSE": xgb_rmse,
            "MAPE": xgb_mape
        })
        joblib.dump(xgb, f"../models/XGBoost_{target_col}.pkl")

    # Salvar separadamente
    rf_df = pd.DataFrame(rf_results)
    xgb_df = pd.DataFrame(xgb_results)

    rf_df.to_csv("../models/ml__rf_metrics.csv", index=False, mode='w')
    xgb_df.to_csv("../models/ml_xgb_metrics.csv", index=False, mode='w')

    return rf_df, xgb_df
