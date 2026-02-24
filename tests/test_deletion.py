"""
Tests for DELETE /activities/{activity_name}/participants/{email} endpoint.

Tests verify the participant removal functionality including success cases,
error handling, and edge cases following the AAA (Arrange-Act-Assert) pattern.
"""


def test_delete_participant_success(client):
    """
    Test successful removal of an existing participant from an activity.
    
    Following AAA pattern:
    - Arrange: Set up activity with existing participant
    - Act: DELETE participant from activity
    - Assert: Verify success response and participant is removed
    """
    # Arrange
    activity_name = "Chess Club"
    existing_email = "michael@mergington.edu"  # Pre-existing participant
    
    # Verify participant exists before deletion
    initial_response = client.get("/activities")
    initial_data = initial_response.json()
    assert existing_email in initial_data[activity_name]["participants"]
    
    # Act
    response = client.delete(f"/activities/{activity_name}/participants/{existing_email}")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert existing_email in data["message"]
    assert activity_name in data["message"]
    
    # Verify the participant was actually removed
    final_response = client.get("/activities")
    final_data = final_response.json()
    assert existing_email not in final_data[activity_name]["participants"]


def test_delete_participant_nonexistent_activity(client):
    """
    Test deletion from a non-existent activity returns 404 error.
    
    Following AAA pattern:
    - Arrange: Set up invalid activity name
    - Act: DELETE request with invalid activity
    - Assert: Verify 404 error is returned
    """
    # Arrange
    invalid_activity = "Nonexistent Club"
    email = "student@mergington.edu"
    
    # Act
    response = client.delete(f"/activities/{invalid_activity}/participants/{email}")
    
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower()


def test_delete_nonexistent_participant(client):
    """
    Test deletion of a non-existent participant returns 404 error.
    
    Following AAA pattern:
    - Arrange: Set up valid activity but non-existent participant email
    - Act: DELETE request with non-existent participant
    - Assert: Verify 404 error is returned
    """
    # Arrange
    activity_name = "Chess Club"
    nonexistent_email = "notaparticipant@mergington.edu"
    
    # Verify participant doesn't exist
    initial_response = client.get("/activities")
    initial_data = initial_response.json()
    assert nonexistent_email not in initial_data[activity_name]["participants"]
    
    # Act
    response = client.delete(f"/activities/{activity_name}/participants/{nonexistent_email}")
    
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower()


def test_delete_decreases_participant_count(client):
    """
    Test that deletion decreases the participant count by 1.
    
    Following AAA pattern:
    - Arrange: Get initial participant count
    - Act: Delete an existing participant
    - Assert: Verify count decreased by 1
    """
    # Arrange
    activity_name = "Programming Class"
    existing_email = "emma@mergington.edu"
    
    # Get initial state
    initial_response = client.get("/activities")
    initial_data = initial_response.json()
    initial_count = len(initial_data[activity_name]["participants"])
    assert existing_email in initial_data[activity_name]["participants"]
    
    # Act
    delete_response = client.delete(f"/activities/{activity_name}/participants/{existing_email}")
    
    # Assert
    assert delete_response.status_code == 200
    
    # Verify participant count decreased
    final_response = client.get("/activities")
    final_data = final_response.json()
    final_count = len(final_data[activity_name]["participants"])
    
    assert final_count == initial_count - 1
    assert existing_email not in final_data[activity_name]["participants"]


def test_delete_then_signup_same_email(client):
    """
    Test that a deleted participant can sign up again.
    
    Following AAA pattern:
    - Arrange: Set up activity with existing participant
    - Act: Delete participant, then sign up again
    - Assert: Verify both operations succeed
    """
    # Arrange
    activity_name = "Gym Class"
    email = "john@mergington.edu"
    
    # Verify initial state
    initial_response = client.get("/activities")
    initial_data = initial_response.json()
    assert email in initial_data[activity_name]["participants"]
    
    # Act - Delete
    delete_response = client.delete(f"/activities/{activity_name}/participants/{email}")
    assert delete_response.status_code == 200
    
    # Verify deletion
    after_delete_response = client.get("/activities")
    after_delete_data = after_delete_response.json()
    assert email not in after_delete_data[activity_name]["participants"]
    
    # Act - Sign up again
    signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    
    # Assert
    assert signup_response.status_code == 200
    
    # Verify participant is back
    final_response = client.get("/activities")
    final_data = final_response.json()
    assert email in final_data[activity_name]["participants"]


def test_delete_all_participants_from_activity(client):
    """
    Test that all participants can be removed from an activity.
    
    Following AAA pattern:
    - Arrange: Set up activity with known participants
    - Act: Delete all participants one by one
    - Assert: Verify activity has no participants
    """
    # Arrange
    activity_name = "Basketball Team"
    
    # Get initial participants
    initial_response = client.get("/activities")
    initial_data = initial_response.json()
    participants = initial_data[activity_name]["participants"].copy()
    assert len(participants) > 0
    
    # Act - Delete all participants
    for email in participants:
        response = client.delete(f"/activities/{activity_name}/participants/{email}")
        assert response.status_code == 200
    
    # Assert
    final_response = client.get("/activities")
    final_data = final_response.json()
    assert len(final_data[activity_name]["participants"]) == 0


def test_delete_participant_from_different_activities(client):
    """
    Test deleting the same email from multiple activities after signup.
    
    Following AAA pattern:
    - Arrange: Sign up same email to multiple activities
    - Act: Delete the email from each activity
    - Assert: Verify deletion succeeds for each activity independently
    """
    # Arrange
    email = "versatile@mergington.edu"
    activities_to_test = ["Swimming Club", "Drama Club", "Art Class"]
    
    # Sign up to all activities
    for activity_name in activities_to_test:
        signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")
        assert signup_response.status_code == 200
    
    # Verify signups
    verify_response = client.get("/activities")
    verify_data = verify_response.json()
    for activity_name in activities_to_test:
        assert email in verify_data[activity_name]["participants"]
    
    # Act - Delete from each activity
    for activity_name in activities_to_test:
        delete_response = client.delete(f"/activities/{activity_name}/participants/{email}")
        assert delete_response.status_code == 200
    
    # Assert - Verify removal from all activities
    final_response = client.get("/activities")
    final_data = final_response.json()
    for activity_name in activities_to_test:
        assert email not in final_data[activity_name]["participants"]


def test_delete_with_url_encoded_email(client):
    """
    Test deletion with URL-encoded special characters in email.
    
    Following AAA pattern:
    - Arrange: Sign up email with special characters, then prepare for deletion
    - Act: DELETE with URL-encoded email
    - Assert: Verify deletion succeeds
    """
    # Arrange
    activity_name = "Debate Team"
    email_with_plus = "jane.doe+test@mergington.edu"
    
    # First sign up the participant
    signup_response = client.post(f"/activities/{activity_name}/signup?email={email_with_plus}")
    assert signup_response.status_code == 200
    
    # Verify signup
    check_response = client.get("/activities")
    check_data = check_response.json()
    assert email_with_plus in check_data[activity_name]["participants"]
    
    # Act - Delete with URL encoding (+ becomes %2B)
    import urllib.parse
    encoded_email = urllib.parse.quote(email_with_plus, safe='')
    delete_response = client.delete(f"/activities/{activity_name}/participants/{encoded_email}")
    
    # Assert
    assert delete_response.status_code == 200
    
    # Verify deletion
    final_response = client.get("/activities")
    final_data = final_response.json()
    assert email_with_plus not in final_data[activity_name]["participants"]
