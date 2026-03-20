import pandas as pd

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    
    df = df.copy()

    # Asegurar que los nombres de columnas sean strings
    df.columns = pd.Index([str(col) for col in df.columns])

    # Normalizar nombres de columnas
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    # Eliminar columnas completamente vacías
    df = df.dropna(axis=1, how="all")

    # Eliminar filas duplicadas
    df = df.drop_duplicates()

    # Lista de columnas que son porcentajes
    porcentaje_cols = ["porcentaje_compradores", "porcentaje_gasto", "porcentaje_transacciones"]
    
    # Convertir columnas numéricas si es posible
    for col in df.columns:
        try:
            df[col] = pd.to_numeric(df[col])
            if col in porcentaje_cols:
                df[col] = (df[col] * 100).round(2)
        except Exception:
            pass

    return df
