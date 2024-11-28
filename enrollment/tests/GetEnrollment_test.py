import unittest
import requests

BASE_URL = "http://localhost:8002"

class TestGetEnrollment(unittest.TestCase):
    def setUp(self):
        response = requests.post(
            f"{BASE_URL}/api/v1/courses/246/parallels/6/enrollments",
            json={"student_id": 1},
        )

        self.assertEqual(response.status_code, 200)
        self.enrollment_data = response.json()

    def tearDown(self):
        if hasattr(self, "enrollment_data"):
            enrollment_id = self.enrollment_data["id"]
            course_id = self.enrollment_data["course_id"]
            parallel_id = self.enrollment_data["parallel_id"]
            response = requests.delete(
                f"{BASE_URL}/api/v1/courses/{course_id}/parallels/{parallel_id}/enrollments/{enrollment_id}"
            )
            self.assertEqual(response.status_code, 200)

    def test_get_enrollment_success(self):
        # Consultar la inscripción creada
        course_id = self.enrollment_data["course_id"]
        parallel_id = self.enrollment_data["parallel_id"]
        enrollment_id = self.enrollment_data["id"]

        response = requests.get(
            f"{BASE_URL}/api/v1/courses/{course_id}/parallels/{parallel_id}/enrollments/{enrollment_id}"
        )

        # Verificar respuesta exitosa
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["id"], enrollment_id)

    def test_get_enrollment_not_found(self):
        # Consultar una inscripción inexistente
        response = requests.get(
            f"{BASE_URL}/api/v1/courses/201/parallels/4/enrollments/9999"
        )

        # Verificar error 404
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Inscripción no encontrada")


class TestListEnrollments(unittest.TestCase):
    def setUp(self):
        # Crear una inscripción inicial para usar en los tests
        response = requests.post(
            f"{BASE_URL}/api/v1/courses/246/parallels/6/enrollments",
            json={"student_id": 1},
        )
        self.assertEqual(response.status_code, 200)
        self.enrollment_data = response.json()

    def tearDown(self):
        # Eliminar la inscripción creada para limpiar los datos
        if hasattr(self, "enrollment_data"):
            enrollment_id = self.enrollment_data["id"]
            course_id = self.enrollment_data["course_id"]
            parallel_id = self.enrollment_data["parallel_id"]
            response = requests.delete(
                f"{BASE_URL}/api/v1/courses/{course_id}/parallels/{parallel_id}/enrollments/{enrollment_id}"
            )
            self.assertEqual(response.status_code, 200)

    def test_list_enrollments_success(self):
        # Consultar todas las inscripciones para el curso y paralelo
        course_id = self.enrollment_data["course_id"]
        parallel_id = self.enrollment_data["parallel_id"]

        response = requests.get(
            f"{BASE_URL}/api/v1/courses/{course_id}/parallels/{parallel_id}/enrollments"
        )

        # Verificar respuesta exitosa
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
        self.assertGreaterEqual(len(response.json()), 1)

    def test_list_enrollments_empty(self):
        # Consultar un paralelo sin inscripciones (usar un ID diferente)
        response = requests.get(
            f"{BASE_URL}/api/v1/courses/277/parallels/5/enrollments"
        )

        # Verificar que no hay inscripciones
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 0)