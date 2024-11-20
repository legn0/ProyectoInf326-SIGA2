import { React, useState, useEffect } from "react";
import Navbar from "../Components/NavBar";
import AcorcionCursos from "../Components/Accordion";
import HorarioTable from "../Components/HorarioTable";
import { useDisclosure, Button } from "@chakra-ui/icons";
import { useQuery, useMutation } from "@tanstack/react-query";
import { createCurso, getAllCursos } from "../api/courses";

export const VistaCursos = () => {
  const isAdmin = false;
  const horarioDisclosure = useDisclosure(false);
  const [selectedBlockId, setSelectedBlockID] = useState();
  const [horarioFiltrado, setHorarioFiltrado] = useState([]);

  const [paralelos, setParalelos] = useState([
    {
      curso: "fis120",
      paralelo: 200,
      limite_cupo: 60,
      jornada: "Diurna",
      campus_sede: "San Joaquin",
      block_id: 101,
    },
    {
      curso: "fis120",
      paralelo: 201,
      limite_cupo: 80,
      jornada: "Diurna",
      campus_sede: "San Joaquin",
      block_id: 102,
    },
    {
      curso: "inf326",
      paralelo: 200,
      limite_cupo: 70,
      jornada: "Diurna",
      campus_sede: "Casa Central",
      block_id: 103,
    },
  ]);

  // const [cursos, setCursos] = useState([
  //   {
  //     sigla: "inf232",
  //     nombre: "Curso oka",
  //     departamento: "informatica",
  //     prerequisitos: "",
  //   },
  //   {
  //     sigla: "inf326",
  //     nombre: "Arquitectura de Software",
  //     departamento: "informatica",
  //     prerequisitos: "",
  //   },
  //   {
  //     sigla: "mat021",
  //     nombre: "Matematicas 1",
  //     departamento: "matematica",
  //     prerequisitos: "",
  //   },
  //   {
  //     sigla: "mat022",
  //     nombre: "Matematicas 2",
  //     departamento: "matematica",
  //     prerequisitos: "mat021",
  //   },
  //   {
  //     sigla: "mat023",
  //     nombre: "Matematicas 3",
  //     departamento: "matematica",
  //     prerequisitos: "mat022",
  //   },
  //   {
  //     sigla: "fis120",
  //     nombre: "Fisica General 2",
  //     departamento: "fisica",
  //     prerequisitos: "mat022",
  //   },
  // ]);

  const horarios = [
    { id: 1, bloque_id: 101, dia: "Lunes", hora: "1-2", ocupado: true },
    { id: 3, bloque_id: 101, dia: "Martes", hora: "11-12", ocupado: true },
    { id: 5, bloque_id: 102, dia: "Miércoles", hora: "7-8", ocupado: true },
    { id: 6, bloque_id: 103, dia: "Jueves", hora: "3-4", ocupado: true },
    // Más horarios según sea necesario
  ];

  useEffect(() => {
    setHorarioFiltrado(horariosFiltrados(selectedBlockId));
  }, [selectedBlockId]);

  const horariosFiltrados = (bloqueId) =>
    horarios.filter((horario) => horario.bloque_id === bloqueId);

  const CrearParalelo = (paralelo) => {
    setParalelos([...paralelos, paralelo]);
  };

  // const CrearCurso = (curso) => {
  //   setCursos([...cursos, curso]);
  // };
  ///
  /// Coneccion con backennd
  const cursosQuery = useQuery({
    queryKey: ["courses"],
    queryFn: getAllCursos,
  });
  const createCursoMutation = useMutation({
    mutationFn: createCurso,
    onError: (data) => console.log("No lo pude mandar"),
  });

  const CrearCurso = (curso) => {
    createCursoMutation.mutate({
      name: curso.nombre,
      sigla: curso.sigla,
      creditos: curso.creditos,
      departamento: curso.departamennto,
      prerequisites: curso.prerequisitos,
    });
  };


  useEffect(()=>{
    console.log(cursosQuery.data)
  }, [cursosQuery])


  const rendering = ()=>{
      if (cursosQuery.status === "pending"){
        return <h1>Loading cursos...</h1>  }
      else if (cursosQuery.status === "error"){
        return <h1>Error fetching cursos: {cursosQuery.error.message}</h1>
      } else if (cursosQuery.status ==="success"){
        return <AcorcionCursos
        cursos={cursosQuery.data}
        paralelos={paralelos}
        crearCurso={CrearCurso}
        crearParalelo={CrearParalelo}
        isAdmin={isAdmin}
        setSelecterParallel={setSelectedBlockID}
        horarioOnOpen={horarioDisclosure.onOpen}
      />
      }
  }

  return (
    <>
      <Navbar isAdmin={isAdmin} />


      {rendering()}
      

      <HorarioTable
        horarioFiltrado={horarioFiltrado}
        isOpen={horarioDisclosure.isOpen}
        onClose={horarioDisclosure.onClose}
      />
    </>
  );
};

export default VistaCursos;
