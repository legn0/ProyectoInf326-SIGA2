import unittest
from unittest.mock import MagicMock
import requests
from ..app.api.routes import TestClient
from ..app.crud.crud import EnrollmentCRUD

# Assuming your FastAPI app is called "app"
#from app import app

class TestCreateEnrollment(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.db = MagicMock()

    def test_create_enrollment_success(self):
        # Mock the data
        enrollment_data = {
            "student_id": 1,
        }
        # Mock CRUD methods
        EnrollmentCRUD.get_enrollment_by_student_and_course = MagicMock(return_value=None)  # No existing enrollment
        EnrollmentCRUD.create_enrollment = MagicMock(return_value=enrollment_data)

        # Send the request
        response = requests.post(
            "http://174.138.124.76/enrollment/api/v1/courses/101/parallels/5/enrollments",
            json={"student_id": 1},
        )

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["is_active"], "Pendiente")
        #EnrollmentCRUD.get_enrollment_by_student_and_course.assert_called_once_with(1, 101, 5)
        #EnrollmentCRUD.create_enrollment.assert_called_once()
    
    def test_create_enrollment_duplicate(self):
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
        #EnrollmentCRUD.create_enrollment.assert_not_called()