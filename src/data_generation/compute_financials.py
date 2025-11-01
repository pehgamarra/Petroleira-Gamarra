import pandas as pd

# -----------------------
# 1. Distribuir custos gerais para cada campo
# -----------------------
def aplicar_share_custos_gerais(df_prod, df_custos_gerais):
    """
    Distribui custos gerais para cada linha de produção proporcionalmente à produção do mês.
    """
    # Merge df_prod com custos gerais por data
    df = df_prod.merge(df_custos_gerais, on="data", how="left")
    
    # Total produção por mês
    total_producao_mes = df.groupby("data")["producao_barris"].transform("sum")
    
    # Share proporcional para cada campo
    df["share_admin"] = df["producao_barris"] / total_producao_mes * df["admin_brl"]
    df["share_manut"] = df["producao_barris"] / total_producao_mes * df["manutencao_brl"]
    df["share_logistica"] = df["producao_barris"] / total_producao_mes * df["logistica_brl"]
    
    # Soma dos custos gerais alocados
    df["custo_geral_brl"] = df["share_admin"] + df["share_manut"] + df["share_logistica"]
    return df

# -----------------------
# 2. Calcular lucro líquido
# -----------------------
def calcular_lucro_liquido(df):
    """
    lucro_brl = receita - custo_operacional - custo_geral
    """
    df["lucro_liquido_brl"] = df["receita"] - df["custo_operacional"] - df["custo_geral_brl"]
    return df

# -----------------------
# 3. Consolidar agregados mensais
# -----------------------
def consolidar_agregados(df):
    """
    Retorna dataframe com total empresa por mês: produção, receita, custos, lucro
    """
    df_agg = df.groupby("data").agg(
        producao_total_barris=("producao_barris", "sum"),
        receita_total_brl=("receita", "sum"),
        custo_operacional_total_brl=("custo_operacional", "sum"),
        custo_geral_total_brl=("custo_geral_brl", "sum"),
        lucro_total_brl=("lucro_liquido_brl", "sum")
    ).reset_index()
    return df_agg

# -----------------------
# 4. Salvar arquivos
# -----------------------
def salvar_financeiro(df_prod, df_agg, producao_path, processed_path):
    df_prod.to_excel(producao_path, index=False)
    df_agg.to_excel(processed_path, index=False)
    print(f"✅ Produção mensal atualizada salva em: {producao_path}")
    print(f"✅ Agregados mensais salvos em: {processed_path}")
