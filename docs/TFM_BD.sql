-- Crear base de datos si no existe
CREATE DATABASE IF NOT EXISTS TFM;
USE TFM;

-- Dimensión: Periodo (Año y mes)
CREATE TABLE IF NOT EXISTS Periodo (
    id_periodo INT AUTO_INCREMENT PRIMARY KEY,
    anio INT NOT NULL,
    mes INT NOT NULL CHECK (mes BETWEEN 1 AND 12),
    UNIQUE KEY uk_periodo (anio, mes)
);

-- Dimensión: Nacionalidad
CREATE TABLE IF NOT EXISTS Nacionalidad (
    id_nacionalidad INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE
);

-- Dimensión: Clase_Comprador
CREATE TABLE IF NOT EXISTS Clase_Comprador (
    id_clase INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE
);

-- Dimensión: Rango_Edad
CREATE TABLE IF NOT EXISTS Rango_Edad (
    id_rango INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE
);

-- Fact Table: Gastos
CREATE TABLE IF NOT EXISTS Gastos (
    id_gasto BIGINT AUTO_INCREMENT PRIMARY KEY,
    id_periodo INT NOT NULL,
    id_nacionalidad INT NOT NULL,
    id_clase INT NOT NULL,
    id_rango INT NOT NULL,
    gasto_medio DECIMAL(15,5) NOT NULL,
    porcentaje_transacciones DECIMAL(15,5) NOT NULL,
    porcentaje_compradores DECIMAL(15,5) NOT NULL,
    porcentaje_gasto DECIMAL(15,5) NOT NULL,
    FOREIGN KEY (id_periodo) REFERENCES Periodo(id_periodo),
    FOREIGN KEY (id_nacionalidad) REFERENCES Nacionalidad(id_nacionalidad),
    FOREIGN KEY (id_clase) REFERENCES Clase_Comprador(id_clase),
    FOREIGN KEY (id_rango) REFERENCES Rango_Edad(id_rango),
    UNIQUE KEY uk_gastos (id_periodo, id_nacionalidad, id_clase, id_rango),
    INDEX idx_gastos_periodo (id_periodo),
    INDEX idx_gastos_nacionalidad (id_nacionalidad)
);

SET SQL_SAFE_UPDATES = 0;