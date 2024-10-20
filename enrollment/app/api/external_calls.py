import httpx
import logging

class ExternalCourseAPI:
    @staticmethod
    def get_parallel_data(course_id: int, parallel_id: int):
        try:
            response = httpx.get(f"http://localhost:8000/api/v1/courses/{course_id}/parallels/{parallel_id}")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as exc:
            logging.error(f"Error al consultar los datos del paralelo: {exc}")
            raise Exception("Error al consultar los datos del paralelo")