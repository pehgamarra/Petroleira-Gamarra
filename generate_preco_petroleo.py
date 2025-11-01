import pandas as pd
import numpy as np
from pathlib import Path

def gerar_preco_petroleo(output_path=Path("data/raw/preco_petroleo.xlsx")):
    """Gera série mensal do preço do barril de petróleo (USD) 2005-2025"""
    np.random.seed(42)
    
    # Datas
    dates = pd.date_range(start="2005-01", end="2025-12", freq="MS")
    
    # Tendência base + ruído
    base_price = 60 + 15 * np.sin(np.linspace(0, 12, len(dates)))
    noise = np.random.normal(0, 3, len(dates))
    price_usd = base_price + noise
    
    # Choques históricos
    def apply_shock(series, year, factor):
        idx = (dates.year == year)
        series[idx] *= factor

    apply_shock(price_usd, 2008, 1.6)
    apply_shock(price_usd, 2009, 0.6)
    apply_shock(price_usd, 2014, 0.7)
    apply_shock(price_usd, 2020, 0.5)
    apply_shock(price_usd, 2022, 1.4)
    
    # Suavizar e garantir valores positivos
    price_usd = np.maximum(price_usd, 25)
    price_usd = pd.Series(price_usd).rolling(3, center=True, min_periods=1).mean().values
    
    # Criar DataFrame e salvar
    df = pd.DataFrame({
        "data": dates,
        "preco_barril_usd": np.round(price_usd, 2)
    })

    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_excel(output_path, index=False)
    print(f"Arquivo salvo em: {output_path}")

# Permite rodar o script diretamente
if __name__ == "__main__":
    gerar_preco_petroleo()
