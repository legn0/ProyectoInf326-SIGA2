import axios from "axios";

apiUrlEnrollment = "http://174.138.124.76/enrollment/api/v1/courses/";

export function inscribirEstudiante({ course_id, parallel_id, estudiante }) {
  return axios
    .post(
      `${apiUrlEnrollment}${course_id}/parallels/${parallel_id}/enrollment/`,
      estudiante
    )
    .then((res) => res.data);
}

export function eliminarInscripcion({ course_id, parallel_id, enrollment_id }) {
  return axios.delete(
    `${apiUrlEnrollment}${course_id}/parallels/${parallel_id}/enrollment/${enrollment_id}`
  );
}

export function getInscripcion({ course_id, parallel_id, enrollment_id }) {
  return axios
    .get(
      `${apiUrlEnrollment}${course_id}/parallels/${parallel_id}/enrollment/${enrollment_id}`
    )
    .then((res) => res.data);
}

export function getAllInscripcionesFromParalelo({ course_id, parallel_id }) {
  return axios
    .get(`${apiUrlEnrollment}${course_id}/parallels/${parallel_id}/enrollment/`)
    .then((res) => res.data);
}
