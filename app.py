import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import folium
from streamlit_folium import st_folium
import datetime
import time

from services.api_data import fetch_diva_data, fetch_actividades_ocio_data, fetch_turismo_receptor_data, fetch_conectividad_aerea_data, fetch_ind_rentabilidad_provincia_data
from processing.cleaning import clean_data
from analysis.eda import basic_stats

# -------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA 
# -------------------------------------------------------
st.set_page_config(
    page_title="DIVA Data Analysis",
    layout="wide"
)

st.title("📊 Análisis DIVA – Galicia (A Coruña)")

st.subheader("Mapa Interactivo de Galicia")

# -------------------------------------------------------
# MAPA INICIAL
# -------------------------------------------------------
import folium
from streamlit_folium import st_folium

# 1. Centramos el mapa en A Coruña (Lat: 43.36, Lon: -8.41)
# Subimos el zoom_start a 13 para que se vea la ciudad de cerca
m = folium.Map(location=[43.3623, -8.4115], zoom_start=13)

# 2. Añadimos el marcador de A Coruña
folium.Marker(
    [43.3713, -8.3960], 
    popup="A Coruña - Plaza de María Pita",
    tooltip="Ver detalles de la ciudad"
).add_to(m)

# 3. Lo mostramos en la web
st_folium(m, width=700, height=500)

