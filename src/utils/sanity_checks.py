import pandas as pd
from pathlib import Path

# ------------------------------------
# 1. Checagens básicas de integridade
# ------------------------------------
def check_date_coverage(df, col_data="data", start="2005-01-01", end="2025-12-01"):
    """
    Verifica se há cobertura completa entre as datas esperadas.
    """
    datas_esperadas = pd.date_range(start=start, end=end, freq="MS")
    datas_presentes = pd.to_datetime(df[col_data].unique())
    faltantes = set(datas_esperadas) - set(datas_presentes)
    if faltantes:
        print(f"⚠️ Datas faltantes ({len(faltantes)}): {sorted(list(faltantes))[:5]} ...")
    else:
        print("✅ Cobertura de datas completa.")
    return len(faltantes) == 0


def check_missing_values(df, cols_chave):
    """
    Checa se há valores ausentes nas colunas principais.
    """
    missing = df[cols_chave].isna().sum()
    if missing.sum() > 0:
        print("⚠️ Valores ausentes detectados:")
        print(missing[missing > 0])
    else:
        print("✅ Nenhum valor ausente nas colunas-chave.")
    return missing


def check_correlation(df, col_preco, col_receita, threshold=0.3):
    """
    Verifica se existe correlação positiva razoável entre preço e receita.
    """
    corr = df[[col_preco, col_receita]].corr().iloc[0, 1]
    if corr > threshold:
        print(f"✅ Correlação esperada confirmada (r = {corr:.2f})")
    else:
        print(f"⚠️ Correlação baixa (r = {corr:.2f}) — revisar geração de dados.")
    return corr


# ------------------------------------
# 2. Geração do relatório resumido
# ------------------------------------
def gerar_relatorio(df_prod, df_agg, path_out):
    """
    Gera um pequeno arquivo .txt com resumo das checagens e estatísticas básicas.
    """
    with open(path_out, "w", encoding="utf-8") as f:
        f.write("### SANITY CHECKS - RELATÓRIO FINAL ###\n\n")
        f.write(f"Total de registros: {len(df_prod)}\n")
        f.write(f"Período: {df_prod['data'].min()} → {df_prod['data'].max()}\n\n")

        f.write("Colunas do dataset:\n")
        for col in df_prod.columns:
            f.write(f" - {col}\n")

        f.write("\nResumo Financeiro:\n")
        resumo = df_agg.describe().round(2)
        f.write(str(resumo))

    print(f"📄 Relatório salvo em: {path_out}")
