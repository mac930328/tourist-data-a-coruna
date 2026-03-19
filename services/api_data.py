import requests
import pandas as pd
from io import BytesIO

BASE_URL = "https://dataestur.azure-api.net/API-SEGITTUR-v1"

TURISMO_RECEPTOR_MUN_PAIS_DL_URL = (
    BASE_URL +
    "/TURISMO_RECEPTOR_MUN_PAIS_DL" +
    "?CCAA=Galicia&Provincia=Todos"
)

DIVA_DL_URL = (
    BASE_URL +
    "/DIVA_DL" +
    "?CCAA=Galicia&Provincia=Coru%C3%B1a%2C%20A"
)

ACTIVIDADES_OCIO_DL_URL = (
    BASE_URL +
    "/ACTIVIDADES_OCIO_DL" +
    "?CCAA=Galicia&Provincia=A%20Coru%C3%B1a"  
)

CONECTIVIDAD_AEREA_RESERVAS_MOMENTO_COMPRA_DL_URL = (
    BASE_URL +
    "/CONECTIVIDAD_AEREA_RESERVAS_MOMENTO_COMPRA_DL" +
    "?Pa%C3%ADs%20origen=Todos&Ciudad%20destino=Coru%C3%B1a%2C%20A&Tipo%20origen=Todos"  
)

IND_RENTABILIDAD_PROVINCIA_DL_URL = (
    BASE_URL +
    "/IND_RENTABILIDAD_PROVINCIA_DL" +
    "?Provincia=A%20Coru%C3%B1a"
)

HEADERS = {
    "octect-stream":{
        "accept": "application/octet-stream"
    },
    "vnd-ms-excel":{
        "accept": "application/vnd.ms-excel"
    }
}

def fetch_diva_data():
    try:
        response = requests.get(DIVA_DL_URL, headers=HEADERS["octect-stream"], timeout=15)
        response.raise_for_status()

        for enc in ("utf-8", "latin-1", "iso-8859-1", "cp1252"):
            try:
                df = pd.read_csv(
                    BytesIO(response.content),
                    encoding=enc,
                    sep=";",
                    decimal=","
                )
                return df
            except Exception:
                continue

        print("No se pudo decodificar el CSV con ningún encoding, retornando DataFrame vacío")
        return pd.DataFrame()

    except requests.exceptions.Timeout:
        print("Timeout al conectar con la API al obtener el dataset DIVA_DL")
        return pd.DataFrame()

    except requests.exceptions.RequestException as e:
        print(f"Error en la API: {e}")
        return pd.DataFrame()
    
def fetch_turismo_receptor_data():
    try:
        response = requests.get(TURISMO_RECEPTOR_MUN_PAIS_DL_URL, headers=HEADERS["octect-stream"], timeout=60)
        response.raise_for_status()

        for enc in ("utf-8", "latin-1", "iso-8859-1", "cp1252"):
            try:
                df = pd.read_csv(
                    BytesIO(response.content),
                    encoding=enc,
                    sep=";",
                    decimal=","
                )
                return df
            except Exception:
                continue

        print("No se pudo decodificar el CSV con ningún encoding, retornando DataFrame vacío")
        return pd.DataFrame()

    except requests.exceptions.Timeout:
        print("Timeout al conectar con la API al obtener el dataset TURISMO_RECEPTOR_MUN_PAIS_DL")
        return pd.DataFrame()

    except requests.exceptions.RequestException as e:
        print(f"Error en la API: {e}")
        return pd.DataFrame()

def fetch_actividades_ocio_data():
    try:
        response = requests.get(ACTIVIDADES_OCIO_DL_URL, headers=HEADERS["vnd-ms-excel"], timeout=15)
        response.raise_for_status()

        for enc in ("utf-8", "latin-1", "iso-8859-1", "cp1252"):
            try:
                df = pd.read_csv(
                    BytesIO(response.content),
                    encoding=enc,
                    sep=";",
                    decimal=","
                )
                return df
            except Exception:
                continue

        # Si no funciona como CSV, intentar como Excel
        try:
            df = pd.read_excel(BytesIO(response.content))
            return df
        except Exception:
            pass

        print("No se pudo decodificar el archivo con ningún método, retornando DataFrame vacío")
        return pd.DataFrame()

    except requests.exceptions.Timeout:
        print("Timeout al conectar con la API al obtener el dataset ACTIVIDADES_OCIO_DL")
        return pd.DataFrame()

    except requests.exceptions.RequestException as e:
        print(f"Error en la API: {e}")
        return pd.DataFrame()

def fetch_conectividad_aerea_data():
    try:
        response = requests.get(CONECTIVIDAD_AEREA_RESERVAS_MOMENTO_COMPRA_DL_URL, headers=HEADERS["vnd-ms-excel"], timeout=15)
        response.raise_for_status()

        for enc in ("utf-8", "latin-1", "iso-8859-1", "cp1252"):
            try:
                df = pd.read_csv(
                    BytesIO(response.content),
                    encoding=enc,
                    sep=";",
                    decimal=","
                )
                return df
            except Exception:
                continue

        # Si no funciona como CSV, intentar como Excel
        try:
            df = pd.read_excel(BytesIO(response.content))
            return df
        except Exception:
            pass

        print("No se pudo decodificar el archivo con ningún método, retornando DataFrame vacío")
        return pd.DataFrame()

    except requests.exceptions.Timeout:
        print("Timeout al conectar con la API al obtener el dataset CONECTIVIDAD_AEREA_RESERVAS_MOMENTO_COMPRA_DL")
        return pd.DataFrame()

    except requests.exceptions.RequestException as e:
        print(f"Error en la API: {e}")
        return pd.DataFrame()

def fetch_ind_rentabilidad_provincia_data():
    try:
        response = requests.get(IND_RENTABILIDAD_PROVINCIA_DL_URL, headers=HEADERS["vnd-ms-excel"], timeout=15)
        response.raise_for_status()

        for enc in ("utf-8", "latin-1", "iso-8859-1", "cp1252"):
            try:
                df = pd.read_csv(
                    BytesIO(response.content),
                    encoding=enc,
                    sep=";",
                    decimal=","
                )
                return df
            except Exception:
                continue

        # Si no funciona como CSV, intentar como Excel
        try:
            df = pd.read_excel(BytesIO(response.content))
            return df
        except Exception:
            pass

        print("No se pudo decodificar el archivo con ningún método, retornando DataFrame vacío")
        return pd.DataFrame()

    except requests.exceptions.Timeout:
        print("Timeout al conectar con la API al obtener el dataset IND_RENTABILIDAD_PROVINCIA_DL")
        return pd.DataFrame()

    except requests.exceptions.RequestException as e:
        print(f"Error en la API: {e}")
        return pd.DataFrame()   
