import axios from "axios";

const apiUrlSchedule = "http://174.138.124.76/schedule/api/v1/courses/";

export function createSchedule({ course_id, parallel_id, horario }) {
  return axios
    .post(
      `${apiUrlSchedule}${course_id}/parallels/${parallel_id}/schedules/`,
      horario
    )
    .then((res) => res.data);
}

export function eliminarSchedule({ course_id, parallel_id, schedule_id }) {
  return axios.delete(
    `${apiUrlSchedule}${course_id}/parallels/${parallel_id}/schedules/${schedule_id}`
  );
}

export function getSchedule({ course_id, parallel_id, schedule_id }) {
  return axios
    .get(
      `${apiUrlSchedule}${course_id}/parallels/${parallel_id}/schedules/${schedule_id}`
    )
    .then((res) => res.data);
}

export function getAllSchedulesFromParalelo({ course_id, parallel_id }) {
  return axios
    .get(`${apiUrlSchedule}${course_id}/parallels/${parallel_id}/schedules/`, {
      params: { _sort: "bloque_id" },
    })
    .then((res) => res.data);
}
