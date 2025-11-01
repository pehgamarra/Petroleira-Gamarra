import pandas as pd
import numpy as np
from pathlib import Path

def gerar_cambio(output_path=Path("data/raw/cambio.xlsx")):
    """Gera série mensal do câmbio USD/BRL 2005-2025"""
    np.random.seed(7)
    
    dates = pd.date_range(start="2005-01", end="2025-12", freq="MS")
    
    # Tendência base + ruído
    base = 2.5 + 0.5 * np.sin(np.linspace(0, 10, len(dates)))
    noise = np.random.normal(0, 0.1, len(dates))
    cambio = base + noise
    
    # Choques macroeconômicos
    def apply_shift(series, year, factor):
        idx = (dates.year == year)
        series[idx] *= factor

    apply_shift(cambio, 2015, 1.4)
    apply_shift(cambio, 2020, 1.3)
    apply_shift(cambio, 2022, 1.2)
    
    # Suavizar e limitar valores
    cambio = pd.Series(cambio).rolling(3, center=True, min_periods=1).mean()
    cambio = np.clip(cambio, 1.5, 6.0)
    
    # Criar DataFrame e salvar
    df = pd.DataFrame({
        "data": dates,
        "taxa_cambio": np.round(cambio, 2)
    })
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_excel(output_path, index=False)
    print(f"Arquivo salvo em: {output_path}")

# Permite rodar o script diretamente
if __name__ == "__main__":
    gerar_cambio()
