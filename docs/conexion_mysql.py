import os
import pandas as pd
from sqlalchemy import create_engine

# Configuración desde variables de entorno
usuario = os.getenv("DB_USER", "root")
contrasena = os.getenv("DB_PASSWORD", "12345678")
host = os.getenv("DB_HOST", "mysql")
base_datos = os.getenv("DB_NAME", "TFM")

cadena_conexion = f"mysql+pymysql://{usuario}:{contrasena}@{host}:3306/{base_datos}"

engine = create_engine(
    cadena_conexion,
    pool_pre_ping=True
)


def obtener_datos(limit=10):
    consulta_sql = f"""
        SELECT 
            p.anio, 
            p.mes, 
            n.nombre AS nacionalidad, 
            g.gasto_medio 
        FROM Gastos g
        JOIN Periodo p ON g.id_periodo = p.id_periodo
        JOIN Nacionalidad n ON g.id_nacionalidad = n.id_nacionalidad
        LIMIT {limit};
    """
    try:
        df = pd.read_sql(consulta_sql, con=engine)
        return df
    except Exception as e:
        print("Error al consultar la base de datos:", e)
        return pd.DataFrame()