import axios from "axios";


const legacy = true;

const apiUrlCourses =  `http://${!legacy ? "174.138.124.76" : "174.138.110.82"}/courses/api/v1/courses/` ;

// CURSOS
export function createCurso({
  name,
  sigla,
  creditos,
  departamento,
  prerequisitos,
}) {
  return axios
    .post(apiUrlCourses, {
      name: name,
      sigla: sigla,
      creditos: creditos,
      departamento: departamento,
      prerequisites: prerequisitos,
    })
    .then((res) => res.data);
}

export function eliminarCurso({ course_id }) {
  return axios.delete(`${apiUrlCourses}${course_id}`);
}

export function getCurso({ course_id }) {
  return axios.delete(`${apiUrlCourses}${course_id}`);
}
export function getAllCursos() {
  return axios
    .get(`${apiUrlCourses}`, {
      params: { _sort: "sigla" },
    })
    .then((res) => res.data);
}

//PARALELOS

export function createParallel({
  course_id,
  number,
  limite_cupo,
  jornada,
  campus,
}) {
  return axios.post(`${apiUrlCourses}${course_id}/parallels/`, {
    number: number,
    limite_cupo: limite_cupo,
    jornada: jornada,
    Campus: campus,
  });
}

export function deleteParallel({ course_id, parallel_id }) {
  return axios.delete(`${apiUrlCourses}${course_id}/parallels/${parallel_id}`);
}

export function getParallel({ course_id, parallel_id }) {
  return axios
    .get(`${apiUrlCourses}${course_id}/parallels/${parallel_id}`)
    .then((res) => res.data);
}

export function getAllParallelsFromCourse({ course_id }) {
  return axios
    .get(`${apiUrlCourses}${course_id}/parallels/`, {
      params: { _sort: "sigla" },
    })
    .then((res) => res.data);
}
