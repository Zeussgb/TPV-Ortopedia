CREATE DATABASE IF NOT EXISTS tpv_ortopedia;
USE tpv_ortopedia;

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    password VARCHAR(255) NOT NULL,
    rol VARCHAR(20) NOT NULL
);

CREATE TABLE productos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codigo VARCHAR(50) NOT NULL UNIQUE,
    nombre VARCHAR(150) NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    stock INT NOT NULL DEFAULT 0,
    stock_minimo INT NOT NULL DEFAULT 5
);

CREATE TABLE ventas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total DECIMAL(10,2) NOT NULL,
    tipo_pago VARCHAR(20) NOT NULL,
    dinero_entregado DECIMAL(10,2),
    cambio DECIMAL(10,2),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

CREATE TABLE lineas_venta (
    id INT AUTO_INCREMENT PRIMARY KEY,
    venta_id INT NOT NULL,
    producto_id INT NOT NULL,
    cantidad INT NOT NULL,
    precio_unitario DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (venta_id) REFERENCES ventas(id),
    FOREIGN KEY (producto_id) REFERENCES productos(id)
);

CREATE TABLE caja (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    fecha DATE NOT NULL,
    dinero_apertura DECIMAL(10,2) NOT NULL,
    dinero_cierre DECIMAL(10,2),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);