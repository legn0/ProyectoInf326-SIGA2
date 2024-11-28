import unittest
import requests

BASE_URL = "http://localhost:8002"  # Cambia esto si tu servidor corre en otro puerto

class TestDeleteEnrollment(unittest.TestCase):
    def setUp(self):
        # Crear una inscripción para usar en los tests
        self.course_id = 240
        self.parallel_id = 2
        response = requests.post(
            f"{BASE_URL}/api/v1/courses/{self.course_id}/parallels/{self.parallel_id}/enrollments",
            json={"student_id": 1},
        )
        if response.status_code == 200:
            enrollment = response.json()
            self.enrollment_id = enrollment["id"]
        else:
            self.enrollment_id = None

    def test_delete_enrollment_success(self):
        """Verifica que se pueda eliminar una inscripción existente"""
        response = requests.delete(
            f"{BASE_URL}/api/v1/courses/{self.course_id}/parallels/{self.parallel_id}/enrollments/{self.enrollment_id}"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Inscripción eliminada exitosamente")

        # Verificar que la inscripción ya no existe
        follow_up_response = requests.get(
            f"{BASE_URL}/api/v1/courses/{self.course_id}/parallels/{self.parallel_id}/enrollments/{self.enrollment_id}"
        )
        self.assertEqual(follow_up_response.status_code, 404)

    def test_delete_enrollment_not_found(self):
        """Verifica que intentar eliminar una inscripción inexistente devuelve 404"""
        fake_enrollment_id = 99999  # ID que no existe
        response = requests.delete(
            f"{BASE_URL}/api/v1/courses/{self.course_id}/parallels/{self.parallel_id}/enrollments/{fake_enrollment_id}"
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Inscripción no encontrada")

    def tearDown(self):
        # Limpieza: Eliminar la inscripción creada, si aún existe
        if self.enrollment_id:
            requests.delete(
                f"{BASE_URL}/api/v1/courses/{self.course_id}/parallels/{self.parallel_id}/enrollments/{self.enrollment_id}"
            )

if __name__ == "__main__":
    unittest.main()