"""
Test configuration and fixtures for FastAPI backend tests.

This module provides pytest fixtures for testing the Mergington High School API,
including a TestClient fixture and fixtures for managing test data state.
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """
    Fixture that provides a TestClient for making requests to the FastAPI app.
    
    Returns:
        TestClient: A test client instance for the FastAPI application
    """
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """
    Fixture that resets the activities dictionary to its initial state before each test.
    
    This fixture runs automatically (autouse=True) before each test to ensure
    test isolation and prevent state leakage between tests.
    
    The fixture resets the activities dictionary after each test completes.
    """
    # Store the initial state
    initial_activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Join the school basketball team and compete in inter-school tournaments",
            "schedule": "Mondays and Wednesdays, 4:00 PM - 6:00 PM",
            "max_participants": 15,
            "participants": ["james@mergington.edu", "lucas@mergington.edu"]
        },
        "Swimming Club": {
            "description": "Improve swimming techniques and participate in swim meets",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 20,
            "participants": ["sarah@mergington.edu", "emily@mergington.edu"]
        },
        "Drama Club": {
            "description": "Perform in school plays and develop acting skills",
            "schedule": "Thursdays, 3:30 PM - 5:30 PM",
            "max_participants": 25,
            "participants": ["lily@mergington.edu", "ava@mergington.edu"]
        },
        "Art Class": {
            "description": "Explore painting, drawing, and sculpture techniques",
            "schedule": "Wednesdays, 3:00 PM - 5:00 PM",
            "max_participants": 18,
            "participants": ["mia@mergington.edu", "isabella@mergington.edu"]
        },
        "Debate Team": {
            "description": "Develop argumentation skills and compete in debate competitions",
            "schedule": "Tuesdays, 4:00 PM - 5:30 PM",
            "max_participants": 16,
            "participants": ["ethan@mergington.edu", "noah@mergington.edu"]
        },
        "Science Club": {
            "description": "Conduct experiments and participate in science fairs",
            "schedule": "Fridays, 3:00 PM - 4:30 PM",
            "max_participants": 15,
            "participants": ["william@mergington.edu", "alexander@mergington.edu"]
        }
    }
    
    # Reset before test runs (yield allows the test to execute)
    activities.clear()
    activities.update(initial_activities)
    
    yield
    
    # Reset after test completes (cleanup)
    activities.clear()
    activities.update(initial_activities)
