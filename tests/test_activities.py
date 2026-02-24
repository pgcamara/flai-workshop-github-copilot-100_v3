"""
Tests for GET /activities endpoint.

Tests verify that the activities endpoint returns all available activities
with the correct structure and data following the AAA (Arrange-Act-Assert) pattern.
"""


def test_get_activities_returns_all_activities(client):
    """
    Test that GET /activities returns all 9 activities with correct structure.
    
    Following AAA pattern:
    - Arrange: Client fixture provides TestClient
    - Act: Make GET request to /activities endpoint
    - Assert: Verify response structure and content
    """
    # Arrange
    # (client fixture provides the TestClient)
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) == 9  # Should have all 9 activities
    
    # Verify specific activities exist
    expected_activities = [
        "Chess Club",
        "Programming Class",
        "Gym Class",
        "Basketball Team",
        "Swimming Club",
        "Drama Club",
        "Art Class",
        "Debate Team",
        "Science Club"
    ]
    for activity_name in expected_activities:
        assert activity_name in data


def test_get_activities_returns_correct_structure(client):
    """
    Test that each activity has the required fields with correct types.
    
    Following AAA pattern:
    - Arrange: Client fixture provides TestClient
    - Act: Make GET request to /activities endpoint
    - Assert: Verify each activity has required fields
    """
    # Arrange
    # (client fixture provides the TestClient)
    
    # Act
    response = client.get("/activities")
    
    # Assert
    data = response.json()
    
    # Check that each activity has the required structure
    for activity_name, activity_data in data.items():
        assert "description" in activity_data
        assert "schedule" in activity_data
        assert "max_participants" in activity_data
        assert "participants" in activity_data
        
        # Verify types
        assert isinstance(activity_data["description"], str)
        assert isinstance(activity_data["schedule"], str)
        assert isinstance(activity_data["max_participants"], int)
        assert isinstance(activity_data["participants"], list)
        
        # Verify participants are strings (emails)
        for participant in activity_data["participants"]:
            assert isinstance(participant, str)


def test_get_activities_returns_initial_participants(client):
    """
    Test that activities include the initial participant data.
    
    Following AAA pattern:
    - Arrange: Client fixture provides TestClient
    - Act: Make GET request to /activities endpoint
    - Assert: Verify each activity has 2 initial participants
    """
    # Arrange
    # (client fixture provides the TestClient)
    
    # Act
    response = client.get("/activities")
    
    # Assert
    data = response.json()
    
    # Each activity should start with 2 participants
    for activity_name, activity_data in data.items():
        assert len(activity_data["participants"]) == 2
        
    # Verify specific participants for Chess Club
    assert "michael@mergington.edu" in data["Chess Club"]["participants"]
    assert "daniel@mergington.edu" in data["Chess Club"]["participants"]


def test_get_activities_has_valid_max_participants(client):
    """
    Test that max_participants values are within expected range.
    
    Following AAA pattern:
    - Arrange: Client fixture provides TestClient
    - Act: Make GET request to /activities endpoint
    - Assert: Verify max_participants values are reasonable
    """
    # Arrange
    # (client fixture provides the TestClient)
    
    # Act
    response = client.get("/activities")
    
    # Assert
    data = response.json()
    
    # Verify max_participants are positive integers
    for activity_name, activity_data in data.items():
        max_participants = activity_data["max_participants"]
        assert max_participants > 0
        assert max_participants >= 10  # Reasonable minimum
        assert max_participants <= 50  # Reasonable maximum
