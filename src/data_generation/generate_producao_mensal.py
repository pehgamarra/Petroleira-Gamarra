import pandas as pd
import numpy as np

# -----------------------
# 1. Carregar dados
# -----------------------
def carregar_dados(campos_path, preco_path, cambio_path):
    campos = pd.read_excel(campos_path)
    preco = pd.read_excel(preco_path)
    cambio = pd.read_excel(cambio_path)
    return campos, preco, cambio

# -----------------------
# 2. Merge preco + cambio
# -----------------------
def merge_preco_cambio(preco, cambio):
    preco = preco.merge(cambio, on="data")
    preco["preco_brl"] = preco["preco_barril_usd"] * preco["taxa_cambio"]
    return preco

# -----------------------
# 3. Curva de maturação
# -----------------------
def calcular_fator_maturacao(meses):
    if meses < 12:
        return 0.1 + 0.075 * meses  # ramp-up
    elif meses < 60:
        return 1.0  # pico
    else:
        return max(0.5, 1.0 - 0.005 * (meses - 60))  # declínio lento

# -----------------------
# 4. Produção mensal de um campo
# -----------------------
def producao_mensal_campo(campo, dates, preco_df):
    capacidade = campo["capacidade_barris_dia"]
    data_inicio = campo["data_inicio"]
    rows = []

    for date in dates:
        if date < data_inicio:
            producao_dia = 0
        else:
            meses = (date.year - data_inicio.year) * 12 + (date.month - data_inicio.month)
            fator = calcular_fator_maturacao(meses)
            sazonalidade = 1 + 0.05 * np.sin(2 * np.pi * (date.month-1)/12)
            ruido = 1 + np.random.normal(0, 0.03)
            producao_dia = capacidade * fator * sazonalidade * ruido

        dias_no_mes = pd.Period(date, freq="M").days_in_month
        producao_barris = producao_dia * dias_no_mes

        preco_brl = preco_df.loc[preco_df["data"] == date, "preco_brl"].values[0]
        receita = producao_barris * preco_brl

        rows.append([
            campo["id"], campo["nome"], campo["estado"], campo["tipo_petroleo"],
            date, producao_barris, preco_brl, receita
        ])
    return rows

# -----------------------
# 5. Gerar produção para todos os campos
# -----------------------
def gerar_producao_total(campos, preco_df, start="2005-01", end="2025-12"):
    dates = pd.date_range(start=start, end=end, freq="MS")
    all_rows = []
    for _, campo in campos.iterrows():
        all_rows.extend(producao_mensal_campo(campo, dates, preco_df))
    df = pd.DataFrame(all_rows, columns=[
        "campo_id", "nome_campo", "estado", "tipo_petroleo",
        "data", "producao_barris", "preco_brl", "receita"
    ])
    return df

# -----------------------
# 6. Adicionar custos e lucro
# -----------------------
def adicionar_custos_lucro(df, custo_pct=0.4):
    df["custo_operacional"] = df["receita"] * custo_pct
    df["lucro_bruto"] = df["receita"] - df["custo_operacional"]
    return df

# -----------------------
# 7. Salvar arquivos
# -----------------------
def salvar_arquivos(df, csv_path, excel_path):
    df.to_csv(csv_path, index=False)
    df.to_excel(excel_path, index=False)
    print(f"✅ CSV salvo em: {csv_path}")
    print(f"✅ Excel salvo em: {excel_path}")
