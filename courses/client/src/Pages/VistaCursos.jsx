import React from "react";
import { Box, useDisclosure, Button } from "@chakra-ui/react";
import PopUpConsulta from "../Components/PopUpConsulta";
import PopUpFormParalelo from "../Components/PopUpFormParalelo";
import PopUpFormCurso from "../Components/PopUpFormCurso";

export const VistaCursos = () => {
  const paralelo1 = {
    curso: "inf285",
    paralelo: 200,
    limite_cupo: 60,
    jornada: "Diurna",
    campus_sede: "San Joaquin",
  };

  const disclosureCosulta = useDisclosure(false);
  const disclosureFormParalelo = useDisclosure(false);
  const disclosureFormCurso = useDisclosure(false);

  return (
    <>
      <Box> Ola soy un placeholder del nav bar</Box>

      <Button onClick={disclosureCosulta.onOpen}>
        ola borrar Ver Paralelo
      </Button>
      <Button onClick={disclosureFormParalelo.onOpen}>
        ola borrar Crear Paralelo
      </Button>
      <Button onClick={disclosureFormCurso.onOpen}>
        ola borrar Crear Curso
      </Button>

      <PopUpConsulta
        dataParalelo={paralelo1}
        isOpen={disclosureCosulta.isOpen}
        onClose={disclosureCosulta.onClose}
      />
      <PopUpFormParalelo
        dataCurso={paralelo1}
        isOpen={disclosureFormParalelo.isOpen}
        onClose={disclosureFormParalelo.onClose}
      />
      <PopUpFormCurso
        isOpen={disclosureFormCurso.isOpen}
        onClose={disclosureFormCurso.onClose}
      />
    </>
  );
};

export default VistaCursos;
