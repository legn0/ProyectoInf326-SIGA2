import React,{ useState} from 'react'
import './editSchedule.css'

export const EditSchedule = () => {
    const hours = ['1-2','3-4','5-6','7-8','9-10','11-12','13-14','15-16','17-18','19-20'];
    const days = ['Lunes','Martes','Miércoles','Jueves','Viernes','Sábado','Domingo'];
    const [courseId, setCourseId] = useState('');
    const [parallelId, setParallelId] = useState('');
    const [professorId, setProfessorId] = useState('');
    const [professorName, setProfessorName] = useState('');
    const [classType, setClassType] = useState('');
    const [selected, setSelected] = useState({});
    const [defaultOptionText] = useState('Seleccione una opción');

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
        setSelected(prevSelected => ({
            ...prevSelected,
            [day]: {
                ...prevSelected[day],
                [hour]: prevSelected[day]?.[hour] ? null : { rowIndex, colIndex }
            }
        }));
    };
    const handleSubmit = async () => {
        const selectedItems = [];
        for (const day in selected) {
          for (const hour in selected[day]) {
            const selection = selected[day][hour];
            if (selected[day][hour]) {
                const id_bloque = selection.colIndex * 10 + selection.rowIndex +1;
                selectedItems.push({
                    id_bloque: parseInt(id_bloque, 10),
                    nombre_bloque: hour, // Assuming courseName is the block name
                    tipo: classType,
                    id_profesor: parseInt(professorId,10),
                    nombre_profesor: professorName, // Replace with actual professor name if available
                    dia: day
                });
            }
          }
        }
        const data = selectedItems;
        console.log('Data to be sent:', data); // Log the data to verify its structure
    
        try {
          const response = await fetch(`http://127.0.0.1:8000/api/v1/courses/${parseInt(courseId,10)}/parallels/${parseInt(parallelId,10)}/schedules`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
          });
    
          if (response.ok) {
            console.log('Data submitted successfully');
            alert('Datos guardados exitosamente!'); // Show success message
            window.location.reload(); // Refresh the page
          } else {
            console.error('Fallo al enviar datos:', response);
            alert(`Fallo al enviar datos: ${response}`); // Show error message
          }
        } catch (error) {
            console.error('Error:', error);
            alert(`Error al conectarse con API: ${error.message}`); // Show error message
            window.location.reload(); // Refresh the page


        }
      };

      const selectedItems = [];
      for (const day in selected) {
          for (const hour in selected[day]) {
              const selection = selected[day][hour];
              if (selection) {
                  selectedItems.push(`${day} ${hour} Id Bloque: ${selection.colIndex * 10 + selection.rowIndex +1}`);
              }
          }
      }
    

    return (
    <>
        <div className="app">
            <h1 className='Titulo'> SIGA NUEVO  😎</h1>
            <div className='container'>

                {/* Formulario de datos */}
                <div>
                    <h4 style={{textAlign:'left', margin: '10px 0px 10px 5px'}}> Id Curso: 
                    <input 
                        type="text" 
                        value={courseId} 
                        onChange={handleCourseIdChange} 
                        style={{margin: '10px', width: '100px'}}
                    />
                    </h4>
                    <h4> Id Paralelo: 
                    <input 
                        type="text" 
                        value={parallelId} 
                        onChange={handleParallelIdChange} 
                        style={{margin: '10px', width: '100px'}}
                    />
                    </h4>
                    <h4 style={{textAlign:'left', margin: '10px 0px 10px 5px'}}> Nombre Profesor: 
                    <input 
                        type="text" 
                        value={professorName} 
                        onChange={handleProfessorNameChange} 
                        style={{margin: '10px', width: '100px'}}
                    />
                    </h4>
                    <h4 style={{textAlign:'left', margin: '10px 0px 10px 5px'}}> ID Profesor: 
                    <input 
                        type="text" 
                        value={professorId} 
                        onChange={handleProfessorIdChange} 
                        style={{margin: '10px', width: '100px'}}
                    />
                    </h4>
                    <h4 style={{textAlign:'left', margin: '10px 0px 10px 5px'}}> Tipo de Clase: 
                    <select style={{ margin: '10px', maxHeight: '100px', overflowY: 'auto' }} value={classType} onChange={handleClassTypeChange}>
                        <option value="" disabled>{defaultOptionText}</option>
                        <option value="Catedra">Catedra</option>
                        <option value="Ayudantia">Ayudantia</option>
                    </select></h4>
                </div>

                {/* Horarios elegidos */}
                <div className="selected-items">
                    <h2>Horarios elegidos</h2>
                    <ul>
                        {selectedItems.map((item) => (           
                            <li key={item}>{item}</li>
                        ))}
                    </ul>
                </div>
                
                {/* Tabla de horarios */}
                <table className="schedule">
                <thead>
                    <tr>
                        <th>Hora</th>
                        {days.map((day, dayIndex) => (<th key={day}>{day}</th> ))}
                    </tr>
                </thead>
                    <tbody>
                        {hours.map((hour, rowIndex) => (
                            <tr key={hour}>
                                <td>{hour}</td>
                                {days.map((day, colIndex) => (
                                    <td key={day}>
                                        <button
                                            className={selected[day]?.[hour] ? 'selected' : ''}
                                            onClick={() => handleSelect(day, hour, rowIndex, colIndex)}>
                                        </button>
                                    </td>
                                ))}
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
            {/* Boton de guardar */}
            <button onClick={handleSubmit} className='button_submit'>Guardar</button>
        </div>
    </>
  )
}

export default EditSchedule