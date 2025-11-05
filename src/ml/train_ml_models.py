import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
import joblib
import warnings
warnings.filterwarnings("ignore")

def mean_absolute_percentage_error(y_true, y_pred):
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100


# Função principal
def train_ml_models(path_dataset, target_col="target_producao_next"):
    """
    Treina modelos de machine learning (Random Forest e XGBoost)
    para prever a produção futura.
    """

    print("Treinando modelos de ML...")

    # 1. Carregar dataset
    df = pd.read_csv(path_dataset, parse_dates=["data"])
    df = df.dropna(subset=[target_col])

    # 2. Selecionar features
    feature_cols = [
        "producao_total", "taxa_crescimento", "var_3m",
        "dia", "mes", "trimestre", "ano"
    ]
    X = df[feature_cols]
    y = df[target_col]

    # 3. Divisão temporal
    train_mask = df["data"].dt.year <= 2023
    test_mask = df["data"].dt.year > 2023

    X_train, X_test = X[train_mask], X[test_mask]
    y_train, y_test = y[train_mask], y[test_mask]

    # 4. Modelo Random Forest
    rf_model = RandomForestRegressor(
        n_estimators=300,
        max_depth=8,
        random_state=42
    )
    rf_model.fit(X_train, y_train)
    rf_pred = rf_model.predict(X_test)

    rf_metrics = {
        "modelo": "Random Forest",
        "MAE": mean_absolute_error(y_test, rf_pred),
        "RMSE": mean_squared_error(y_test, rf_pred, squared=False),
        "MAPE": mean_absolute_percentage_error(y_test, rf_pred)
    }

    # Importância das variáveis
    rf_importance = pd.DataFrame({
        "feature": feature_cols,
        "importance": rf_model.feature_importances_
    }).sort_values("importance", ascending=False)
    rf_importance.to_csv("data/processed/feature_importance_rf.csv", index=False)

    # 5. Modelo XGBoost
    xgb_model = XGBRegressor(
        n_estimators=500,
        learning_rate=0.05,
        max_depth=6,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42
    )
    xgb_model.fit(X_train, y_train)
    xgb_pred = xgb_model.predict(X_test)

    xgb_metrics = {
        "modelo": "XGBoost",
        "MAE": mean_absolute_error(y_test, xgb_pred),
        "RMSE": mean_squared_error(y_test, xgb_pred, squared=False),
        "MAPE": mean_absolute_percentage_error(y_test, xgb_pred)
    }

    xgb_importance = pd.DataFrame({
        "feature": feature_cols,
        "importance": xgb_model.feature_importances_
    }).sort_values("importance", ascending=False)
    xgb_importance.to_csv("data/processed/feature_importance_xgb.csv", index=False)

    # 6. Salvar previsões e modelos
    df_pred = pd.DataFrame({
        "data": df.loc[test_mask, "data"],
        "real": y_test,
        "rf_previsto": rf_pred,
        "xgb_previsto": xgb_pred
    })
    df_pred.to_csv("data/processed/predictions_ml.csv", index=False)

    joblib.dump(rf_model, "models/random_forest.pkl")
    joblib.dump(xgb_model, "models/xgboost.pkl")

    print("Treinamento concluído com sucesso.")
    return rf_metrics, xgb_metrics