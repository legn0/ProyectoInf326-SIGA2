import unittest
from unittest.mock import MagicMock
import requests
#from ..app.api.routes import TestClient
#from ..app.crud.crud import EnrollmentCRUD

# Assuming your FastAPI app is called "app"
#from app import app

BASE_URL = "http://localhost:8002"

class TestCreateEnrollment(unittest.TestCase):
    def tearDown(self):
        if hasattr(self, "Course_Id") and hasattr(self, "Parallel_Id") and hasattr(self, "Enrollment_Id"):
            response = requests.delete(
                f"{BASE_URL}/api/v1/courses/{self.Course_Id}/parallels/{self.Parallel_Id}/enrollments/{self.Enrollment_Id}",
            )
            
            print(response.json())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["message"], "Inscripción eliminada exitosamente")

    def test_create_enrollment_success(self):
        # Send the request
        response = requests.post(
            f"{BASE_URL}/api/v1/courses/201/parallels/4/enrollments",
            json={"student_id": 1},
        )

        print(response.json())
        TestCreateEnrollment.Course_Id = response.json()['course_id']
        TestCreateEnrollment.Parallel_Id = response.json()['parallel_id']
        TestCreateEnrollment.Enrollment_Id = response.json()['id']

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["is_active"], "Pendiente")
    
    """def test_create_enrollment_duplicate(self):
        # Mock the data
        existing_enrollment = {
            "student_id": 1,
            "course_id": 101,
            "parallel_id": 5,
            "is_active": "Inscrita"
        }
        #EnrollmentCRUD.get_enrollment_by_student_and_course = MagicMock(return_value=existing_enrollment)

        # Send the request
        response = self.client.post(
            "http://174.138.124.76/enrollment/api/v1/courses/101/parallels/5/enrollments",
            json={"student_id": 1},
        )

        # Assertions
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["detail"], "El estudiante ya está inscrito en este curso caca")
        #EnrollmentCRUD.get_enrollment_by_student_and_course.assert_called_once_with(1, 101, 5)
        #EnrollmentCRUD.create_enrollment.assert_not_called()"""