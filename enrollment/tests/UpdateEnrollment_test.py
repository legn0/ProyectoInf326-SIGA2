import unittest
import requests
#from app.crud.crud import EnrollmentCRUD
#from app.database.database import get_db

#{'id': 54, 'student_id': 1, 'course_id': 203, 'parallel_id': 4, 'created_at': '2024-11-28T00:05:20', 'is_active': 'Pendiente'}
BASE_URL = "http://localhost:8002"

class TestUpdateEnrollment(unittest.TestCase):
    def setUp(self) :
        if self._testMethodName == 'test_Update_enrollment_success':
            response = requests.post(
                f"{BASE_URL}/api/v1/courses/281/parallels/4/enrollments",
                json={"student_id": 4},
            )

            self.Enrollment = response.json()

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["is_active"], "Pendiente")
            
    
    def tearDown(self):
        if hasattr(self, "Enrollment"):
            response = requests.delete(
                f"{BASE_URL}/api/v1/courses/{self.Enrollment['course_id']}/parallels/{self.Enrollment['parallel_id']}/enrollments/{self.Enrollment['id']}",
            )

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["message"], "Inscripción eliminada exitosamente")

    def test_Update_enrollment_success(self):
        # Send the request
        self.Enrollment['is_active'] = "Inscrita"
        response = requests.put(
            f"{BASE_URL}/api/v1/courses/{self.Enrollment['course_id']}/parallels/{self.Enrollment['parallel_id']}/enrollments/{self.Enrollment['id']}",
            json=self.Enrollment,
        )

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["is_active"], "Inscrita")
    
    def test_Update_enrollment_no_exist(self):
        # Send the request
        response = requests.put(
            f"{BASE_URL}/api/v1/courses/281/parallels/4/enrollments/enrollments/0",
            json={"student_id": 4},
        )

        # Assertions
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Not Found")