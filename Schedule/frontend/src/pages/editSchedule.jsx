import React, { useState } from 'react';
import {
  Box,Button,Container,Heading,Input,Select,Table,Tbody,
  Td,Th,Thead,Tr,UnorderedList,ListItem,useToast,Flex,
} from '@chakra-ui/react';
import { useNavigate } from 'react-router-dom';
import './editSchedule.css';



export const EditSchedule = () => {
  const hours = ['1-2', '3-4', '5-6', '7-8', '9-10', '11-12', '13-14', '15-16', '17-18', '19-20'];
  const days = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'];
  const [courseId, setCourseId] = useState('');
  const [parallelId, setParallelId] = useState('');
  const [professorId, setProfessorId] = useState('');
  const [professorName, setProfessorName] = useState('');
  const [classType, setClassType] = useState('');
  const [selected, setSelected] = useState({});
  const [defaultOptionText] = useState('Seleccione una opción');
  const toast = useToast();
  const navigate = useNavigate();

  const handleBackClick = () => {
    navigate(-1);
  };


  const handleCourseIdChange = (event) => {
    setCourseId(event.target.value);
  };

  const handleParallelIdChange = (event) => {
    setParallelId(event.target.value);
  };

  const handleProfessorIdChange = (event) => {
    setProfessorId(event.target.value);
  };

  const handleProfessorNameChange = (event) => {
    setProfessorName(event.target.value);
  };

  const handleClassTypeChange = (event) => {
    setClassType(event.target.value);
  };

  const handleSelect = (day, hour, rowIndex, colIndex) => {
    setSelected((prevSelected) => ({
      ...prevSelected,
      [day]: {
        ...prevSelected[day],
        [hour]: prevSelected[day]?.[hour] ? null : { rowIndex, colIndex },
      },
    }));
  };

  const handleSubmit = async () => {
    const selectedItems = [];
    for (const day in selected) {
      for (const hour in selected[day]) {
        const selection = selected[day][hour];
        if (selection) {
          const id_bloque = selection.colIndex * 10 + selection.rowIndex + 1;
          selectedItems.push({
            id_bloque: parseInt(id_bloque, 10),
            nombre_bloque: hour,
            tipo: classType,
            id_profesor: parseInt(professorId, 10),
            nombre_profesor: professorName,
            dia: day,
          });
        }
      }
    }

    const data = selectedItems;
    console.log('Data to be sent:', data); // Log the data to verify its structure

    

    // try {
    //   const response = await fetch(
    //     `http://127.0.0.1:8000/api/v1/courses/${courseId}/parallels/${parallelId}/schedules`,
    //     {
    //       method: 'POST',
    //       headers: {
    //         'Content-Type': 'application/json',
    //       },
    //       body: JSON.stringify(data),
    //     }
    //   );

    //   if (response.ok) {
    //     console.log('Data submitted successfully');
    //     toast({
    //       title: 'Datos guardados exitosamente!',
    //       status: 'success',
    //       duration: 5000,
    //       isClosable: true,
    //     });
    //     window.location.reload(); // Refresh the page
    //   } else {
    //     console.error('Fallo al enviar datos:', response);
    //     toast({
    //       title: `Fallo al enviar datos: ${response.statusText}`,
    //       status: 'error',
    //       duration: 5000,
    //       isClosable: true,
    //     });
    //   }
    // } catch (error) {
    //   console.error('Error:', error);
    //   toast({
    //     title: `Error al conectarse con API: ${error.message}`,
    //     status: 'error',
    //     duration: 5000,
    //     isClosable: true,
    //   });
    // }
  };

  const selectedItems = [];
  for (const day in selected) {
    for (const hour in selected[day]) {
      const selection = selected[day][hour];
      if (selection) {
        const id_bloque = selection.colIndex * 10 + selection.rowIndex + 1;
        selectedItems.push({
          id_bloque: parseInt(id_bloque, 10),
          nombre_bloque: hour,
          tipo: classType,
          id_profesor: parseInt(professorId, 10),
          nombre_profesor: professorName,
          dia: day,
        });
      }
    }
  }

  return (
    <Container maxW="100%" backgroundColor={'white'} fontFamily={'Verdana'}>
      
      <Flex justifyContent="space-between" alignItems="center" mb={4}>
        <Heading as="h3" size="lg"  fontFamily={'Verdana'}>
          SIGA - Editar Horario
        </Heading>
        <Button onClick={handleBackClick} colorScheme="blue" width={150} mt={3}>
          Volver
        </Button>
      </Flex>




        <Flex >
            <Box mb={4}>
                <Heading as="h4" size="md" mb={2}>
                Curso:
                </Heading>
                <Input value={courseId} onChange={handleCourseIdChange} mb={2} backgroundColor={'#eee'} width={'220px'}/>
                <Heading as="h4" size="md" mb={2}>
                Paralelo:
                </Heading>
                <Input value={parallelId} onChange={handleParallelIdChange} mb={2} backgroundColor={'#eee'} width={'220px'}/>
                <Heading as="h4" size="md" mb={2}>
                Profesor ID:
                </Heading>
                <Input value={professorId} onChange={handleProfessorIdChange} mb={2} backgroundColor={'#eee'} width={'220px'}/>
                <Heading as="h4" size="md" mb={2}>
                Nombre del Profesor:
                </Heading>
                <Input value={professorName} onChange={handleProfessorNameChange} mb={2} backgroundColor={'#eee'} width={'220px'} />
                <Heading as="h4" size="md" mb={2}>
                Tipo de Clase:
                </Heading>

                <Select value={classType} onChange={handleClassTypeChange} mb={4} width={'220px'} fontSize={'15px'} backgroundColor={'#eee'}>
                <option value="" disabled>
                    {defaultOptionText}
                </option>
                <option value="Catedra">Catedra</option>
                <option value="Ayudantia">Ayudantia</option>
                </Select>

                <Button onClick={handleSubmit} colorScheme="green" mt={4} mb = {4} width={'100px'}>
                    Guardar
                </Button>
            </Box>

            <Box className="selected-items" mb={4} mr={15} ml={4}>
                <Heading as="h2" size="md" mb={2}>
                Horarios elegidos
                </Heading>
                <UnorderedList>
                {selectedItems.map((item) => (
                    <ListItem key={item.id_bloque}>
                    {item.dia} {item.nombre_bloque} ({item.hora})
                    </ListItem>
                ))}
                </UnorderedList>
            </Box>
            <Box>
                <Table variant="simple" className="schedule">
                <Thead>
                    <Tr>
                    <Th>Hora</Th>
                    {days.map((day) => (
                        <Th key={day}>{day}</Th>
                    ))}
                    </Tr>
                </Thead>
                <Tbody>
                    {hours.map((hour, rowIndex) => (
                    <Tr key={hour}>
                        <Td>{hour}</Td>
                        {days.map((day, colIndex) => (
                        <Td key={day}>
                            <Button className='button'
                            variant={selected[day]?.[hour] ? 'solid' : 'outline'}
                            colorScheme={selected[day]?.[hour] ? 'green' : 'gray'}
                            onClick={() => handleSelect(day, hour, rowIndex, colIndex)}
                            display="block">
                            {selected[day]?.[hour] ? '' : ''}
                            
                            </Button>
                        </Td>
                        ))}
                    </Tr>
                    ))}
                </Tbody>
                </Table>
            </Box>
        </Flex>
    </Container>
  );
};

export default EditSchedule;