import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.linear_model import LinearRegression

# CONFIGURAÇÕES
BASE_DIR = Path("..")
DATA_PATH = Path("../data/processed/financials_consolidated.xlsx")
MODEL_DIR = Path("../models")
OUTPUT_FILE = Path("../data/processed/predictions.xlsx")

TARGETS = ["target_producao_next", "target_receita_next"]
HORIZON = 12  # meses futuros


def generate_predictions():
    """
    Gera previsões simples para os próximos 12 meses com base nas médias móveis.
    Usa regressão linear simples como baseline para projeções financeiras.
    """

    # Carregar dados
    df = pd.read_excel(DATA_PATH)
    df["data"] = pd.to_datetime(df["data"])
    df = df.sort_values("data")

    #Criar variáveis de tempo
    df["t"] = np.arange(len(df))  # contador temporal

    #Prever cada variável numérica com regressão linear
    results = []
    future_months = pd.date_range(df["data"].iloc[-1] + pd.offsets.MonthBegin(),
                                  periods=HORIZON, freq="MS")

    for col in ["producao_total_barris", "receita_total_brl",
                "custo_operacional_total_brl", "custo_geral_total_brl", "lucro_total_brl"]:
        model = LinearRegression()
        model.fit(df[["t"]], df[col])

        future_t = pd.DataFrame(
            {"t": np.arange(len(df), len(df) + HORIZON)}
        )
        preds = model.predict(future_t)

        tmp = pd.DataFrame({
            "data": future_months,
            "variavel": col,
            "previsto": preds
        })
        results.append(tmp)

    #Consolidar resultados
    forecast_df = pd.concat(results, ignore_index=True)

    #Salvar Excel
    output_path = BASE_DIR / "data" / "processed" / "predictions.xlsx"
    forecast_df.to_excel(output_path, index=False)
    print(f" Previsões salvas em: {output_path}")

    return forecast_df
