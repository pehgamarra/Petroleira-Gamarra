import pandas as pd
from pathlib import Path

def consolidate_metrics(base_dir="../models", output_file="../models/all_metrics.csv"):
    BASE_DIR = Path(base_dir)
    metric_files = list(BASE_DIR.glob("*_metrics.csv"))

    def normalize_columns(df):
        df = df.copy()
        rename_map = {
            'MODEL': 'modelo', 'MODEL_NAME': 'modelo',
            'mae': 'MAE', 'rmse': 'RMSE', 'mape': 'MAPE', 'r2': 'R2',
            'target': 'target'
        }
        df = df.rename(columns=rename_map)
        keep_cols = ['target', 'modelo', 'MAE', 'RMSE', 'MAPE', 'R2']
        for col in keep_cols:
            if col not in df.columns:
                df[col] = pd.NA
        return df[keep_cols]

    dfs = [normalize_columns(pd.read_csv(f)) for f in metric_files]
    all_metrics_df = pd.concat(dfs, ignore_index=True)
    all_metrics_df.to_csv(output_file, index=False)
    return all_metrics_df
