import pandas as pd

def basic_stats(df: pd.DataFrame) -> pd.DataFrame:
    return df.describe(include="all").transpose()

def nulls_summary(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.isna()
        .sum()
        .to_frame("nulls")
        .assign(percent=lambda x: (x["nulls"] / len(df)) * 100)
        .sort_values("percent", ascending=False)
    )
