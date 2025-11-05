import pandas as pd
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

    results = []
    os.makedirs("models", exist_ok=True)

    for target_col in ["target_producao_next", "target_receita_next"]:
        if target_col not in df.columns:
            continue

        X = df[feature_cols].fillna(0)
        y = df[target_col].fillna(0)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

        models = {
            "RandomForest": RandomForestRegressor(n_estimators=200, random_state=42),
            "XGBoost": XGBRegressor(n_estimators=300, learning_rate=0.05, max_depth=5)
        }

        for name, model in models.items():
            model.fit(X_train, y_train)
            preds = model.predict(X_test)

            mae = mean_absolute_error(y_test, preds)
            rmse = mean_squared_error(y_test, preds, squared=False)
            mape = mean_absolute_percentage_error(y_test, preds)

            results.append({
                "target": target_col,
                "modelo": name,
                "MAE": mae,
                "RMSE": rmse,
                "MAPE": mape
            })

            joblib.dump(model, f"models/{name}_{target_col}.pkl")

    pd.DataFrame(results).to_csv("models/ml_metrics.csv", index=False)
    return pd.DataFrame(results)
