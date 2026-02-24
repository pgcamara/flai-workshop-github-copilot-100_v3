"""
Tests for GET / (root) endpoint.

Tests verify that the root endpoint properly redirects to the static index page
following the AAA (Arrange-Act-Assert) pattern.
"""


def test_root_redirects_to_static_index(client):
    """
    Test that GET / redirects to /static/index.html.
    
    Following AAA pattern:
    - Arrange: Client fixture provides TestClient
    - Act: Make GET request to root endpoint
    - Assert: Verify redirect response with correct location
    """
    # Arrange
    # (client fixture provides the TestClient)
    
    # Act
    response = client.get("/", follow_redirects=False)
    
    # Assert
    assert response.status_code == 307  # Temporary redirect
    assert "location" in response.headers
    assert response.headers["location"] == "/static/index.html"


def test_root_redirect_can_be_followed(client):
    """
    Test that following the redirect from root leads to a valid response.
    
    Following AAA pattern:
    - Arrange: Client fixture provides TestClient
    - Act: Make GET request to root endpoint with follow_redirects=True
    - Assert: Verify final response is successful
    """
    # Arrange
    # (client fixture provides the TestClient)
    
    # Act
    response = client.get("/", follow_redirects=True)
    
    # Assert
    # Following the redirect should lead to the static HTML file
    assert response.status_code == 200
    # The response should be HTML content
    assert "text/html" in response.headers.get("content-type", "")


def test_root_returns_redirect_response_type(client):
    """
    Test that the root endpoint returns a RedirectResponse.
    
    Following AAA pattern:
    - Arrange: Client fixture provides TestClient
    - Act: Make GET request to root endpoint
    - Assert: Verify response is a redirect type (3xx status code)
    """
    # Arrange
    # (client fixture provides the TestClient)
    
    # Act
    response = client.get("/", follow_redirects=False)
    
    # Assert
    assert 300 <= response.status_code < 400  # Any 3xx redirect status code
    assert "location" in response.headers
