import React,{ useState} from 'react'

export const EditSchedule = () => {
    const hours = ['1-2','3-4','5-6','7-8','9-10','11-12','13-14','15-16','17-18','19-20'];
    const days = ['Lunes','Martes','Miércoles','Jueves','Viernes','Sábado','Domingo'];
    const [courseId, setCourseId] = useState('');
    const [parallelId, setParallelId] = useState('');
    const [professorId, setProfessorId] = useState('');
    const [classType, setClassType] = useState('');
    const [selected, setSelected] = useState({});

    const handleCourseIdChange = (event) => {
        setCourseId(event.target.value);
      };

    const handleParallelIdChange = (event) => {
        setParallelId(event.target.value);
      };
    
    const handleProfessorIdChange = (event) => {
        setProfessorId(event.target.value);
        };

    const handleClassTypeChange = (event) => {
        setClassType(event.target.value);
    };
    
    const handleSelect = (day, hour) => {
        setSelected((prevSelected) => ({
            ...prevSelected,
            [day]: {
                ...prevSelected[day],
                [hour]: !prevSelected[day]?.[hour]
            }
        }));
    };
    const handleSubmit = async () => {
        const selectedItems = [];
        for (const day in selected) {
          for (const hour in selected[day]) {
            if (selected[day][hour]) {
              selectedItems.push({ day, hour });
            }
          }
        }
        const data = { 
          classType,
          professorId,
          schedule: selectedItems
        };
    
        try {
          const response = await fetch(`/api/v1/courses/${courseId}/parallels/${parallelId}/schedules`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
          });
    
          if (response.ok) {
            console.log('Data submitted successfully');
          } else {
            console.error('Failed to submit data');
          }
        } catch (error) {
          console.error('Error:', error);
        }
      };

    const selectedItems = [];
    for (const day in selected) {
        for (const hour in selected[day]) {
            if (selected[day][hour]) {
                selectedItems.push(`${day} ${hour}`);
            }
        }
    }
    

    return (
    <>
        <div className="app">
            <h1 className='Titulo'> SIGA  </h1>
            <h3 style={{textAlign:'left', margin: '10px'}}> Id Curso: 
            <input 
                type="text" 
                value={courseId} 
                onChange={handleCourseIdChange} 
                style={{margin: '10px'}}
            />
            </h3>
            <h3 style={{textAlign:'left', margin: '10px'}}> Id Paralelo: 
            <input 
                type="text" 
                value={parallelId} 
                onChange={handleParallelIdChange} 
                style={{margin: '10px'}}
            />
            </h3>
            <h3 style={{textAlign:'left', margin: '10px'}}> ID Profesor: 
            <input 
                type="text" 
                value={professorId} 
                onChange={handleProfessorIdChange} 
                style={{margin: '10px'}}
            />
            </h3>
            <h3 style={{textAlign:'left', margin: '10px'}}> Tipo de Clase: 
            <select style={{margin: '10px'}} value={classType} onChange={handleClassTypeChange}>
                <option value="Catedra">Catedra</option>
                <option value="Ayudantia">Ayudantia</option>
            </select></h3>
            <div className='container'>
                <div className="selected-items">
                    <h2>Horarios elegidos</h2>
                    <ul>
                        {selectedItems.map((item) => (           
                            <li key={item}>{item}</li>
                        ))}
                    </ul>
                </div>

                <table className="schedule">
                <thead>
                    <tr>
                        <th>Hora</th>
                        {days.map((day) => (<th key={day}>{day}</th> ))}
                    </tr>
                </thead>
                    <tbody>
                        {hours.map((hour) => (
                            <tr key={hour}>
                                <td>{hour}</td>
                                {days.map((day) => (
                                    <td key={day}>
                                        <button
                                            className={selected[day]?.[hour] ? 'selected' : ''}
                                            onClick={() => handleSelect(day, hour)}>
                                        </button>
                                    </td>
                                ))}
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
            <button onClick={handleSubmit} style={{margin: '10px'}}>Submit</button>
        </div>
    </>
  )
}

export default EditSchedule