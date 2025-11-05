"""
Gera o dataset final para modelagem (ML) com targets e splits temporais.
"""

import pandas as pd
import numpy as np
from pathlib import Path

def load_features(base_dir: Path):
    """Carrega o dataset de features gerado no EDA."""
    features_path = base_dir / "data" / "processed" / "ml_dataset_features.csv"
    df = pd.read_csv(features_path, parse_dates=["data"])
    df = df.sort_values("data").reset_index(drop=True)
    return df

def create_targets(df: pd.DataFrame):
    """Cria as colunas de target (valores do próximo mês)."""
    df["target_producao_next"] = df["producao_total_barris"].shift(-1)
    df["target_receita_next"] = df["receita_total_brl"].shift(-1)
    return df

def add_temporal_features(df: pd.DataFrame):
    """Adiciona colunas de tempo úteis para o modelo."""
    df["ano"] = df["data"].dt.year
    df["mes"] = df["data"].dt.month
    df["mes_sin"] = np.sin(2 * np.pi * df["mes"] / 12)
    df["mes_cos"] = np.cos(2 * np.pi * df["mes"] / 12)
    return df

def temporal_split(df: pd.DataFrame):
    """Cria splits de treino, validação e teste por faixa de datas."""
    df["split"] = "train"
    df.loc[df["ano"].between(2021, 2023), "split"] = "val"
    df.loc[df["ano"] >= 2024, "split"] = "test"
    return df

def save_final_dataset(df: pd.DataFrame, base_dir: Path):
    """Salva o dataset final de ML."""
    output_path = base_dir / "data" / "processed" / "ml_dataset.csv"
    df.to_csv(output_path, index=False)
    print(f"✅ Dataset final salvo em: {output_path}")
    return output_path

def prepare_ml_dataset(base_dir: Path):
    """Pipeline principal."""
    df = load_features(base_dir)
    df = create_targets(df)
    df = add_temporal_features(df)
    df = temporal_split(df)

    # Remover linhas finais com target NaN
    df = df.dropna(subset=["target_producao_next", "target_receita_next"])

    save_final_dataset(df, base_dir)
    return df