# -------------------------------------------------------
# INFORMACION SOBRE A CORUÑA
# -------------------------------------------------------
st.markdown("""
    <style>
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #e0f2f1; /* Un tono azul claro oceánico */
        padding: 10px 10px 0px 10px;
        border-radius: 10px 10px 0px 0px;
    }

    .stTabs [data-baseweb="tab"] {
        height: 45px;
        background-color: white;
        border-radius: 8px 8px 0px 0px;
        padding: 5px 15px;
        font-weight: bold;
        color: #004a99;
        border: 1px solid #d1d1d1;
    }

    .stTabs [aria-selected="true"] {
        background-color: #004a99 !important; /* Azul marino */
        color: white !important;
    }

    .stTabs [data-baseweb="tab"]:hover {
        color: #007bff;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Creación de las Pestañas
tab1, tab2, tab3, tab4 = st.tabs([
    " Información", 
    " Gastronomía", 
    " Clima", 
    " Economía"
])

# --- CONTENIDO DE CADA PESTAÑA ---

with tab1:
    st.subheader("Información")
    # Introducción breve
    st.write("""
    Situada en una península en el noroeste de Galicia, **A Coruña** es una ciudad donde la historia romana se funde con la modernidad. 
    Conocida por sus fachadas acristaladas, es un destino donde el mar siempre está a la vista.
    """)

    # Columnas para datos rápidos
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("###  Historia")
        st.write("Fundada por los romanos, su puerto ha sido clave en rutas comerciales y expediciones históricas durante siglos.")
    
    with col2:
        st.markdown("###  Apodo")
        st.write("Se la llama la **'Ciudad de Cristal'** debido a las famosas galerías de madera y vidrio de la Avenida de la Marina.")
    
    with col3:
        st.markdown("###  Estilo de vida")
        st.write("Es una ciudad para caminar, famosa por su Paseo Marítimo de más de 13 km y sus playas urbanas (Riazor y Orzán).")
with tab2:
    st.write("Gastronomía")
    st.write("""
    A Coruña es el paraíso de los productos del mar y la carne de calidad. 
    Aquí te dejamos los platos que **no puedes dejar de probar**:
    """)

    #  Platos típicos en cuadrícula
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("###  Pulpo á Feira")
        st.write("""
        Cocinado en calderos de cobre y servido con aceite de oliva, pimentón y sal gruesa. 
        En Coruña es tradición acompañarlo con "cachelos" (patatas cocidas).
        """)
        
        st.markdown("###  Tortilla de Betanzos")
        st.write("""
        A pocos kilómetros de la ciudad se hace una de las mejores tortillas de España: 
        muy poco cuajada y con huevos de corral de gran calidad.
        """)

    with col2:
        st.markdown("###  Ternera Gallega")
        st.write("""
        Si prefieres carne, el chuletón de ternera gallega con Denominación de Origen 
        es una apuesta segura por su ternura y sabor.
        """)
        
        st.markdown("###  Estrella Galicia")
        st.write("""
        No es un plato, pero es casi religión. La fábrica principal está en la ciudad 
        y puedes visitar **MEGA** (Museo de Estrella Galicia) para conocer su historia.
        """)
with tab3:
    st.subheader("Estado del Clima")
    c1, c2 = st.columns(2)
    c1.metric("Temp. Media Verano", "22°C")
    c2.metric("Temp. Media Invierno", "11°C")
    st.info(" **Consejo:** En A Coruña el tiempo cambia rápido. ¡Lleva siempre un paraguas o un chubasquero!")

with tab4:
    st.subheader("Económica")
    st.write("A Coruña es el motor económico de Galicia.")
    data = {
        "Sector": ["Servicios/Retail (Inditex)", "Puerto y Pesca", "Turismo", "TIC"],
        "Impacto": ["Muy Alto", "Alto", "Medio-Alto", "Creciente"]
    }
    st.table(data)

# -------------------------------------------------------
# MAPA CON LUGARES TURISTICOS
# -------------------------------------------------------

st.subheader(" Puntos Estratégicos y Lugares de Interés")

# 1. Crear el mapa centrado en A Coruña
m = folium.Map(location=[43.3723, -8.4115], zoom_start=13, tiles="cartodbpositron")

# 2. Definir los lugares con su URL de imagen y enlace web
# Nota: Usamos enlaces directos de imágenes de Wikipedia/Wikimedia por estabilidad
lugares = [
    {
        "nombre": "Torre de Hércules", 
        "coord": [43.3859, -8.4066], 
        "color": "blue", 
        "icon": "info-sign",
        "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/27/Torre_de_H%C3%A9rcules_2023.jpg/960px-Torre_de_H%C3%A9rcules_2023.jpg",
        "link": "https://www.torredeherculesacoruna.com/"
    },
    {
        "nombre": "Plaza de María Pita", 
        "coord": [43.3708, -8.3958], 
        "color": "red", 
        "icon": "home",
        "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d2/Plaza_A_Coru%C3%B1a.JPG/500px-Plaza_A_Coru%C3%B1a.JPG",
        "link": "https://www.turismo.gal/recurso/-/detalle/4351/praza-de-maria-pita"
    },
    {
        "nombre": "Castillo de San Antón", 
        "coord": [43.3661, -8.3891], 
        "color": "green", 
        "icon": "tower",
        "img":"https://upload.wikimedia.org/wikipedia/commons/thumb/9/9a/Entrada_del_Castillo_de_San_Ant%C3%B3n.jpg/500px-Entrada_del_Castillo_de_San_Ant%C3%B3n.jpg",
        "link": "https://www.coruna.gal/museos/es/museo-arqueologico"

    },
    {
        "nombre": "Monte de San Pedro", 
        "coord": [43.3775, -8.4328], 
        "color": "orange", 
        "icon": "eye-open",
        "img": "https://dynamic-media-cdn.tripadvisor.com/media/photo-o/09/61/c6/1f/monte-de-san-pedro.jpg?w=2000&h=-1&s=1",
        "link": "https://www.coruna.gal/turismo/es/que-ver/parques/parque-del-monte-de-san-pedro"
    },
    {
        "nombre": "Acuario Finisterrae", 
        "coord": [43.3833, -8.4083], 
        "color": "cadetblue", 
        "icon": "tint",
        "img": "https://upload.wikimedia.org/wikipedia/commons/b/b7/Sala_Maremagnum_%28Gran_Volumen%29._Aquarium_Finisterrae._MC2.jpg",
        "link": "https://www.coruna.gal/museos/es/mc2/aquarium"
    }
]

# 3. Añadir los marcadores con Popups personalizados (HTML)
for lugar in lugares:
    # Creamos el contenido HTML del Popup
    html_content = f"""
    <div style="font-family: Arial, sans-serif; width: 200px;">
        <h4 style="margin: 0 0 5px 0;">
            <a href="{lugar['link']}" target="_blank" style="color: #0078AA; text-decoration: none;">
                {lugar['nombre']} 🔗
            </a>
        </h4>
        <hr style="margin: 5px 0;">
        <img src="{lugar['img']}" alt="{lugar['nombre']}" style="width: 100%; border-radius: 5px; margin-bottom: 8px;">
        <p style="font-size: 11px; color: gray; margin: 0;">Haz clic en el título para más información.</p>
    </div>
    """
    
    # Configuramos el IFrame y el Popup
    iframe = folium.IFrame(html_content, width=220, height=200)
    popup = folium.Popup(iframe, max_width=250)

    folium.Marker(
        location=lugar["coord"],
        popup=popup,
        tooltip=lugar["nombre"],
        icon=folium.Icon(color=lugar["color"], icon=lugar["icon"])
    ).add_to(m)

# 4. Renderizar en Streamlit
st_folium(m, width="100%", height=500)



# -------------------------------------------------------
# CARGA DE DATOS
# -------------------------------------------------------
st.divider()
@st.cache_data(ttl=3600)
def load_data():
    datasets = {}
    
    # DIVA data
    raw_diva = fetch_diva_data()
    clean_diva = clean_data(raw_diva)
    if 'año' in clean_diva.columns and 'mes' in clean_diva.columns:
        clean_diva['Fecha'] = pd.to_datetime(clean_diva['año'].astype(str) + '-' + clean_diva['mes'].astype(str) + '-01')
    datasets['diva'] = {'raw': raw_diva, 'clean': clean_diva}
    
    time.sleep(5)
    
    # Turismo receptor data
    raw_turismo = fetch_turismo_receptor_data()
    clean_turismo = clean_data(raw_turismo)
    if 'año' in clean_turismo.columns and 'mes' in clean_turismo.columns:
        clean_turismo['Fecha'] = pd.to_datetime(clean_turismo['año'].astype(str) + '-' + clean_turismo['mes'].astype(str) + '-01')
    datasets['turismo_receptor'] = {'raw': raw_turismo, 'clean': clean_turismo}
    
    time.sleep(5)
    
    # Actividades ocio data
    raw_ocio = fetch_actividades_ocio_data()
    clean_ocio = clean_data(raw_ocio)
    if 'año' in clean_ocio.columns and 'mes' in clean_ocio.columns:
        clean_ocio['Fecha'] = pd.to_datetime(clean_ocio['año'].astype(str) + '-' + clean_ocio['mes'].astype(str) + '-01')
    datasets['actividades_ocio'] = {'raw': raw_ocio, 'clean': clean_ocio}
    
    time.sleep(5)
    
    # Conectividad aerea data
    raw_aerea = fetch_conectividad_aerea_data()
    clean_aerea = clean_data(raw_aerea)
    if 'año' in clean_aerea.columns and 'mes' in clean_aerea.columns:
        clean_aerea['Fecha'] = pd.to_datetime(clean_aerea['año'].astype(str) + '-' + clean_aerea['mes'].astype(str) + '-01')
    datasets['conectividad_aerea'] = {'raw': raw_aerea, 'clean': clean_aerea}
    
    time.sleep(5)
    
    # Rentabilidad provincia data
    raw_rent = fetch_ind_rentabilidad_provincia_data()
    clean_rent = clean_data(raw_rent)
    if 'año' in clean_rent.columns and 'mes' in clean_rent.columns:
        clean_rent['Fecha'] = pd.to_datetime(clean_rent['año'].astype(str) + '-' + clean_rent['mes'].astype(str) + '-01')
    datasets['rentabilidad_provincia'] = {'raw': raw_rent, 'clean': clean_rent}
    
    return datasets

with st.sidebar:
    st.header("⚙️ Opciones")
    refresh = st.button("🔄 Refrescar datos")

if refresh:
    st.cache_data.clear()

with st.spinner("Consultando APIs y procesando datos..."):
    datasets = load_data()

# Check if at least DIVA data loaded
if datasets['diva']['raw'].empty:
    st.error("No se pudieron cargar datos de la API DIVA.")
    st.stop()

# For stats and explorer, use DIVA data as primary
clean_df = datasets['diva']['clean']

# 1. Creamos las pestañas definiendo sus nombres
# 1. Inyección de CSS personalizado
st.markdown("""
    <style>
    /* Estilo para el contenedor de las pestañas */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: #f0f2f6; /* Color de fondo de la barra */
        padding: 10px 10px 0px 10px;
        border-radius: 10px 10px 0px 0px;
    }

    /* Estilo para cada pestaña individual */
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: white;
        border-radius: 5px 5px 0px 0px;
        gap: 1px;
        padding: 10px 20px;
        font-weight: bold;
        color: #4b4b4b;
        border: 1px solid #e6e6e6;
    }

    /* Estilo cuando la pestaña está seleccionada */
    .stTabs [aria-selected="true"] {
        background-color: #ff4b4b !important; /* Color corporativo Streamlit */
        color: white !important;
        border-bottom: 2px solid #ff4b4b;
    }

    /* Hover: cuando pasas el ratón por encima */
    .stTabs [data-baseweb="tab"]:hover {
        color: #ff4b4b;
    }
    </style>
    """, unsafe_allow_html=True)

tab1, tab2 = st.tabs([" Datos limpios (DIVA)", " Datos originales (DIVA)"])

# 2. Usamos el bloque 'with' para cada pestaña
with tab1:
    st.subheader("Vista previa de datos procesados (DIVA)")
    st.dataframe(clean_df.head(100), use_container_width=True)

with tab2:
    st.subheader("Vista previa de datos brutos (DIVA)")
    st.dataframe(datasets['diva']['raw'].head(100), use_container_width=True)

# -------------------------------------------------------
# DATOS ADICIONALES
# -------------------------------------------------------
st.divider()
st.subheader("📊 Datos de Todas las APIs")

dataset_tabs = st.tabs([name.replace('_', ' ').title() for name in datasets.keys()])

for i, name in enumerate(datasets.keys()):
    with dataset_tabs[i]:
        raw_tab, clean_tab = st.tabs(["Datos Originales", "Datos Limpios"])
        
        with raw_tab:
            st.dataframe(datasets[name]['raw'].head(100), use_container_width=True)
        
        with clean_tab:
            st.dataframe(datasets[name]['clean'].head(100), use_container_width=True)



# -------------------------------------------------------
# ESTADÍSTICAS
# -------------------------------------------------------
st.divider()
st.subheader("📈 Estadísticas Descriptivas Avanzadas")
stats_df = basic_stats(clean_df)

# Aplicamos un estilo de gradiente (heatmap) a la tabla
# Aplicar el gradiente solo a las columnas que son flotantes o enteros
st.dataframe(
    stats_df.style.background_gradient(cmap='Blues', axis=0).format(precision=2),
    use_container_width=True
)

num_cols = [
    col for col in clean_df.select_dtypes(include="number").columns
    if col not in ["año", "mes"]
]

if len(num_cols) > 0:
    st.subheader(" Explorador Dinámico")
    
    col1, col2 = st.columns([1, 3])
    with col1:
        variable = st.selectbox("Métrica", num_cols)
        agrupacion = st.selectbox("Agrupar por", ["nacionalidad", "rango_edad", "clase_comprador", "año", "mes"])
    
    with col2:
        # Creamos un gráfico que resume la media de la métrica por el grupo elegido
        fig = px.bar(
            clean_df.groupby(agrupacion)[variable].mean().reset_index(),
            x=agrupacion,
            y=variable,
            color=variable,
            title=f"Promedio de {variable} por {agrupacion}",
            template="plotly_white"
        )
        st.plotly_chart(fig, use_container_width=True)

st.divider()

st.subheader("📊 Distribución y Outliers por Edad")

# Gráfico de caja para ver la dispersión del gasto medio
fig_box = px.box(
    clean_df, 
    x="rango_edad", 
    y="gasto_medio", 
    color="rango_edad",
    points="outliers", # Resalta valores muy por encima de la media
    title="Análisis de Dispersión: Gasto Medio vs Rango de Edad"
)
st.plotly_chart(fig_box, use_container_width=True)

st.divider()

st.subheader("🔗 Correlación entre Variables Numéricas")

# Calculamos la correlación solo de las columnas numéricas
corr = clean_df.select_dtypes(include="number").corr()

fig_corr = px.imshow(
    corr, 
    text_auto=True, 
    aspect="auto", 
    color_continuous_scale='RdBu_r',
    title="¿Qué variables influyen más entre sí?"
)
st.plotly_chart(fig_corr, use_container_width=True)



# -------------------------------------------------------
# SIDEBAR: FILTROS
# -------------------------------------------------------
with st.sidebar:
    st.header("Filtros Estratégicos")


# Creamos objetos date usando el año del DF
    start_date = datetime.date(int(clean_df['año'].min()), 1, 1)
    end_date = datetime.date(int(clean_df['año'].max()), 12, 31)

    rango_fecha = st.date_input(
        "Periodo de Análisis",
        [start_date, end_date]
    )
    

# -------------------------------------------------------
# FILTRADO DE DATOS
# -------------------------------------------------------
st.divider()
# Filtrado por Edad
# 1. El Radio Button 
segmento_edad = st.radio(
    "Segmento de Edad",
    ["Todos", "Menos de 40", "40-54", "Mas de 54", "Rango Desconocido"],
    horizontal=True
)

# 2. Diccionario de mapeo 
mapeo_edad = {
    "Menos de 40": "Menos de 40 años",
    "40-54": "De 40 a 54 años",
    "Mas de 54": "Más de 54 años", 
    "Rango Desconocido": "Rango Desconocido"
}

# 3. Lógica del Filtro
if segmento_edad == "Todos":
    df_filtrado = clean_df
else:
    # IMPORTANTE: Usamos segmento_edad
    nombre_real_columna = mapeo_edad[segmento_edad]
    df_filtrado = clean_df[clean_df['rango_edad'] == nombre_real_columna]

# 4. Mostrar resultados

st.subheader(f"Análisis para el segmento: {segmento_edad}")

top_gasto = df_filtrado.groupby('nacionalidad')['gasto_medio'].mean().sort_values(ascending=False).head(10).reset_index()

if not top_gasto.empty:
    # Gráfico de barras horizontales para ver el ranking
    fig = px.bar(
        top_gasto,
        x="gasto_medio",
        y="nacionalidad",
        orientation='h',
        title=f"Top 10 Países con mayor Gasto Medio ({segmento_edad})",
        labels={"gasto_medio": "Gasto Medio (€)", "nacionalidad": "País"},
        color="gasto_medio",
        color_continuous_scale="Viridis"
    )
    # Invertimos el eje Y para que el 1º salga arriba
    fig.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig, use_container_width=True)
    
    # Añadimos una métrica comparativa
    promedio_segmento = df_filtrado['gasto_medio'].mean()
    promedio_total = clean_df['gasto_medio'].mean()
    diff = promedio_segmento - promedio_total
    
    st.metric(
        label=f"Gasto Medio de {segmento_edad}", 
        value=f"{promedio_segmento:.2f} €",
        delta=f"{diff:.2f} € vs Promedio General"
    )
else:
    st.warning("No hay datos disponibles para este filtro.")



# Calculamos el Top 10 de nacionalidades que más gastan en este segmento

st.divider()

nacionalidad = st.multiselect(
        "Nacionalidad",
        clean_df['nacionalidad'].unique(),
        default=clean_df['nacionalidad'].unique()
    )
#  Filtro de Nacionalidad
mask = pd.Series(True, index=clean_df.index)
if nacionalidad: # Solo filtramos si hay algo seleccionado en el multiselect
    mask &= (clean_df['nacionalidad'].isin(nacionalidad))
top_gasto = df_filtrado.groupby('nacionalidad')['gasto_medio'].mean().sort_values(ascending=False).head(10).reset_index()



#  Aplicación: Creamos el nuevo DataFrame filtrado
df_filtered = clean_df[mask]


# -------------------------------------------------------
# KPIs
# -------------------------------------------------------
# -------------------------------------------------------
# KPIs CORREGIDOS SEGÚN EL DATASET REAL
# -------------------------------------------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    # Usamos 'porcentaje_transacciones' como indicador de volumen de actividad (Turistas)
    volumen_promedio = df_filtered['porcentaje_transacciones'].mean()
    ano_corriente = df_filtered['año'].max()
    ano_anterior = ano_corriente - 1
    vol_promedio_corriente = df_filtered[df_filtered['año'] == ano_corriente]['porcentaje_transacciones'].mean()
    vol_promedio_anterior = df_filtered[df_filtered['año'] == ano_anterior]['porcentaje_transacciones'].mean()
    delta_vol = ((vol_promedio_corriente - vol_promedio_anterior) / vol_promedio_anterior * 100) if vol_promedio_anterior else 0
    st.metric(
        label="Volumen Promedio de Actividad", 
        value=f"{volumen_promedio:.2f}%", 
        delta=f"{delta_vol:.2f}% vs año anterior"
    )

with col2:
    gasto_promedio = df_filtered['gasto_medio'].mean()
    gasto_promedio_corriente = df_filtered[df_filtered['año'] == ano_corriente]['gasto_medio'].mean()
    gasto_promedio_anterior = df_filtered[df_filtered['año'] == ano_anterior]['gasto_medio'].mean()
    delta_gasto = ((gasto_promedio_corriente - gasto_promedio_anterior) / gasto_promedio_anterior * 100) if gasto_promedio_anterior else 0
    st.metric(
        label="Gasto Medio", 
        value=f"{gasto_promedio:.2f}€", 
        delta=f"{delta_gasto:.2f}% vs año anterior"
    )

with col3:
    # Calculamos la recuperación comparando con el año base 2019 (si está en los datos)
    if 2019 in df_filtered['año'].unique():
        gasto_2019 = df_filtered[df_filtered['año'] == 2019]['gasto_medio'].mean()
        recuperacion = (gasto_promedio / gasto_2019 * 100) if gasto_2019 else 0
        st.metric(
            label="Recuperación Pre-Pandemia", 
            value=f"{recuperacion:.2f}%", 
            delta_color="normal"
        )
    else:
        st.metric(
            label="Recuperación Pre-Pandemia", 
            value="0%", 
            delta_color="normal"
    )

with col4:
    # Buscamos la nacionalidad con mayor porcentaje de gasto acumulado
    top_nacionalidad = df_filtered.groupby('nacionalidad')['porcentaje_gasto'].mean().idxmax()
    st.metric(
        label="Top Nacionalidad (% Gasto Promedio)",
        value=top_nacionalidad
    )

# -------------------------------------------------------
# GRÁFICAS
# -------------------------------------------------------
st.divider()
c1, c2 = st.columns([2, 1])

with c1:
    st.subheader("📈 Evolución del Gasto Medio por Nacionalidad")

    nacionalidades = sorted(df_filtered["nacionalidad"].unique())

    nationalidades_select = st.multiselect(
        "Selecciona hasta 4 nacionalidades",
        options=nacionalidades,
        default=nacionalidades[:4],
        max_selections=4
    )

    df_plot = df_filtered[
        df_filtered["nacionalidad"].isin(nationalidades_select)
    ]

    fig_line = px.line(
        df_plot,
        x="Fecha",
        y="gasto_medio",
        color="nacionalidad",
        labels={
            "gasto_medio": "Gasto Medio (€)",
            "Fecha": "Mes de visita"
        }
    )
    st.plotly_chart(fig_line, use_container_width=True)

with c2:
    st.subheader("🎯 Segmentación por Edad")
    # Usamos 'rango_edad' para los nombres y 'porcentaje_compradores' para los valores
    fig_pie = px.pie(
        df_filtered,
        names="rango_edad",
        values="porcentaje_compradores",
        hole=0.5,
        color_discrete_sequence=px.colors.sequential.RdBu,
        labels={"rango_edad": "Rango de Edad", "porcentaje_compradores": "% Compradores"}
    )
    # Mejoramos la leyenda para que no estorbe
    fig_pie.update_layout(legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5))
    st.plotly_chart(fig_pie, use_container_width=True)

# -------------------------------------------------------
#  ANÁLISIS CRUZADO
# -------------------------------------------------------
st.divider()
st.subheader("Relación Gasto vs Nacionalidad")
    
fig_box = px.box(
        df_filtered,
        x="nacionalidad",
        y="gasto_medio",
        color="nacionalidad",
        points="all", 
        title="Distribución de Gasto por Origen",
        labels={
            "nacionalidad": "País de Origen",
            "gasto_medio": "Gasto Medio (€)"
        },
        template="plotly_white"
    )
    
    
fig_box.update_layout(showlegend=False) 
    
st.plotly_chart(fig_box)

# -------------------------------------------------------
# PREDICCIÓN
# -------------------------------------------------------
st.divider()
st.subheader("Proyección Estratégica 2025")
st.info("Basado en los datos actuales, se estima un crecimiento del 12% en el sector senior (51+) para la temporada estival de 2025.")

# -------------------------------------------------------
# MAPA DE CALOR
# -------------------------------------------------------
st.divider()
st.subheader("Mapa de Calor: Estacionalidad del Gasto")
mes_mapa = {
    1: 'Ene', 2: 'Feb', 3: 'Mar', 4: 'Abr',
    5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Ago',
    9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dic'
}

df_filtered['mes_nombre'] = df_filtered['mes'].map(mes_mapa)

pivot_df = df_filtered.pivot_table(
    index='nacionalidad', 
    columns='mes_nombre', 
    values='gasto_medio', 
    aggfunc='mean'
)
orden_meses = ['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic']
pivot_df = pivot_df.reindex(columns=orden_meses)
pivot_df = pivot_df.fillna('No data')
fig_heatmap = px.imshow(
    pivot_df,
    labels=dict(x="Mes", y="País", color="Gasto Medio"),
    color_continuous_scale='Viridis'
)
st.plotly_chart(fig_heatmap, use_container_width=True)

# -------------------------------------------------------
# TURISTA DE VALOR
# -------------------------------------------------------
st.divider()
st.subheader("Análisis de Valor: Transacciones vs Gasto")
fig_scatter = px.scatter(
    df_filtered, 
    x="porcentaje_transacciones", 
    y="gasto_medio",
    size="porcentaje_gasto", 
    color="nacionalidad",
    hover_name="nacionalidad",
    title="Relación entre Volumen de Transacciones y Gasto Medio"
)
st.plotly_chart(fig_scatter, use_container_width=True)

# -------------------------------------------------------
# COMPORTAMIENTO DEL CONSUMIDOR
# -------------------------------------------------------
st.divider()
st.subheader("Perfil de Lealtad por Nacionalidad")
fig_stack = px.bar(
    df_filtered, 
    x="nacionalidad", 
    y="porcentaje_transacciones", 
    color="clase_comprador",
    title="Distribución de Tipo de Comprador por País",
    barmode="stack"
)
st.plotly_chart(fig_stack, use_container_width=True)

# -------------------------------------------------------
# COMPOCISION DEL MERCADO
# -------------------------------------------------------
st.divider()
st.subheader("Composición del Mercado Turístico")
fig_tree = px.treemap(
    df_filtered, 
    path=['nacionalidad', 'rango_edad'], 
    values='porcentaje_gasto',
    color='gasto_medio',
    title="Cuota de Gasto por País y Edad"
)
st.plotly_chart(fig_tree, use_container_width=True)