CREATE TABLE IF NOT EXISTS bloques_horario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(10) NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL
);

CREATE TABLE IF NOT EXISTS horarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    course_id INT NOT NULL,
    parallel_id INT NOT NULL,
    bloque_id INT,
    tipo VARCHAR(50),
    id_profesor INT NOT NULL,
    nombre_profesor VARCHAR(50),
    is_deleted TINYINT(1) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (bloque_id) REFERENCES bloques_horario(id)
);

INSERT INTO bloques_horario (nombre, hora_inicio, hora_fin) VALUES 
('1-2', '08:15:00', '09:25:00'),
('3-4', '09:40:00', '10:50:00'),
('5-6', '11:05:00', '12:15:00'),
('7-8', '12:30:00', '13:40:00'),
('9-10', '14:40:00', '15:50:00'),
('11-12', '16:05:00', '17:15:00'),
('13-14', '17:30:00', '18:40:00'),
('15-16', '18:50:00', '20:00:00'),
('17-18', '20:15:00', '21:25:00');