import React from "react";
import './HorarioTable.css'; // Importar estilos personalizados

function HorarioTable({ bloqueId }) {
  // Datos de ejemplo de horarios para cada bloque y día de la semana
  const horarios = [
    { id: 1, bloque_id: 101, dia: "Lunes", hora: "08:00", ocupado: true },
    { id: 2, bloque_id: 101, dia: "Lunes", hora: "10:00", ocupado: false },
    { id: 3, bloque_id: 101, dia: "Martes", hora: "08:00", ocupado: true },
    { id: 4, bloque_id: 102, dia: "Miércoles", hora: "10:00", ocupado: false },
    { id: 5, bloque_id: 102, dia: "Miércoles", hora: "12:00", ocupado: true },
    { id: 6, bloque_id: 103, dia: "Jueves", hora: "08:00", ocupado: true },
    { id: 7, bloque_id: 103, dia: "Viernes", hora: "12:00", ocupado: false },
    // Más horarios según sea necesario
  ];

  // Filtrar los horarios por bloqueId
  const horariosFiltrados = horarios.filter((horario) => horario.bloque_id === bloqueId);

  // Definir los días de la semana
  const diasSemana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"];

  return (
    <div className="horario-table-container">
      <table className="horario-table">
        <thead>
          <tr>
            <th>Hora</th>
            {diasSemana.map((dia) => (
              <th key={dia}>{dia}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {/* Horas predefinidas (8:00, 10:00, 12:00, etc.) */}
          {["08:00", "10:00", "12:00", "14:00", "16:00", "18:00", "20:00"].map((hora) => (
            <tr key={hora}>
              <td>{hora}</td>
              {diasSemana.map((dia) => {
                // Buscar el horario correspondiente para cada día y hora
                const horario = horariosFiltrados.find(
                  (h) => h.dia === dia && h.hora === hora
                );
                const isOcupado = horario ? horario.ocupado : false;

                return (
                  <td key={dia} className={isOcupado ? "ocupado" : "vacío"}>
                    {isOcupado ? "Ocupado" : "Vacío"}
                  </td>
                );
              })}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default HorarioTable;
