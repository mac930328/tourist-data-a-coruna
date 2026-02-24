
# DIVA Streamlit App – Galicia (A Coruña)

Aplicación interactiva desarrollada con **Streamlit** para consultar, limpiar y analizar datos de la **API DIVA (SEGITTUR)** para Galicia – provincia de A Coruña.

---

## Objetivos

- Consultar la API DIVA en tiempo real.
- Limpiar y normalizar los datos automáticamente.
- Proporcionar análisis exploratorio interactivo.
- Visualizar datos numéricos de manera sencilla.
- Permitir refrescar los datos con un botón.
- Garantizar coherencia en métricas agregadas mediante promedios (avg).
- Mostrar comparativas temporales dinámicas y métricas de recuperación fiables.

---

## Estructura del proyecto

```
diva-streamlit/
├── app.py                  # Aplicación principal Streamlit
├── services/
│   └── diva_api.py         # Funciones para consumir la API
├── processing/
│   └── cleaning.py         # Limpieza y transformación de datos
├── analysis/
│   └── eda.py              # Funciones de análisis exploratorio
├── requirements.txt        # Dependencias Python
└── README.md               # Documentación del proyecto
```

---

## Instalación y uso

1. Clonar el repositorio:

```bash
git clone https://github.com/LizethDayannaSC/tourist-data-a-coruna.git
cd diva-streamlit
```

2. Crear un entorno virtual (opcional):

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

3. Instalar dependencias:

```bash
pip install -r requirements.txt
```

4. Ejecutar la app:

```bash
streamlit run app.py
```

5. Abrir en el navegador:

```
http://localhost:8501
```

---

## Funcionalidades de la App

1. **Consulta de la API en tiempo real**
   - Descarga los datos cada vez que se inicia o se pulsa "Refrescar".

2. **Limpieza de datos**
   - Normaliza nombres de columnas (lowercase, `_` en lugar de espacios).
   - Elimina columnas vacías.
   - Elimina filas duplicadas.
   - Convierte automáticamente columnas numéricas.

3. **Análisis exploratorio (EDA)**
   - Estadísticas descriptivas de todas las columnas (`describe`).
   - Resumen de valores nulos.
   - Visualización de columnas numéricas.

4. **Interactividad**
   - Botón de "Refrescar datos".
   - Selector de columna para graficar.
   - Vistas de datos originales y limpios.

---

## Detalle de módulos

**services/diva_api.py**
- `fetch_diva_data()`: Consulta la API DIVA y devuelve un DataFrame de pandas.

**processing/cleaning.py**
- `clean_diva_data(df)`: Limpia, normaliza y transforma el DataFrame.

**analysis/eda.py**
- `basic_stats(df)`: Devuelve estadísticas descriptivas.
- `nulls_summary(df)`: Resumen de valores nulos.

**app.py**
- Script principal de Streamlit.
- Integra los módulos anteriores.
- Crea la interfaz web con:
  - Datos originales
  - Datos limpios
  - Estadísticas
  - Gráficos interactivos
  - Comparativas interanuales

---
## Mejoras implementadas en el MVP

- Todos los porcentajes ahora se calculan como promedios (avg) para garantizar coherencia en las métricas mostradas.
- Los deltas funcionan correctamente, calculándose dinámicamente frente al año anterior.
- La métrica de recuperación pre-pandemia refleja correctamente los valores reales frente al periodo base.
- Año y mes redefinidos como dimensiones analíticas.
- Límite de selección de nacionalidades en gráficos comparativos.
- Corrección en el mapa de calor mostrando NaN en ausencia de datos.

---

## Licencia

**MIT License** – libre para uso y modificación.
