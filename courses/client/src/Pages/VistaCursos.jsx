import { React, useState } from "react";
import Navbar from "../Components/NavBar";
import AcorcionCursos from "../Components/Accordion";

export const VistaCursos = () => {
  const isAdmin = true;
  const [paralelos, setParalelos] = useState([
    {
      curso: "fis120",
      paralelo: 200,
      limite_cupo: 60,
      jornada: "Diurna",
      campus_sede: "San Joaquin",
    },
    {
      curso: "fis120",
      paralelo: 201,
      limite_cupo: 80,
      jornada: "Diurna",
      campus_sede: "San Joaquin",
    },
    {
      curso: "inf326",
      paralelo: 200,
      limite_cupo: 70,
      jornada: "Diurna",
      campus_sede: "Casa Central",
    },
  ]);

  const [cursos, setCursos] = useState([
    {
      sigla: "inf232",
      nombre: "Curso oka",
      departamento: "informatica",
      prerequisitos: "",
    },
    {
      sigla: "inf326",
      nombre: "Arquitectura de Software",
      departamento: "informatica",
      prerequisitos: "",
    },
    {
      sigla: "mat021",
      nombre: "Matematicas 1",
      departamento: "matematica",
      prerequisitos: "",
    },
    {
      sigla: "mat022",
      nombre: "Matematicas 2",
      departamento: "matematica",
      prerequisitos: "mat021",
    },
    {
      sigla: "mat023",
      nombre: "Matematicas 3",
      departamento: "matematica",
      prerequisitos: "mat022",
    },
    {
      sigla: "fis120",
      nombre: "Fisica General 2",
      departamento: "fisica",
      prerequisitos: "mat022",
    },
  ]);

  const CrearParalelo = (paralelo) => {
    setParalelos([...paralelos, paralelo]);
  };

  const CrearCurso = (curso) => {
    setCursos([...cursos, curso]);
  };

  return (
    <>
      <Navbar />

      <AcorcionCursos
        cursos={cursos}
        paralelos={paralelos}
        crearCurso={CrearCurso}
        crearParalelo={CrearParalelo}


        isAdmin={isAdmin}
      />
    </>
  );
};

export default VistaCursos;
