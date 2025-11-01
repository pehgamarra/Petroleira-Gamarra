import pandas as pd
import numpy as np

# -----------------------
# 1. Custo variável por barril
# -----------------------
def calcular_custo_variavel(df, custo_var_brl_por_barril=50):
    """
    Adiciona coluna custo_variavel_brl baseada na produção mensal
    """
    df["custo_variavel_brl"] = df["producao_barris"] * custo_var_brl_por_barril
    return df

# -----------------------
# 2. Custo fixo por campo
# -----------------------
def calcular_custo_fixo(df, custo_fixo_por_barris_dia=5000):
    """
    Custo fixo mensal proporcional à capacidade
    """
    # Proporcional à capacidade média mensal (capacidade_barris_dia)
    df["custo_fixo_brl"] = df["producao_barris"].apply(lambda x: custo_fixo_por_barris_dia if x>0 else 0)
    return df

# -----------------------
# 3. Custos gerais
# -----------------------
def gerar_custos_gerais(start="2005-01", end="2025-12", 
                        custo_admin_base=50000, custo_manut_base=40000, custo_logistica_base=30000):
    """
    Gera dataframe com custos gerais mensais, ajustados por inflação e sazonalidade
    """
    dates = pd.date_range(start=start, end=end, freq="MS")
    np.random.seed(42)
    
    custos = []
    for i, date in enumerate(dates):
        # Inflação anual ~3%
        anos = date.year - 2005
        inflacao = (1 + 0.03) ** anos
        
        # Sazonalidade ±5%
        sazonalidade = 1 + 0.05 * np.sin(2 * np.pi * (date.month-1)/12)
        
        custos.append([
            date,
            custo_admin_base * inflacao * sazonalidade,
            custo_manut_base * inflacao * sazonalidade,
            custo_logistica_base * inflacao * sazonalidade
        ])
    
    df = pd.DataFrame(custos, columns=["data", "admin_brl", "manutencao_brl", "logistica_brl"])
    return df

# -----------------------
# 4. Calcular margem bruta
# -----------------------
def calcular_margem_bruta(df):
    """
    Adiciona coluna margem_bruta = receita - custo_total (operacional)
    """
    df["custo_operacional"] = df["custo_variavel_brl"] + df["custo_fixo_brl"]
    df["margem_bruta"] = df["receita"] - df["custo_operacional"]
    return df

# -----------------------
# 5. Salvar arquivos
# -----------------------
def salvar_arquivos(df_custos, df_prod, custos_gerais_path, producao_path):
    df_custos.to_excel(custos_gerais_path, index=False)
    df_prod.to_excel(producao_path, index=False)
    print(f"✅ Custos gerais salvos em: {custos_gerais_path}")
    print(f"✅ Produção mensal atualizada salva em: {producao_path}")
