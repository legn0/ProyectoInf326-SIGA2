import {
  Accordion,
  Table,
  Thead,
  Tr,
  Th,
  Tbody,
  TableContainer,
  Button,
  useDisclosure,
} from "@chakra-ui/react";
import AcordionCursosItem from "./AcordionCursosItem";
import PopUpFormCurso from "../Components/PopUpFormCurso";

function AcorcionCursos({ cursos, paralelos, crearCurso, crearParalelo, isAdmin }) {
  const disclosureFormCurso = useDisclosure(false);

  return (
    <>
      <Accordion allowMultiple defaultIndex={[0]}>
        <TableContainer>
          <Table>
            <Thead>
              <Tr>
                <Th>Sigla</Th>
                <Th>Nombre</Th>
                <Th>Departamento</Th>
                <Th>Prerequisitos</Th>
                {isAdmin ? <Th>
                  <Button onClick={disclosureFormCurso.onOpen}>
                    Crear Curso
                  </Button>
                </Th> : ""}
              </Tr>
            </Thead>
            <Tbody>
              {cursos.map((curso, index) => (
                <AcordionCursosItem
                  index={index}
                  value={curso.sigla}
                  curso={curso}
                  paralelos={paralelos.filter(
                    (paralelo) => paralelo.curso === curso.sigla
                  )}
                  crearParalelo={crearParalelo}
                  isAdmin={isAdmin}
                />
              ))}
            </Tbody>
          </Table>
        </TableContainer>
      </Accordion>
      {isAdmin ? <PopUpFormCurso
        isOpen={disclosureFormCurso.isOpen}
        onClose={disclosureFormCurso.onClose}
        crearCurso={crearCurso}
      /> : ""}
    </>
  );
}

export default AcorcionCursos;
