import pytest
from fastapi.testclient import TestClient
from courses_api import app

client = TestClient(app)

# Task 1 — Test Course Creation (Positive Case)
def test_create_course_success():
    new_course = {
        "id": 2,
        "title": "Machine Learning",
        "duration": 40,
        "fee": 5000,
        "is_active": True
    }
    response = client.post("/courses", json=new_course)
    assert response.status_code == 201
    assert response.json()["title"] == "Machine Learning"
    assert response.json()["fee"] == 5000
    # ensure it was added
    all_courses = client.get("/courses").json()
    assert any(course["id"] == 2 for course in all_courses)

# Task 2 — Duplicate Course ID Handling
@pytest.mark.parametrize("duplicate_id", [1, 2])
def test_duplicate_course_id(duplicate_id):
    duplicate_course = {
        "id": duplicate_id,
        "title": "Duplicate Course",
        "duration": 25,
        "fee": 2500,
        "is_active": True
    }
    response = client.post("/courses", json=duplicate_course)
    assert response.status_code == 400
    assert response.json()["detail"] == "Course ID already exists"

# Task 3 — Validation Error Testing
def test_validation_error():
    invalid_course = {
        "id": 3,
        "title": "AI",
        "duration": 0,
        "fee": -500,
        "is_active": True
    }
    response = client.post("/courses", json=invalid_course)
    assert response.status_code == 422
    # the response text should contain validation error codes
    data = response.json()
    error_types = [err["type"] for err in data["detail"]]

    # Updated checks for Pydantic v2
    assert "greater_than" in error_types
    assert any("duration" in err["loc"] for err in data["detail"])
    assert any("fee" in err["loc"] for err in data["detail"])

# Task 4 — Test GET Returns Correct Format
def test_get_courses_format():
    response = client.get("/courses")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert all(isinstance(course, dict) for course in data)
    required_keys = {"id", "title", "duration", "fee", "is_active"}
    for course in data:
        assert required_keys.issubset(course.keys())
