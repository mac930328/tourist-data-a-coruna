USE TFM;

-- ¿Cómo evoluciona el gasto medio a lo largo de los años y meses? ¿Existen picos estacionales (ej. verano, navidades)?
SELECT 
    p.anio, 
    p.mes, 
    ROUND(AVG(g.gasto_medio), 2) AS promedio_gasto_medio,
    ROUND(SUM(g.porcentaje_transacciones), 4) AS total_porcentaje_transacciones
FROM Gastos g
JOIN Periodo p ON g.id_periodo = p.id_periodo
GROUP BY p.anio, p.mes
ORDER BY p.anio ASC, p.mes ASC;

-- ¿Cuáles son los 10 países que concentran el mayor porcentaje de gasto y cuál es su gasto medio histórico?
SELECT 
    n.nombre AS nacionalidad,
    ROUND(AVG(g.gasto_medio), 2) AS gasto_medio_historico,
    ROUND(AVG(g.porcentaje_gasto) * 100, 2) AS cuota_de_gasto_promedio_pct
FROM Gastos g
JOIN Nacionalidad n ON g.id_nacionalidad = n.id_nacionalidad
GROUP BY n.nombre
ORDER BY cuota_de_gasto_promedio_pct DESC
LIMIT 10;

-- Gasto Medio de Todos
SELECT 
    CONCAT(REPLACE(ROUND(AVG(gasto_medio), 2), '.', ','), '€') AS gasto_medio_total
FROM Gastos;

-- Volumen promedio de actividad global
SELECT 
    CONCAT(REPLACE(ROUND(AVG(porcentaje_transacciones) * 100, 2), '.', ','), '%') AS promedio_actividad_transacciones,
    CONCAT(REPLACE(ROUND(AVG(porcentaje_compradores) * 100, 2), '.', ','), '%') AS promedio_actividad_compradores
FROM Gastos;

-- Volumen de actividad por Año y Mes
SELECT 
    p.anio AS año,
    p.mes AS mes,
    CONCAT(REPLACE(ROUND(AVG(g.porcentaje_transacciones) * 100, 2), '.', ','), '%') AS volumen_transacciones_medio,
    CONCAT(REPLACE(ROUND(AVG(g.porcentaje_compradores) * 100, 2), '.', ','), '%') AS volumen_compradores_medio
FROM Gastos g
JOIN Periodo p ON g.id_periodo = p.id_periodo
GROUP BY p.anio, p.mes
ORDER BY p.anio ASC, p.mes ASC;

-- ¿Qué combinación de Edad y Clase de Comprador es la más valiosa (la que tiene el gasto medio más alto)?
SELECT 
    c.nombre AS clase_comprador,
    r.nombre AS rango_edad,
    ROUND(AVG(g.gasto_medio), 2) AS gasto_medio,
    ROUND(AVG(g.porcentaje_compradores) * 100, 2) AS peso_demografico_pct
FROM Gastos g
JOIN Clase_Comprador c ON g.id_clase = c.id_clase
JOIN Rango_Edad r ON g.id_rango = r.id_rango
GROUP BY c.nombre, r.nombre
ORDER BY gasto_medio DESC;

-- ¿Qué tipo de clientes realizan muchas transacciones aunque sean pocos compradores? (Identificando la alta fidelidad).
SELECT 
    c.nombre AS clase_comprador,
    ROUND(SUM(g.porcentaje_transacciones) * 100, 2) AS total_transacciones_pct,
    ROUND(SUM(g.porcentaje_compradores) * 100, 2) AS total_compradores_pct,
    ROUND(SUM(g.porcentaje_transacciones) / SUM(g.porcentaje_compradores), 2) AS ratio_fidelidad
FROM Gastos g
JOIN Clase_Comprador c ON g.id_clase = c.id_clase
GROUP BY c.nombre
ORDER BY ratio_fidelidad DESC;

-- Segmentación Demográfica
SELECT 
    g.*, -- Aquí van  columnas específicas que necesites
    r.nombre AS rango_edad
FROM Gastos g
JOIN Rango_Edad r ON g.id_rango = r.id_rango;

-- Cuando selecciona un rango específico. Por ejemplo menores de 40 años
SELECT 
    g.*, 
    r.nombre AS rango_edad
FROM Gastos g
JOIN Rango_Edad r ON g.id_rango = r.id_rango
WHERE r.nombre = 'Menos de 40 años';

--  Gasto medio y la cuota de gasto desglosada por País y por Tipo de Comprador
SELECT 
    n.nombre AS nacionalidad,
    c.nombre AS clase_comprador,
    ROUND(AVG(g.gasto_medio), 2) AS promedio_gasto_medio,
    CONCAT(REPLACE(ROUND(AVG(g.porcentaje_gasto) * 100, 2), '.', ','), '%') AS cuota_de_gasto
FROM Gastos g
JOIN Nacionalidad n ON g.id_nacionalidad = n.id_nacionalidad
JOIN Clase_Comprador c ON g.id_clase = c.id_clase
GROUP BY n.nombre, c.nombre
ORDER BY AVG(g.gasto_medio) DESC;

-- Perfil de Lealtad por Nacionalidad
SELECT 
    n.nombre AS nacionalidad,
    c.nombre AS clase_comprador,
    CONCAT(REPLACE(ROUND(AVG(g.porcentaje_compradores) * 100, 2), '.', ','), '%') AS distribucion_compradores,
    CONCAT(REPLACE(ROUND(AVG(g.porcentaje_transacciones) * 100, 2), '.', ','), '%') AS distribucion_transacciones,
    ROUND(AVG(g.gasto_medio), 2) AS gasto_medio_segmento
FROM Gastos g
JOIN Nacionalidad n ON g.id_nacionalidad = n.id_nacionalidad
JOIN Clase_Comprador c ON g.id_clase = c.id_clase
GROUP BY n.nombre, c.nombre
ORDER BY n.nombre ASC, AVG(g.porcentaje_compradores) DESC;

-- Composición del Mercado Turístico enfocada en la cuota de gasto por país y edad.
SELECT 
    n.nombre AS pais,
    r.nombre AS rango_edad,
    CONCAT(REPLACE(ROUND(AVG(g.porcentaje_gasto) * 100, 2), '.', ','), '%') AS cuota_de_gasto,
    ROUND(AVG(g.gasto_medio), 2) AS gasto_medio
FROM Gastos g
JOIN Nacionalidad n ON g.id_nacionalidad = n.id_nacionalidad
JOIN Rango_Edad r ON g.id_rango = r.id_rango
GROUP BY n.nombre, r.nombre
ORDER BY AVG(g.porcentaje_gasto) DESC;