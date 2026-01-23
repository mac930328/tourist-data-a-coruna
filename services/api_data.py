import requests
import pandas as pd
from io import BytesIO

API_URL = (
    "https://dataestur.azure-api.net/API-SEGITTUR-v1/DIVA_DL"
    "?CCAA=Galicia&Provincia=Coru%C3%B1a%2C%20A"
)

HEADERS = {
    "accept": "application/octet-stream"
}

def fetch_diva_data():
    response = requests.get(API_URL)
    response.raise_for_status()

    for enc in ("utf-8", "latin-1", "iso-8859-1", "cp1252"):
        try:
            df = pd.read_csv(BytesIO(response.content), encoding=enc, sep=";", decimal=",")
            print(f"Leído correctamente con encoding: {enc}")
            print(df.head())
            print(df.columns.tolist())
            return df
        except UnicodeDecodeError:
            continue

    raise ValueError("No se pudo decodificar el CSV con ningún encoding")

