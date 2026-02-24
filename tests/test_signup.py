"""
Tests for POST /activities/{activity_name}/signup endpoint.

Tests verify the signup functionality including success cases, error handling,
and edge cases following the AAA (Arrange-Act-Assert) pattern.
"""


def test_signup_success(client):
    """
    Test successful signup of a new participant to an activity.
    
    Following AAA pattern:
    - Arrange: Set up test data with a new email
    - Act: POST to signup endpoint
    - Assert: Verify success response and participant is added
    """
    # Arrange
    activity_name = "Chess Club"
    new_email = "newstudent@mergington.edu"
    
    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={new_email}")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert new_email in data["message"]
    assert activity_name in data["message"]
    
    # Verify the participant was actually added
    activities_response = client.get("/activities")
    activities_data = activities_response.json()
    assert new_email in activities_data[activity_name]["participants"]


def test_signup_nonexistent_activity(client):
    """
    Test signup to a non-existent activity returns 404 error.
    
    Following AAA pattern:
    - Arrange: Set up invalid activity name
    - Act: POST to signup endpoint with invalid activity
    - Assert: Verify 404 error is returned
    """
    # Arrange
    invalid_activity = "Nonexistent Club"
    email = "student@mergington.edu"
    
    # Act
    response = client.post(f"/activities/{invalid_activity}/signup?email={email}")
    
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower()


def test_signup_duplicate_email(client):
    """
    Test that signing up the same email twice returns 400 error.
    
    Following AAA pattern:
    - Arrange: Set up activity and existing participant email
    - Act: Attempt to signup with duplicate email
    - Assert: Verify 400 error is returned
    """
    # Arrange
    activity_name = "Chess Club"
    existing_email = "michael@mergington.edu"  # Already in Chess Club
    
    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={existing_email}")
    
    # Assert
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "already signed up" in data["detail"].lower()


def test_signup_increases_participant_count(client):
    """
    Test that signup increases the participant count by 1.
    
    Following AAA pattern:
    - Arrange: Get initial participant count
    - Act: Add a new participant
    - Assert: Verify count increased by 1
    """
    # Arrange
    activity_name = "Programming Class"
    new_email = "extra@mergington.edu"
    
    # Get initial state
    initial_response = client.get("/activities")
    initial_data = initial_response.json()
    initial_count = len(initial_data[activity_name]["participants"])
    
    # Act
    signup_response = client.post(f"/activities/{activity_name}/signup?email={new_email}")
    
    # Assert
    assert signup_response.status_code == 200
    
    # Verify participant count increased
    final_response = client.get("/activities")
    final_data = final_response.json()
    final_count = len(final_data[activity_name]["participants"])
    
    assert final_count == initial_count + 1
    assert new_email in final_data[activity_name]["participants"]


def test_signup_multiple_students_to_different_activities(client):
    """
    Test that multiple students can sign up for different activities.
    
    Following AAA pattern:
    - Arrange: Set up multiple students and activities
    - Act: Sign up students to different activities
    - Assert: Verify all signups succeeded independently
    """
    # Arrange
    signups = [
        ("Chess Club", "chess1@mergington.edu"),
        ("Programming Class", "programmer1@mergington.edu"),
        ("Gym Class", "athlete1@mergington.edu")
    ]
    
    # Act & Assert
    for activity_name, email in signups:
        response = client.post(f"/activities/{activity_name}/signup?email={email}")
        
        # Assert each signup is successful
        assert response.status_code == 200
        
        # Verify participant was added
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        assert email in activities_data[activity_name]["participants"]


def test_signup_same_email_to_different_activities(client):
    """
    Test that the same email can sign up for multiple different activities.
    
    Following AAA pattern:
    - Arrange: Set up one email and multiple activities
    - Act: Sign up same email to different activities
    - Assert: Verify signup succeeds for all activities
    """
    # Arrange
    email = "multitasker@mergington.edu"
    activities_to_join = ["Chess Club", "Programming Class", "Art Class"]
    
    # Act & Assert
    for activity_name in activities_to_join:
        response = client.post(f"/activities/{activity_name}/signup?email={email}")
        
        # Assert each signup is successful
        assert response.status_code == 200
        
        # Verify participant was added to this activity
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        assert email in activities_data[activity_name]["participants"]


def test_signup_with_special_characters_in_email(client):
    """
    Test signup with email containing special characters.
    
    Following AAA pattern:
    - Arrange: Set up email with special characters
    - Act: POST to signup endpoint
    - Assert: Verify signup succeeds
    """
    # Arrange
    activity_name = "Science Club"
    special_email = "john.doe+test@mergington.edu"
    
    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={special_email}")
    
    # Assert
    assert response.status_code == 200
    
    # Verify participant was added
    activities_response = client.get("/activities")
    activities_data = activities_response.json()
    assert special_email in activities_data[activity_name]["participants"]
