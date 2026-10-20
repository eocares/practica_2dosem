CREATE DATABASE IF NOT EXISTS codelima CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE codelima;

CREATE TABLE intereses (
  id      INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  nombre  VARCHAR(60) NOT NULL UNIQUE,
  activo  TINYINT(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB;

CREATE TABLE clientes (
  id          INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  nombre      VARCHAR(80)  NOT NULL,
  email       VARCHAR(120) NOT NULL UNIQUE,
  telefono    VARCHAR(15)  NULL,
  interes_id  INT UNSIGNED NOT NULL,
  mensaje     VARCHAR(500) NULL,
  activo      TINYINT(1)   NOT NULL DEFAULT 1,   -- borrado lógico
  creado_en   TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  actualizado TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT fk_clientes_interes FOREIGN KEY (interes_id) REFERENCES intereses(id),
  CONSTRAINT chk_email CHECK (email LIKE '%_@_%._%')
) ENGINE=InnoDB;
CREATE INDEX idx_clientes_activo ON clientes(activo, creado_en);

INSERT INTO intereses (nombre) VALUES
 ('Python para principiantes'),('Desarrollo web'),('Bases de datos MySQL'),
 ('Java y JavaFX'),('Computación en la nube (AWS)');
INSERT INTO clientes (nombre,email,telefono,interes_id,mensaje) VALUES
 ('Ana Torres','ana@example.com','987654321',1,'Quiero empezar desde cero'),
 ('Luis Rojas','luis@example.com','912345678',4,'Busco horarios de noche'),
 ('María Quispe','maria@example.com',NULL,3,NULL);

-- Usuario remoto (Workbench / app). Cambia la clave.
-- CREATE USER 'webapp'@'%' IDENTIFIED BY 'cambia_esta_clave';
-- GRANT SELECT,INSERT,UPDATE ON codelima.* TO 'webapp'@'%'; FLUSH PRIVILEGES;
