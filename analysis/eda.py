import pandas as pd

def basic_stats(df: pd.DataFrame) -> pd.DataFrame:
    return df.describe(include="all").transpose()
