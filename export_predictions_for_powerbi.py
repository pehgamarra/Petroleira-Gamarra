import os
import pandas as pd
from datetime import datetime

def export_predictions_for_powerbi(
    pred_ml,
    metrics_df,
    pred_sarima=None,
    company_name="Petroleira Gamarra",
    output_path="../data/processed/predictions.xlsx"
):
    """
    Gera um arquivo Excel completo com previsões e métricas dos modelos.
    Ideal para visualização no Power BI.
    """

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    # LIMPEZA E NORMALIZAÇÃO DAS PREVISÕES DE ML
    
    pred_ml["data"] = pd.to_datetime(pred_ml["data"])
    pred_ml = pred_ml.sort_values("data")

    # Reorganizar em formato longo (útil para Power BI)
    pred_long = pred_ml.melt(
        id_vars=["data"],
        value_vars=["real", "rf_previsto", "xgb_previsto"],
        var_name="modelo",
        value_name="valor"
    )

    # Renomear para nomes mais intuitivos
    modelo_map = {
        "real": "Valor Real",
        "rf_previsto": "Random Forest",
        "xgb_previsto": "XGBoost",
    }
    pred_long["modelo"] = pred_long["modelo"].replace(modelo_map)

    # Adicionar colunas de tempo
    pred_long["ano"] = pred_long["data"].dt.year
    pred_long["mes"] = pred_long["data"].dt.month
    pred_long["mes_nome"] = pred_long["data"].dt.strftime("%b")
    pred_long["empresa"] = company_name
    pred_long["fonte"] = "Machine Learning"

    # ADICIONAR SARIMA (se existir)
    if pred_sarima is not None and "data" in pred_sarima:
        pred_sarima["data"] = pd.to_datetime(pred_sarima["data"])
        sarima_long = pred_sarima.melt(
            id_vars=["data"],
            value_vars=["real", "previsto"],
            var_name="modelo",
            value_name="valor"
        )
        sarima_long["modelo"] = sarima_long["modelo"].replace(
            {"real": "Valor Real", "previsto": "SARIMA"}
        )
        sarima_long["ano"] = sarima_long["data"].dt.year
        sarima_long["mes"] = sarima_long["data"].dt.month
        sarima_long["mes_nome"] = sarima_long["data"].dt.strftime("%b")
        sarima_long["empresa"] = company_name
        sarima_long["fonte"] = "SARIMA"
        pred_long = pd.concat([pred_long, sarima_long], ignore_index=True)

    
    # RESUMO MENSAL CONSOLIDADO
    resumo_mensal = (
        pred_long.groupby(["ano", "mes", "modelo"], as_index=False)
        .agg(media_valor=("valor", "mean"))
        .sort_values(["ano", "mes"])
    )

    resumo_mensal["empresa"] = company_name

    #TRATAMENTO DAS MÉTRICAS
    if metrics_df is not None and not metrics_df.empty:
        metrics = metrics_df.copy()
        metrics["empresa"] = company_name
        metrics["data_geracao"] = timestamp
        metrics = metrics.rename(columns={
            "target": "variavel_prevista",
            "modelo": "modelo",
            "MAE": "Erro Médio Absoluto (MAE)",
            "RMSE": "Raiz do Erro Quadrático (RMSE)",
            "MAPE": "Erro Percentual Médio (MAPE)",
            "R2": "R²"
        })
    else:
        metrics = pd.DataFrame()

    # CRIAR ABA DE METADADOS
    meta_info = pd.DataFrame({
        "Chave": [
            "Empresa",
            "Data de Exportação",
            "Total de Registros",
            "Modelos Incluídos",
        ],
        "Valor": [
            company_name,
            timestamp,
            len(pred_long),
            ", ".join(pred_long["modelo"].unique())
        ]
    })

    # SALVAR TUDO EM EXCEL MULTI-ABA
    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        pred_long.to_excel(writer, sheet_name="Previsões", index=False)
        resumo_mensal.to_excel(writer, sheet_name="ResumoMensal", index=False)
        metrics.to_excel(writer, sheet_name="MétricasModelos", index=False)
        meta_info.to_excel(writer, sheet_name="Metadados", index=False)

    print(f"Exportado com sucesso")
    print("Abas incluídas: Previsões | ResumoMensal | MétricasModelos | Metadados")

    return {
        "previsoes": pred_long,
        "resumo_mensal": resumo_mensal,
        "metricas": metrics,
        "metadados": meta_info
    }
