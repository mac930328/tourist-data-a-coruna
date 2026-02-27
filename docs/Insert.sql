USE TFM;

SET SQL_SAFE_UPDATES = 0;

-- Tabla temporal
CREATE TEMPORARY TABLE Staging_Gastos_Limpio (
    anio INT,
    mes INT,
    nacionalidad VARCHAR(100),
    clase_comprador VARCHAR(100),
    rango_edad VARCHAR(100),
    gasto_medio DECIMAL(15,5),
    porcentaje_transacciones DECIMAL(15,5),
    porcentaje_compradores DECIMAL(15,5),
    porcentaje_gasto DECIMAL(15,5)
);

-- Cargar CSV (SIN LOCAL y con ruta interna del contenedor)
LOAD DATA INFILE '/var/lib/mysql-files/diva_limpio.csv'
INTO TABLE Staging_Gastos_Limpio
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

-- Insertar dimensiones
INSERT IGNORE INTO Periodo (anio, mes)
SELECT DISTINCT anio, mes FROM Staging_Gastos_Limpio;

INSERT IGNORE INTO Nacionalidad (nombre)
SELECT DISTINCT nacionalidad FROM Staging_Gastos_Limpio;

INSERT IGNORE INTO Clase_Comprador (nombre)
SELECT DISTINCT clase_comprador FROM Staging_Gastos_Limpio;

INSERT IGNORE INTO Rango_Edad (nombre)
SELECT DISTINCT rango_edad FROM Staging_Gastos_Limpio;

-- Insertar tabla de hechos
INSERT IGNORE INTO Gastos (
    id_periodo, 
    id_nacionalidad, 
    id_clase, 
    id_rango, 
    gasto_medio, 
    porcentaje_transacciones, 
    porcentaje_compradores, 
    porcentaje_gasto
)
SELECT 
    p.id_periodo,
    n.id_nacionalidad,
    c.id_clase,
    r.id_rango,
    s.gasto_medio,
    s.porcentaje_transacciones,
    s.porcentaje_compradores,
    s.porcentaje_gasto
FROM Staging_Gastos_Limpio s
JOIN Periodo p ON s.anio = p.anio AND s.mes = p.mes
JOIN Nacionalidad n ON s.nacionalidad = n.nombre
JOIN Clase_Comprador c ON s.clase_comprador = c.nombre
JOIN Rango_Edad r ON s.rango_edad = r.nombre;