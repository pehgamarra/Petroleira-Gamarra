import pandas as pd
import numpy as np
from pathlib import Path
from faker import Faker

fake = Faker("pt_BR")

def gerar_campos(output_path=Path("data/raw/campos_petroliferos.xlsx"), n_campos=10):
    """Gera lista de campos de petróleo fictícios"""
    np.random.seed(21)
    
    estados = ["RJ", "ES", "BA", "RN"]
    tipos = ["leve", "médio", "pesado"]
    
    campos = []
    for i in range(1, n_campos + 1):
        nome = f"Campo {fake.word().capitalize()} {fake.color_name().split()[0]}"
        estado = np.random.choice(estados)
        tipo = np.random.choice(tipos, p=[0.4, 0.4, 0.2])
        capacidade = np.random.randint(20000, 100000)  # barris/dia
        ano_inicio = np.random.randint(2004, 2016)
        mes_inicio = np.random.randint(1, 13)
        data_inicio = pd.Timestamp(year=ano_inicio, month=mes_inicio, day=1)
        
        campos.append([i, nome, estado, tipo, capacidade, data_inicio])
    
    df = pd.DataFrame(campos, columns=[
        "id", "nome", "estado", "tipo_petroleo", "capacidade_barris_dia", "data_inicio"
    ])
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_excel(output_path, index=False)
    print(f"Arquivo salvo em: {output_path}")

# Permite rodar o script diretamente
if __name__ == "__main__":
    gerar_campos()
