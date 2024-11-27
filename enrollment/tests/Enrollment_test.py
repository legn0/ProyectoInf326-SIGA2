import unittest
import requests
#from app.crud.crud import EnrollmentCRUD
#from app.database.database import get_db

BASE_URL = "http://localhost:8002"

class TestCreateEnrollment(unittest.TestCase):
    def setUp(self) :
        if self._testMethodName == 'test_create_enrollment_duplicate':
            response = requests.post(
                f"{BASE_URL}/api/v1/courses/201/parallels/4/enrollments",
                json={"student_id": 1},
            )

            self.Course_Id = response.json()['course_id']
            self.Parallel_Id = response.json()['parallel_id']
            self.Enrollment_Id = response.json()['id']

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["is_active"], "Pendiente")
            
    
    def tearDown(self):
        if hasattr(self, "Course_Id") and hasattr(self, "Parallel_Id") and hasattr(self, "Enrollment_Id"):
            response = requests.delete(
                f"{BASE_URL}/api/v1/courses/{self.Course_Id}/parallels/{self.Parallel_Id}/enrollments/{self.Enrollment_Id}",
            )

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["message"], "Inscripción eliminada exitosamente")

    def test_create_enrollment_success(self):
        # Send the request
        response = requests.post(
            f"{BASE_URL}/api/v1/courses/201/parallels/4/enrollments",
            json={"student_id": 1},
        )

        TestCreateEnrollment.Course_Id = response.json()['course_id']
        TestCreateEnrollment.Parallel_Id = response.json()['parallel_id']
        TestCreateEnrollment.Enrollment_Id = response.json()['id']

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["is_active"], "Pendiente")
    
    def test_create_enrollment_duplicate(self):
        # Send the request
        response = requests.post(
            f"{BASE_URL}/api/v1/courses/{self.Course_Id}/parallels/{self.Parallel_Id}/enrollments",
            json={"student_id": 1},
        )

        # Assertions
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["detail"], "El estudiante ya está inscrito en este curso")