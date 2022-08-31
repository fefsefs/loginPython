-- primera database sql
-- seleccionar las consultas para ejecutarlas

show databases;
use Usuarios;
create TABLE usuarios (
	id int,
    nombre varchar(255),
    edad int,
    contrasenia varchar(255),
    email varchar(255),
    PRIMARY KEY (id)
);

INSERT INTO usuarios (nombre, edad) VALUES ('Felipe', 17);

ALTER TABLE usuarios MODIFY COLUMN id int auto_increment;

SHOW CREATE TABLE usuarios;


CREATE TABLE `usuarios` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) DEFAULT NULL,
  `edad` int DEFAULT NULL,
  `contrasenia` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
);

INSERT INTO usuarios (nombre, edad) VALUES ('Felipe', 17);
INSERT INTO usuarios (nombre, edad) VALUES ('Crave', 17);
INSERT INTO usuarios (nombre, edad) VALUES ('Ricardo', 17);

SELECT * FROM usuarios;
SELECT * FROM usuarios WHERE id = 1;
SELECT * FROM usuarios WHERE nombre = 'Crave';
SELECT * FROM usuarios WHERE edad= 17 AND nombre = 'Felipe';

UPDATE usuarios SET nombre = 'topo' where id = 3;
-- para borrar registros usar el id!!!!!!
DELETE from usuarios where id = 4;